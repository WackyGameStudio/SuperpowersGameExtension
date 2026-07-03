from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_MARKER = "<!-- superpowers-game-extension: game-project-instructions -->"

EXPECTED_DOCS = [
    "00-index.md",
    "01-product-brief.md",
    "02-gameplay-design.md",
    "03-content-and-ux.md",
    "04-engine-architecture.md",
    "05-validation-release.md",
    "decision-log.md",
    "change-log.md",
]

DOC_REQUIRED_HEADINGS = {
    "00-index.md": ["# 게임 문서 색인", "## 프로젝트 식별", "## 핵심 문서 맵", "## Split criteria"],
    "01-product-brief.md": ["# Product Brief", "## One-line pitch", "## Design pillars", "## Core loop summary"],
    "02-gameplay-design.md": ["# Gameplay Design", "## Core, session, and reward loops", "## Player verbs", "## Gameplay systems"],
    "03-content-and-ux.md": ["# Content and UX", "## Scenes, levels, and maps", "## UI and UX flow", "## Localization and accessibility"],
    "04-engine-architecture.md": ["# Engine Architecture", "## Engine identity", "## Runtime modules and plugins", "## Save schema and migration policy"],
    "05-validation-release.md": ["# Validation and Release", "## Smoke test matrix", "## Performance budgets", "## Build and release targets"],
    "decision-log.md": ["# Decision Log", "## Entries", "## Recording criteria"],
    "change-log.md": ["# Change Log", "## Entries", "## Recording criteria"],
}


EXPECTED_SKILLS = {
    "game-docs-maintaining": "Use when changing game design, gameplay behavior, content, UI/UX, engine architecture, save/network data, validation, performance, build targets, release constraints, or docs/game files.",
    "game-engine-mcp-operating": "Use when connecting to Unreal or Unity MCP, using editor tools, changing engine-owned assets, inspecting scenes, or validating editor state through MCP.",
    "game-scene-ui-iteration": "Use when modifying levels, scenes, maps, actors, GameObjects, prefabs, world objects, spawn points, lighting, collision, navigation, or visual hierarchy in an engine editor.",
    "game-playtesting-and-validation": "Use when verifying gameplay behavior, reproducing bugs, running Unity Edit or Play Mode tests, Unreal Automation tests, functional tests, smoke tests, or editor log checks.",
    "unreal-mcp-workflow": "Use when working with Unreal MCP, Unreal Editor automation, Unreal levels, actors, Blueprints, UMG, CommonUI, materials, PIE, or Automation tests.",
    "unity-mcp-workflow": "Use when working with Unity MCP, Unity Editor automation, scenes, GameObjects, prefabs, ScriptableObjects, uGUI, UI Toolkit, Play Mode, or Edit Mode tests.",
    "game-ui-implementation": "Use when changing HUDs, menus, UI screens, modal flow, UI state ownership, runtime UI binding, focus/navigation, input mode, uGUI, UI Toolkit, UMG, or CommonUI.",
    "game-asset-pipeline": "Use when changing asset import settings, materials, textures, meshes, audio, prefabs, Blueprints, ScriptableObjects, naming, folder taxonomy, source/generated policy, or reference integrity.",
    "game-performance-budgeting": "Use when working on FPS, frame time, hitches, memory, draw calls, shader cost, loading time, build size, profiling, or performance budgets in a game.",
    "game-save-data-migrations": "Use when changing save data schema, persistence format, player progression data, migration logic, backward compatibility, or save/load tests in a game.",
    "game-input-and-camera-design": "Use when changing player controls, input mapping, Unity Input System, Unreal Enhanced Input, camera behavior, camera states, aiming, lock-on, or control accessibility.",
    "game-ai-behavior-debugging": "Use when changing AI behavior, Behavior Trees, state machines, NavMesh, pathfinding, perception, blackboards, utility AI, spawn logic, or enemy debugging.",
    "game-networking-authority": "Use when changing multiplayer networking, authority, ownership, replication, prediction, rollback, matchmaking state, or deterministic gameplay tests.",
    "game-content-branching-and-merging": "Use when resolving engine asset conflicts, binary asset locks, Unity YAML conflicts, prefab or Blueprint merge issues, Unreal OFPA changes, generated file churn, or content branch strategy.",
    "game-build-release-platforms": "Use when changing build scenes/maps, packaging, platform targets, CI build scripts, store submission, release checklist, platform-specific configuration, or certification constraints.",
    "game-localization-accessibility": "Use when changing localization keys, translated text, font fallback, subtitles, readability, colorblind support, input accessibility, safe areas, or platform accessibility requirements.",
}

FORBIDDEN_UNITY_MCP_DETAILS = [
    "mcpforunity://editor/state",
    "mcpforunity://project/info",
    "mcpforunity://instances",
    "find_gameobjects",
    "read_console",
    "run_tests",
    "get_test_job",
]

UNREAL_MCP_REQUIRED_PHRASES = [
    "Tool Search mode",
    "`tools/list`가 `list_toolsets`, `describe_toolset`, `call_tool` 세 meta-tool만 반환해도 정상으로 본다",
    "`list_toolsets`로 Toolset Registry를 확인한다",
    "`describe_toolset`으로 필요한 toolset schema와 mutating 여부를 확인한다",
    "`call_tool`은 한 번에 하나씩 순차 실행한다",
    "Required read-only probes",
    "`EditorToolset.EditorAppToolset`",
    "`EditorToolset.LogsToolset`",
    "`editor_toolset.toolsets.scene.SceneTools`",
    "`AutomationTestToolset.AutomationTestToolset`",
    "`PCGToolset.PCGToolset`",
    "PCG graph 생성, UMG widget 생성, Slate click/type/drag, Blueprint/asset/map 변경은 mutating operation으로 취급한다",
    "mutating operation 전에는 사용자 승인, snapshot, rollback 경로, validation plan을 먼저 남긴다",
    "`Saved/Logs/*.log`",
    "Saved/Logs/*-backup-*.log",
    "`volatile_changed_files`",
    "`.uasset`, `.umap`",
    "`.uasset`와 `.umap`을 text editor로 수정하지 않는다",
    "Unreal MCP tool call은 overlapping하지 않고 serial로 수행한다.",
    "`Saved` 전체를 허용하지 않는다",
    "MCP Inspector",
    "ModelContextProtocol.RefreshTools",
]


def frontmatter_value(text: str, key: str) -> str:
    lines = text.splitlines()
    assert lines[0] == "---"
    end_index = lines[1:].index("---") + 1
    for line in lines[1:end_index]:
        if line.startswith(f"{key}:"):
            return line.split(":", 1)[1].strip().strip('"')
    raise AssertionError(f"missing frontmatter key: {key}")


def body_after_frontmatter(text: str) -> str:
    lines = text.splitlines()
    assert lines[0] == "---"
    end_index = lines[1:].index("---") + 1
    return "\n".join(lines[end_index + 1 :])


def test_extension_repo_does_not_expose_local_agents_at_root():
    assert not (REPO_ROOT / ".agents").exists()
    assert not (REPO_ROOT / "AGENTS.md").exists()


def test_template_agents_md_exists_and_names_required_skills():
    agents_md = REPO_ROOT / "template" / "AGENTS.md"

    assert agents_md.exists()
    text = agents_md.read_text(encoding="utf-8")

    assert "이 저장소는 게임 프로젝트입니다." in text
    assert "Global Superpowers workflow는 그대로 적용합니다." in text
    assert INSTALL_MARKER in text
    for skill_name in [
        "game-docs-maintaining",
        "game-engine-mcp-operating",
        "game-scene-ui-iteration",
        "game-playtesting-and-validation",
        "unreal-mcp-workflow",
        "unity-mcp-workflow",
        "game-ui-implementation",
        "game-asset-pipeline",
        "game-performance-budgeting",
        "game-save-data-migrations",
        "game-input-and-camera-design",
        "game-ai-behavior-debugging",
        "game-networking-authority",
        "game-content-branching-and-merging",
        "game-build-release-platforms",
        "game-localization-accessibility",
    ]:
        assert skill_name in text
    assert "unity-mcp-orchestrator" in text
    assert ".codex/skills/unity-mcp-skill/SKILL.md" in text


def test_template_agents_md_documents_compact_docs_and_skill_routing():
    text = (REPO_ROOT / "template" / "AGENTS.md").read_text(encoding="utf-8")

    required_phrases = [
        "## 살아 있는 게임 문서 정책",
        "6개 핵심 문서와 2개 로그",
        "`01-product-brief.md`",
        "`05-validation-release.md`",
        "## Game skill routing",
        "game-build-release-platforms",
        "brainstorming",
        "writing-plans",
        "implementation",
        "verification",
        "unity-mcp-orchestrator",
        "## 완료의 의미는 검증됨",
    ]
    for phrase in required_phrases:
        assert phrase in text


def test_install_runbook_uses_template_marker_for_duplicate_detection():
    agents_text = (REPO_ROOT / "template" / "AGENTS.md").read_text(encoding="utf-8")
    install_text = (REPO_ROOT / "INSTALL_FOR_AI.md").read_text(encoding="utf-8")

    assert INSTALL_MARKER in agents_text
    assert INSTALL_MARKER in install_text
    assert "## Game skill routing" in agents_text


def test_existing_skills_document_compact_docs_and_domain_handoffs():
    skills_dir = REPO_ROOT / "template" / ".agents" / "skills"

    docs = (skills_dir / "game-docs-maintaining" / "SKILL.md").read_text(encoding="utf-8")
    scene_ui = (skills_dir / "game-scene-ui-iteration" / "SKILL.md").read_text(encoding="utf-8")
    validation = (skills_dir / "game-playtesting-and-validation" / "SKILL.md").read_text(encoding="utf-8")
    engine_mcp = (skills_dir / "game-engine-mcp-operating" / "SKILL.md").read_text(encoding="utf-8")
    build_release = (skills_dir / "game-build-release-platforms" / "SKILL.md").read_text(encoding="utf-8")

    for phrase in [
        "## Core documents",
        "`01-product-brief.md`",
        "`02-gameplay-design.md`",
        "`03-content-and-ux.md`",
        "`04-engine-architecture.md`",
        "`05-validation-release.md`",
        "Do not create a new docs file unless the split criteria below are met.",
        "Final response says which docs changed or why docs were not changed.",
    ]:
        assert phrase in docs

    assert "runtime binding, focus/navigation, input mode, screen flow" in scene_ui
    assert "domain-specific evidence" in validation
    assert "asset import, UI binding, AI behavior, networking, localization" in engine_mcp
    assert "Build/release work changes how the game is packaged" in build_release
    assert "`docs/game/05-validation-release.md`" in build_release


def test_docs_game_template_file_list_is_compact_contract():
    docs_dir = REPO_ROOT / "template" / "docs" / "game"
    actual_docs = sorted(path.name for path in docs_dir.glob("*.md"))

    assert actual_docs == sorted(EXPECTED_DOCS)


def test_docs_game_templates_exist_with_required_headings():
    docs_dir = REPO_ROOT / "template" / "docs" / "game"

    for filename in EXPECTED_DOCS:
        path = docs_dir / filename
        assert path.exists(), f"missing docs template: {filename}"
        text = path.read_text(encoding="utf-8")
        for heading in DOC_REQUIRED_HEADINGS[filename]:
            assert heading in text, f"{filename} missing heading: {heading}"


def test_docs_index_maps_all_game_docs():
    index = (REPO_ROOT / "template" / "docs" / "game" / "00-index.md").read_text(encoding="utf-8")

    for filename in EXPECTED_DOCS:
        if filename == "00-index.md":
            continue
        assert f"`{filename}`" in index


def test_mvp_skills_exist_with_trigger_only_descriptions():
    skills_dir = REPO_ROOT / "template" / ".agents" / "skills"

    for skill_name, expected_description in EXPECTED_SKILLS.items():
        path = skills_dir / skill_name / "SKILL.md"
        assert path.exists(), f"missing skill: {skill_name}"
        text = path.read_text(encoding="utf-8")
        assert frontmatter_value(text, "name") == skill_name
        assert frontmatter_value(text, "description") == expected_description
        assert "## Workflow" in text
        assert "## Verification" in text
        assert "## Overview" in text
        assert body_after_frontmatter(text).strip(), f"{skill_name} body must not be empty"


def test_unity_mcp_workflow_delegates_to_mcpforunity_local_skill():
    skills_dir = REPO_ROOT / "template" / ".agents" / "skills"
    unity_workflow = (skills_dir / "unity-mcp-workflow" / "SKILL.md").read_text(encoding="utf-8")
    engine_mcp = (skills_dir / "game-engine-mcp-operating" / "SKILL.md").read_text(encoding="utf-8")
    scene_ui = (skills_dir / "game-scene-ui-iteration" / "SKILL.md").read_text(encoding="utf-8")
    validation = (skills_dir / "game-playtesting-and-validation" / "SKILL.md").read_text(encoding="utf-8")

    assert "unity-mcp-orchestrator" in unity_workflow
    assert ".codex/skills/unity-mcp-skill/SKILL.md" in unity_workflow
    for text in (engine_mcp, scene_ui, validation):
        assert "unity-mcp-orchestrator" in text

    assert ".codex/skills/unity-mcp-skill/SKILL.md" in engine_mcp

    all_skill_texts = [
        path.read_text(encoding="utf-8")
        for path in (skills_dir).glob("*/SKILL.md")
    ]
    for text in all_skill_texts:
        for detail in FORBIDDEN_UNITY_MCP_DETAILS:
            assert detail not in text


def test_unreal_mcp_workflow_documents_tool_search_mode_and_guardrails():
    skills_dir = REPO_ROOT / "template" / ".agents" / "skills"
    unreal_workflow = (skills_dir / "unreal-mcp-workflow" / "SKILL.md").read_text(encoding="utf-8")

    for phrase in UNREAL_MCP_REQUIRED_PHRASES:
        assert phrase in unreal_workflow

    assert "Saved/Autosaves/**" in unreal_workflow
    assert "Saved/Backup/**" in unreal_workflow
    assert "Saved/Config/**" in unreal_workflow
    assert "Saved/Cooked/**" in unreal_workflow
    assert "Saved/StagedBuilds/**" in unreal_workflow


def test_engine_mcp_operating_hands_off_unreal_tool_search_to_unreal_skill():
    skills_dir = REPO_ROOT / "template" / ".agents" / "skills"
    engine_mcp = (skills_dir / "game-engine-mcp-operating" / "SKILL.md").read_text(encoding="utf-8")

    required_phrases = [
        "Unreal 작업은 `unreal-mcp-workflow`에서 Tool Search mode와 read-only/mutating guardrail을 따른다",
        "`tools/list` meta-tool 3개만 보고 blocker로 판단하지 않는다",
        "Unreal-specific toolset inspection은 `unreal-mcp-workflow`에 위임한다",
    ]
    for phrase in required_phrases:
        assert phrase in engine_mcp
