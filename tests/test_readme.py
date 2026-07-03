from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


KOREAN_README = REPO_ROOT / "README.md"
ENGLISH_README = REPO_ROOT / "README.en.md"
REMOVED_KOREAN_README = REPO_ROOT / "README.kr.md"


def assert_readme_documents_install_flow_and_root_safety(readme: Path) -> None:
    assert readme.exists()
    text = readme.read_text(encoding="utf-8")

    assert "INSTALL_FOR_AI.md" in text
    assert "template/" in text
    assert ".agents/skills" in text
    assert "AGENTS.md" in text
    assert "docs/game" in text
    assert "이 extension repo 루트에는 `.agents/`와 `AGENTS.md`를 만들지 않습니다" in text or "own root does not contain `.agents/` or `AGENTS.md`" in text
    assert "Codex plugin packaging" in text


def test_readmes_document_install_flow_and_root_safety():
    assert_readme_documents_install_flow_and_root_safety(KOREAN_README)
    assert_readme_documents_install_flow_and_root_safety(ENGLISH_README)


def test_readme_language_files_are_korean_default_and_english_translation():
    assert KOREAN_README.exists()
    assert ENGLISH_README.exists()
    assert not REMOVED_KOREAN_README.exists()


def assert_readme_documents_phase_3_4_game_skills(readme: Path) -> None:
    text = readme.read_text(encoding="utf-8")

    for skill_name in [
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

    assert "instruction-based activation" in text
    assert "AGENTS.md" in text
    assert "SKILL.md" in text
    assert "Codex plugin packaging" in text


def test_readmes_document_phase_3_4_game_skills_and_activation_model():
    assert_readme_documents_phase_3_4_game_skills(KOREAN_README)
    assert_readme_documents_phase_3_4_game_skills(ENGLISH_README)


def test_readmes_do_not_list_v1_v2_skills_as_only_excluded_scope():
    for readme in [KOREAN_README, ENGLISH_README]:
        text = readme.read_text(encoding="utf-8")
        assert "- V1/V2 game skills" not in text


def test_korean_readme_leads_with_problem_solution_and_quick_start():
    text = KOREAN_README.read_text(encoding="utf-8")

    expected_headings = [
        "## 왜 필요한가",
        "## 어떻게 해결하나",
        "## Quick Start",
        "## 설치하면 생기는 것",
        "## 사용 방식",
        "## Unity/Unreal MCP와 안전 규칙",
        "## Living Docs",
        "## 포함된 game skills",
        "## 개발자 참고",
    ]

    positions = [text.index(heading) for heading in expected_headings]
    assert positions == sorted(positions)
    assert text.index("Superpowers") < text.index("## Quick Start")
    assert text.index("게임 개발에는") < text.index("## Quick Start")


def test_english_readme_matches_korean_structure():
    text = ENGLISH_README.read_text(encoding="utf-8")

    expected_headings = [
        "## Why this exists",
        "## How it helps",
        "## Quick Start",
        "## What gets installed",
        "## How to use it",
        "## Unity/Unreal MCP and safety rules",
        "## Living Docs",
        "## Included game skills",
        "## Developer notes",
    ]

    positions = [text.index(heading) for heading in expected_headings]
    assert positions == sorted(positions)
    assert text.index("Superpowers") < text.index("## Quick Start")
    assert text.index("game development") < text.index("## Quick Start")


def test_readmes_explain_living_docs_and_game_workflow_activation():
    for readme in [KOREAN_README, ENGLISH_README]:
        text = readme.read_text(encoding="utf-8")

        assert "docs/game" in text
        assert "living docs" in text.lower()
        assert "brainstorming" in text
        assert "implementation" in text
        assert "verification" in text


def test_readmes_document_compact_docs_payload_and_unity_mcp_handoff():
    readme = KOREAN_README.read_text(encoding="utf-8")
    readme_en = ENGLISH_README.read_text(encoding="utf-8")

    for text in (readme, readme_en):
        for doc_name in [
            "00-index.md",
            "01-product-brief.md",
            "02-gameplay-design.md",
            "03-content-and-ux.md",
            "04-engine-architecture.md",
            "05-validation-release.md",
            "decision-log.md",
            "change-log.md",
        ]:
            assert doc_name in text
        assert "split criteria" in text
        assert "game-build-release-platforms" in text
        assert ".codex/skills/unity-mcp-skill/SKILL.md" in text
        assert "unity-mcp-orchestrator" in text
