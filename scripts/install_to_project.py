from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


VERSION = "0.1.0"
SOURCE_REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MANIFEST_NAME = ".superpowers-game-extension-manifest.json"
REQUIRED_TEMPLATE_PAYLOAD_PATHS = (
    Path("AGENTS.md"),
    Path(".agents") / "skills" / "game-docs-maintaining" / "SKILL.md",
    Path(".agents") / "skills" / "game-engine-mcp-operating" / "SKILL.md",
    Path(".agents") / "skills" / "game-scene-ui-iteration" / "SKILL.md",
    Path(".agents") / "skills" / "game-playtesting-and-validation" / "SKILL.md",
    Path(".agents") / "skills" / "unreal-mcp-workflow" / "SKILL.md",
    Path(".agents") / "skills" / "unity-mcp-workflow" / "SKILL.md",
    Path(".agents") / "skills" / "game-ui-implementation" / "SKILL.md",
    Path(".agents") / "skills" / "game-asset-pipeline" / "SKILL.md",
    Path(".agents") / "skills" / "game-performance-budgeting" / "SKILL.md",
    Path(".agents") / "skills" / "game-save-data-migrations" / "SKILL.md",
    Path(".agents") / "skills" / "game-input-and-camera-design" / "SKILL.md",
    Path(".agents") / "skills" / "game-ai-behavior-debugging" / "SKILL.md",
    Path(".agents") / "skills" / "game-networking-authority" / "SKILL.md",
    Path(".agents") / "skills" / "game-content-branching-and-merging" / "SKILL.md",
    Path(".agents") / "skills" / "game-localization-accessibility" / "SKILL.md",
    Path(".agents") / "skills" / "game-build-release-platforms" / "SKILL.md",
    Path("docs") / "game" / "00-index.md",
    Path("docs") / "game" / "01-product-brief.md",
    Path("docs") / "game" / "02-gameplay-design.md",
    Path("docs") / "game" / "03-content-and-ux.md",
    Path("docs") / "game" / "04-engine-architecture.md",
    Path("docs") / "game" / "05-validation-release.md",
    Path("docs") / "game" / "decision-log.md",
    Path("docs") / "game" / "change-log.md",
)


@dataclass(frozen=True)
class PlannedAction:
    relative_path: str
    source_path: Path
    target_path: Path


@dataclass(frozen=True)
class InstallPlan:
    creates: list[PlannedAction]
    conflicts: list[PlannedAction]
    skipped: list[PlannedAction]


def relative_posix(path: Path) -> str:
    return path.as_posix()


def validate_template_dir(template_dir: Path) -> None:
    if not template_dir.exists():
        raise FileNotFoundError(f"template directory does not exist: {template_dir}")
    if not template_dir.is_dir():
        raise NotADirectoryError(f"template path is not a directory: {template_dir}")

    missing_paths: list[str] = []
    for required_path in REQUIRED_TEMPLATE_PAYLOAD_PATHS:
        if not (template_dir / required_path).is_file():
            missing_paths.append(relative_posix(required_path))

    if missing_paths:
        missing = ", ".join(sorted(missing_paths))
        raise ValueError(f"template directory missing required paths: {missing}")


def iter_template_files(template_dir: Path) -> Iterable[Path]:
    for path in sorted(template_dir.rglob("*")):
        if path.is_file():
            yield path


def has_file_ancestor(path: Path, stop_at: Path) -> bool:
    ancestor = path.parent
    while ancestor != stop_at:
        if path_exists_or_is_symlink(ancestor) and (
            path_is_link_or_junction(ancestor) or not ancestor.is_dir()
        ):
            return True
        ancestor = ancestor.parent
    return False


def path_is_within(path: Path, possible_parent: Path) -> bool:
    try:
        path.relative_to(possible_parent)
    except ValueError:
        return False
    return True


def path_exists_or_is_symlink(path: Path) -> bool:
    return os.path.lexists(path)


def windows_path_is_directory_reparse_point(path: os.PathLike[str] | str) -> bool:
    if os.name != "nt":
        return False

    try:
        path_value = os.fspath(path)
        path_stat = os.lstat(path_value)
    except (OSError, TypeError, ValueError):
        return False

    reparse_point_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x0400)
    return bool(path_stat.st_file_attributes & reparse_point_flag) and os.path.isdir(path_value)


def path_is_link_or_junction(path: Path) -> bool:
    is_junction = getattr(path, "is_junction", lambda: False)
    return path.is_symlink() or is_junction() or windows_path_is_directory_reparse_point(path)


def normalize_relative_path(path: Path, description: str) -> Path:
    normalized_parts: list[str] = []
    for part in path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if not normalized_parts:
                raise ValueError(f"{description} must stay within the target project: {path}")
            normalized_parts.pop()
            continue
        normalized_parts.append(part)

    return Path(*normalized_parts) if normalized_parts else Path()


def resolve_via_existing_ancestor(path: Path) -> Path:
    missing_parts: list[str] = []
    existing_ancestor = path
    while not path_exists_or_is_symlink(existing_ancestor):
        missing_parts.append(existing_ancestor.name)
        parent = existing_ancestor.parent
        if parent == existing_ancestor:
            break
        existing_ancestor = parent

    resolved_path = existing_ancestor.resolve()
    for part in reversed(missing_parts):
        resolved_path /= part
    return resolved_path


def escapes_target_dir(path: Path, target_dir: Path) -> bool:
    resolved_path = resolve_via_existing_ancestor(path)
    return not path_is_within(resolved_path, target_dir)


def manifest_conflicts_with_plan(manifest_path: Path, plan: InstallPlan) -> bool:
    for action in plan.creates:
        if path_is_within(manifest_path, action.target_path):
            return True
        if path_is_within(action.target_path, manifest_path):
            return True
    return False


def build_plan(template_dir: Path, target_dir: Path) -> InstallPlan:
    template_dir = template_dir.resolve()
    target_dir = target_dir.resolve()
    creates: list[PlannedAction] = []
    conflicts: list[PlannedAction] = []

    for source_path in iter_template_files(template_dir):
        relative_path = relative_posix(source_path.relative_to(template_dir))
        target_path = target_dir / relative_path
        action = PlannedAction(
            relative_path=relative_path,
            source_path=source_path,
            target_path=target_path,
        )
        if (
            path_exists_or_is_symlink(target_path)
            or has_file_ancestor(target_path, target_dir)
            or escapes_target_dir(target_path, target_dir)
        ):
            conflicts.append(action)
        else:
            creates.append(action)

    return InstallPlan(creates=creates, conflicts=conflicts, skipped=[])


def plan_to_payload(plan: InstallPlan, dry_run: bool) -> dict[str, object]:
    return {
        "dry_run": dry_run,
        "create": [action.relative_path for action in plan.creates],
        "conflicts": [action.relative_path for action in plan.conflicts],
        "skipped": [action.relative_path for action in plan.skipped],
    }


def resolve_manifest_path(target_dir: Path, manifest_name: str) -> Path:
    manifest_path = Path(manifest_name)
    if manifest_path.is_absolute():
        raise ValueError(f"manifest path must be relative to the target project: {manifest_name}")
    target_root = target_dir.resolve()
    normalized_manifest_path = normalize_relative_path(
        manifest_path,
        description="manifest path",
    )
    return target_root / normalized_manifest_path


def append_conflict(payload: dict[str, object], relative_path: str) -> None:
    conflicts = payload["conflicts"]
    if not isinstance(conflicts, list):
        raise TypeError("payload conflicts must be a list")
    if relative_path not in conflicts:
        conflicts.append(relative_path)


def paths(actions: list[PlannedAction]) -> list[str]:
    return [action.relative_path for action in actions]


def copy_files(plan: InstallPlan) -> None:
    for action in plan.creates:
        action.target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(action.source_path, action.target_path)


def write_manifest(
    manifest_path: Path,
    template_dir: Path,
    target_dir: Path,
    plan: InstallPlan,
) -> None:
    manifest = {
        "extension_version": VERSION,
        "installed_at": datetime.now(timezone.utc).isoformat(),
        "source_repo": str(SOURCE_REPO_ROOT),
        "template_dir": str(template_dir.resolve()),
        "target_project": str(target_dir.resolve()),
        "installed_files": paths(plan.creates),
        "skipped_files": paths(plan.skipped),
        "conflicts": paths(plan.conflicts),
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def install_template(
    template_dir: Path,
    target_dir: Path,
    manifest_name: str = DEFAULT_MANIFEST_NAME,
    dry_run: bool = False,
) -> dict[str, object]:
    validate_template_dir(template_dir)
    if not target_dir.exists():
        raise FileNotFoundError(f"target directory does not exist: {target_dir}")
    if not target_dir.is_dir():
        raise NotADirectoryError(f"target path is not a directory: {target_dir}")

    template_dir = template_dir.resolve()
    target_dir = target_dir.resolve()
    if target_dir == SOURCE_REPO_ROOT:
        raise ValueError(f"target directory must not be the source repo root: {SOURCE_REPO_ROOT}")

    manifest_path = resolve_manifest_path(target_dir, manifest_name)
    manifest_relative_path = relative_posix(manifest_path.relative_to(target_dir))
    plan = build_plan(template_dir, target_dir)
    payload = plan_to_payload(plan, dry_run=dry_run)
    payload["manifest_path"] = manifest_relative_path

    if (
        path_exists_or_is_symlink(manifest_path)
        or has_file_ancestor(manifest_path, target_dir)
        or escapes_target_dir(manifest_path, target_dir)
        or manifest_conflicts_with_plan(manifest_path, plan)
    ):
        append_conflict(payload, manifest_relative_path)

    if dry_run or payload["conflicts"]:
        return payload

    copy_files(plan)
    write_manifest(
        manifest_path=manifest_path,
        template_dir=template_dir,
        target_dir=target_dir,
        plan=plan,
    )
    return payload


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install the Superpowers game extension template into a game project.",
    )
    parser.add_argument("target", type=Path, help="Target game project root")
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "template",
        help="Template directory to install",
    )
    parser.add_argument(
        "--manifest",
        default=DEFAULT_MANIFEST_NAME,
        help="Manifest filename or relative path inside the target project",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned changes without writing files",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        payload = install_template(
            template_dir=args.template,
            target_dir=args.target,
            manifest_name=args.manifest,
            dry_run=args.dry_run,
        )
    except (FileNotFoundError, NotADirectoryError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, indent=2), file=sys.stderr)
        return 2

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 1 if payload["conflicts"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
