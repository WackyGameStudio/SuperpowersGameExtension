import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = REPO_ROOT / "scripts" / "install_to_project.py"
TEMPLATE_DIR = REPO_ROOT / "template"
GAME_SKILL_PAYLOAD_PATHS = [
    ".agents/skills/game-docs-maintaining/SKILL.md",
    ".agents/skills/game-engine-mcp-operating/SKILL.md",
    ".agents/skills/game-scene-ui-iteration/SKILL.md",
    ".agents/skills/game-playtesting-and-validation/SKILL.md",
    ".agents/skills/unreal-mcp-workflow/SKILL.md",
    ".agents/skills/unity-mcp-workflow/SKILL.md",
    ".agents/skills/game-ui-implementation/SKILL.md",
    ".agents/skills/game-asset-pipeline/SKILL.md",
    ".agents/skills/game-performance-budgeting/SKILL.md",
    ".agents/skills/game-save-data-migrations/SKILL.md",
    ".agents/skills/game-input-and-camera-design/SKILL.md",
    ".agents/skills/game-ai-behavior-debugging/SKILL.md",
    ".agents/skills/game-networking-authority/SKILL.md",
    ".agents/skills/game-content-branching-and-merging/SKILL.md",
    ".agents/skills/game-localization-accessibility/SKILL.md",
    ".agents/skills/game-build-release-platforms/SKILL.md",
]
COMPACT_DOC_PAYLOAD_PATHS = [
    "docs/game/00-index.md",
    "docs/game/01-product-brief.md",
    "docs/game/02-gameplay-design.md",
    "docs/game/03-content-and-ux.md",
    "docs/game/04-engine-architecture.md",
    "docs/game/05-validation-release.md",
    "docs/game/decision-log.md",
    "docs/game/change-log.md",
]
EXPECTED_TEMPLATE_PAYLOAD_PATHS = [
    "AGENTS.md",
    *GAME_SKILL_PAYLOAD_PATHS,
    *COMPACT_DOC_PAYLOAD_PATHS,
]


def load_installer():
    spec = importlib.util.spec_from_file_location("install_to_project", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def create_directory_link(link_path: Path, target_path: Path) -> None:
    if sys.platform == "win32":
        result = subprocess.run(
            ["cmd", "/c", "mklink", "/J", str(link_path), str(target_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip() or "mklink /J failed"
            pytest.skip(f"Windows symlink/junction creation unavailable: {detail}")
        return

    try:
        link_path.symlink_to(target_path, target_is_directory=True)
    except OSError as exc:
        pytest.skip(f"Directory symlink creation unavailable: {exc}")


def create_file_symlink(link_path: Path, target_path: Path) -> None:
    if sys.platform == "win32":
        result = subprocess.run(
            ["cmd", "/c", "mklink", str(link_path), str(target_path)],
            capture_output=True,
            text=True,
            check=False,
        )
        if result.returncode != 0:
            detail = (result.stderr or result.stdout).strip() or "mklink failed"
            pytest.skip(f"Windows file symlink creation unavailable: {detail}")
        return

    try:
        link_path.symlink_to(target_path)
    except OSError as exc:
        pytest.skip(f"File symlink creation unavailable: {exc}")


def test_build_plan_reports_template_files_for_empty_target(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    plan = installer.build_plan(TEMPLATE_DIR, target)
    create_paths = {action.relative_path for action in plan.creates}

    assert "AGENTS.md" in create_paths
    assert "docs/game/00-index.md" in create_paths
    assert ".agents/skills/game-docs-maintaining/SKILL.md" in create_paths
    assert plan.conflicts == []


def test_installer_required_payload_matches_compact_template_contract():
    installer = load_installer()

    required_paths = {
        installer.relative_posix(path)
        for path in installer.REQUIRED_TEMPLATE_PAYLOAD_PATHS
    }

    assert required_paths == set(EXPECTED_TEMPLATE_PAYLOAD_PATHS)


def test_build_plan_reports_nested_file_conflicts_when_parent_path_is_a_file(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    (target / "docs").write_text("blocked", encoding="utf-8")

    plan = installer.build_plan(TEMPLATE_DIR, target)
    create_paths = {action.relative_path for action in plan.creates}
    conflict_paths = {action.relative_path for action in plan.conflicts}

    assert "docs/game/00-index.md" in conflict_paths
    assert "docs/game/00-index.md" not in create_paths
    assert "AGENTS.md" in create_paths


def test_dry_run_prints_json_and_does_not_create_files(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
        "--dry-run",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["dry_run"] is True
    assert "AGENTS.md" in payload["create"]
    assert ".agents/skills/game-docs-maintaining/SKILL.md" in payload["create"]
    assert payload["conflicts"] == []
    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()
    assert not (REPO_ROOT / "AGENTS.md").exists()
    assert not (REPO_ROOT / ".agents").exists()


def test_dry_run_reports_current_template_payload_files(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
        "--dry-run",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    for relative_path in EXPECTED_TEMPLATE_PAYLOAD_PATHS:
        assert relative_path in payload["create"]


def test_install_manifest_includes_current_template_payload_files(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name=".superpowers-game-extension-manifest.json",
        dry_run=False,
    )

    manifest = json.loads((target / ".superpowers-game-extension-manifest.json").read_text(encoding="utf-8"))
    for relative_path in EXPECTED_TEMPLATE_PAYLOAD_PATHS:
        assert relative_path in manifest["installed_files"]


def test_current_payload_file_conflict_is_not_overwritten(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    existing_skill_path = target / ".agents" / "skills" / "game-ui-implementation" / "SKILL.md"
    existing_skill_path.parent.mkdir(parents=True)
    existing_skill_path.write_text("existing phase 3/4 skill instructions\n", encoding="utf-8")

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert ".agents/skills/game-ui-implementation/SKILL.md" in payload["conflicts"]
    assert existing_skill_path.read_text(encoding="utf-8") == "existing phase 3/4 skill instructions\n"


@pytest.mark.parametrize(
    "missing_relative_path",
    [
        ".agents/skills/game-ui-implementation/SKILL.md",
        ".agents/skills/game-build-release-platforms/SKILL.md",
        "docs/game/03-content-and-ux.md",
        "docs/game/05-validation-release.md",
    ],
)
def test_dry_run_rejects_template_directory_missing_new_required_payload_file(
    tmp_path,
    capsys,
    missing_relative_path,
):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    incomplete_template = tmp_path / "incomplete-template"
    shutil.copytree(TEMPLATE_DIR, incomplete_template)
    (incomplete_template / Path(missing_relative_path)).unlink()

    exit_code = installer.main([
        str(target),
        "--template",
        str(incomplete_template),
        "--dry-run",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    error = json.loads(captured.err)["error"]
    assert "template directory missing required paths:" in error
    assert missing_relative_path in error


def test_dry_run_reports_requested_manifest_path(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
        "--manifest",
        "tools/game-extension/install-manifest.json",
        "--dry-run",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 0
    assert payload["dry_run"] is True
    assert payload["manifest_path"] == "tools/game-extension/install-manifest.json"
    assert "AGENTS.md" in payload["create"]
    assert not (target / "AGENTS.md").exists()


def test_custom_manifest_matching_template_file_is_reported_as_conflict(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name="AGENTS.md",
        dry_run=False,
    )

    assert payload["conflicts"] == ["AGENTS.md"]
    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()


def test_custom_manifest_matching_existing_target_conflict_is_not_duplicated(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    (target / "AGENTS.md").write_text("existing\n", encoding="utf-8")

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name="AGENTS.md",
        dry_run=False,
    )

    assert payload["conflicts"] == ["AGENTS.md"]
    assert not (target / ".agents").exists()


def test_custom_manifest_nested_under_template_file_is_reported_as_conflict(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name="AGENTS.md/install-manifest.json",
        dry_run=False,
    )

    assert "AGENTS.md/install-manifest.json" in payload["conflicts"]
    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()
    assert not (target / "AGENTS.md" / "install-manifest.json").exists()


def test_dry_run_rejects_absolute_manifest_path(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    manifest = tmp_path / "install-manifest.json"

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
        "--manifest",
        str(manifest),
        "--dry-run",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert json.loads(captured.err)["error"]


def test_dry_run_rejects_manifest_path_outside_target_dir(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
        "--manifest",
        "../outside.json",
        "--dry-run",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert json.loads(captured.err)["error"]


def test_dry_run_rejects_template_path_that_is_a_file(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    exit_code = installer.main([
        str(target),
        "--template",
        str(REPO_ROOT / "pyproject.toml"),
        "--dry-run",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert json.loads(captured.err)["error"]


def test_dry_run_rejects_template_directory_missing_required_payload(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    incomplete_template = tmp_path / "incomplete-template"
    incomplete_template.mkdir()
    (incomplete_template / "AGENTS.md").write_text("partial\n", encoding="utf-8")
    (incomplete_template / ".agents" / "skills").mkdir(parents=True)
    (incomplete_template / "docs" / "game").mkdir(parents=True)

    exit_code = installer.main([
        str(target),
        "--template",
        str(incomplete_template),
        "--dry-run",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    error = json.loads(captured.err)["error"]
    assert "template directory missing required paths:" in error
    assert ".agents/skills/game-docs-maintaining/SKILL.md" in error
    assert "docs/game/00-index.md" in error


@pytest.mark.parametrize(
    "missing_relative_path",
    [
        ".agents/skills/game-docs-maintaining/SKILL.md",
        "docs/game/00-index.md",
    ],
)
def test_dry_run_rejects_template_directory_missing_single_required_payload_file(
    tmp_path,
    capsys,
    missing_relative_path,
):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    incomplete_template = tmp_path / "incomplete-template"
    shutil.copytree(TEMPLATE_DIR, incomplete_template)
    (incomplete_template / Path(missing_relative_path)).unlink()

    exit_code = installer.main([
        str(target),
        "--template",
        str(incomplete_template),
        "--dry-run",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    error = json.loads(captured.err)["error"]
    assert "template directory missing required paths:" in error
    assert missing_relative_path in error


def test_symlinked_target_ancestors_are_reported_as_conflicts_and_not_written(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    outside_docs = tmp_path / "outside-docs"
    outside_docs.mkdir()
    outside_tools = tmp_path / "outside-tools"
    outside_tools.mkdir()

    create_directory_link(target / "docs", outside_docs)
    create_directory_link(target / "tools", outside_tools)

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name="tools/game-extension/install-manifest.json",
        dry_run=False,
    )

    assert "docs/game/00-index.md" in payload["conflicts"]
    assert "tools/game-extension/install-manifest.json" in payload["conflicts"]
    assert not (outside_docs / "game" / "00-index.md").exists()
    assert not (outside_tools / "game-extension" / "install-manifest.json").exists()
    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()


def test_linked_target_ancestor_inside_target_is_reported_as_conflict_and_not_written(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    real_docs = target / "real-docs"
    real_docs.mkdir()

    create_directory_link(target / "docs", real_docs)

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        dry_run=False,
    )

    assert "docs/game/00-index.md" in payload["conflicts"]
    assert not (real_docs / "game" / "00-index.md").exists()
    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()


@pytest.mark.skipif(sys.platform != "win32", reason="Windows junction fallback only")
def test_path_is_link_or_junction_detects_junction_without_path_is_junction(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    outside_docs = tmp_path / "outside-docs"
    outside_docs.mkdir()
    link_path = target / "docs"

    create_directory_link(link_path, outside_docs)

    class PathWithoutIsJunction:
        def __init__(self, wrapped_path: Path):
            self._wrapped_path = wrapped_path

        def __fspath__(self) -> str:
            return str(self._wrapped_path)

        def is_symlink(self) -> bool:
            return False

    assert installer.path_is_link_or_junction(PathWithoutIsJunction(link_path)) is True


def test_manifest_parent_link_inside_target_is_reported_as_conflict_and_not_written(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    real_tools = target / "real-tools"
    real_tools.mkdir()

    create_directory_link(target / "tools", real_tools)

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name="tools/game-extension/install-manifest.json",
        dry_run=False,
    )

    assert "tools/game-extension/install-manifest.json" in payload["conflicts"]
    assert not (real_tools / "game-extension" / "install-manifest.json").exists()
    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()


def test_dangling_symlink_target_file_is_reported_as_conflict_and_not_written(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    outside_agents = tmp_path / "outside" / "AGENTS.md"

    create_file_symlink(target / "AGENTS.md", outside_agents)

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        dry_run=False,
    )

    assert payload["conflicts"] == ["AGENTS.md"]
    assert not outside_agents.exists()
    assert (target / "AGENTS.md").is_symlink()
    assert not (target / ".agents").exists()


def test_dangling_symlink_target_ancestor_is_reported_as_conflict_and_not_written(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    outside_docs = tmp_path / "outside-docs"

    create_directory_link(target / "docs", outside_docs)

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        dry_run=False,
    )

    assert "docs/game/00-index.md" in payload["conflicts"]
    assert not (outside_docs / "game" / "00-index.md").exists()
    assert not (target / "AGENTS.md").exists()


def test_install_copies_hidden_agents_docs_and_writes_manifest(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    payload = installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name=".superpowers-game-extension-manifest.json",
        dry_run=False,
    )

    manifest_path = target / ".superpowers-game-extension-manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    assert payload["dry_run"] is False
    assert payload["conflicts"] == []
    assert (target / "AGENTS.md").exists()
    assert (target / "docs" / "game" / "00-index.md").exists()
    assert (target / ".agents" / "skills" / "game-docs-maintaining" / "SKILL.md").exists()
    assert manifest["extension_version"] == installer.VERSION
    assert manifest["installed_at"]
    assert manifest["source_repo"] == str(REPO_ROOT.resolve())
    assert manifest["template_dir"] == str(TEMPLATE_DIR.resolve())
    assert manifest["target_project"] == str(target.resolve())
    assert "AGENTS.md" in manifest["installed_files"]
    assert ".agents/skills/game-docs-maintaining/SKILL.md" in manifest["installed_files"]
    assert manifest["skipped_files"] == []
    assert manifest["conflicts"] == []
    assert not (REPO_ROOT / "AGENTS.md").exists()
    assert not (REPO_ROOT / ".agents").exists()


def test_existing_target_file_is_conflict_and_is_not_overwritten(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    existing_agents = target / "AGENTS.md"
    existing_agents.write_text("custom project instructions\n", encoding="utf-8")

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert "AGENTS.md" in payload["conflicts"]
    assert existing_agents.read_text(encoding="utf-8") == "custom project instructions\n"
    assert not (target / ".agents").exists()
    assert not (target / ".superpowers-game-extension-manifest.json").exists()


def test_reinstall_reports_conflicts(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name=".superpowers-game-extension-manifest.json",
        dry_run=False,
    )
    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
        "--dry-run",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert "AGENTS.md" in payload["conflicts"]
    assert ".agents/skills/game-docs-maintaining/SKILL.md" in payload["conflicts"]


def test_existing_manifest_path_is_conflict_and_is_not_overwritten(tmp_path, capsys):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    manifest_path = target / "tools" / "game-extension" / "install-manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text("existing manifest\n", encoding="utf-8")

    exit_code = installer.main([
        str(target),
        "--template",
        str(TEMPLATE_DIR),
        "--manifest",
        "tools/game-extension/install-manifest.json",
    ])

    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert exit_code == 1
    assert "tools/game-extension/install-manifest.json" in payload["conflicts"]
    assert manifest_path.read_text(encoding="utf-8") == "existing manifest\n"
    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()


def test_custom_manifest_parent_file_blocker_is_reported_before_copy(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()
    blocked_parent = target / "tools"
    blocked_parent.write_text("blocked\n", encoding="utf-8")

    payload = None
    error = None
    try:
        payload = installer.install_template(
            template_dir=TEMPLATE_DIR,
            target_dir=target,
            manifest_name="tools/game-extension/install-manifest.json",
            dry_run=False,
        )
    except Exception as exc:  # pragma: no cover - exercised by the failing pre-fix behavior
        error = exc

    assert not (target / "AGENTS.md").exists()
    assert not (target / ".agents").exists()
    assert blocked_parent.read_text(encoding="utf-8") == "blocked\n"
    assert error is None
    assert payload is not None
    assert payload["conflicts"] == ["tools/game-extension/install-manifest.json"]


def test_custom_manifest_relative_path(tmp_path):
    installer = load_installer()
    target = tmp_path / "GameProject"
    target.mkdir()

    installer.install_template(
        template_dir=TEMPLATE_DIR,
        target_dir=target,
        manifest_name="tools/game-extension/install-manifest.json",
        dry_run=False,
    )

    assert (target / "tools" / "game-extension" / "install-manifest.json").exists()


def test_dry_run_rejects_self_install_to_source_repo_root(capsys):
    installer = load_installer()

    exit_code = installer.main([
        str(REPO_ROOT),
        "--template",
        str(TEMPLATE_DIR),
        "--dry-run",
    ])

    captured = capsys.readouterr()

    assert exit_code == 2
    assert "source repo root" in json.loads(captured.err)["error"]


def test_install_rejects_self_install_to_source_repo_root(monkeypatch):
    installer = load_installer()

    copy_called = False
    manifest_called = False

    def fake_copy_files(plan):
        nonlocal copy_called
        copy_called = True

    def fake_write_manifest(*args, **kwargs):
        nonlocal manifest_called
        manifest_called = True

    monkeypatch.setattr(installer, "copy_files", fake_copy_files)
    monkeypatch.setattr(installer, "write_manifest", fake_write_manifest)

    with pytest.raises(ValueError, match="source repo root"):
        installer.install_template(
            template_dir=TEMPLATE_DIR,
            target_dir=REPO_ROOT,
            dry_run=False,
        )

    assert copy_called is False
    assert manifest_called is False
