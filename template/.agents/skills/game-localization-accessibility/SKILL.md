---
name: game-localization-accessibility
description: Use when changing localization keys, translated text, font fallback, subtitles, readability, colorblind support, input accessibility, safe areas, or platform accessibility requirements.
---

# Game Localization Accessibility

## Overview

Localization과 accessibility는 UI, input, platform release constraints에 걸쳐 있다. Text expansion, fallback fonts, subtitles, readability, safe areas, controller-only navigation을 함께 본다.

## Workflow

1. Text key, font fallback, text expansion, subtitle, color/readability, safe area, remapping 영향을 확인한다.
2. UI implementation과 input/camera design의 accessibility 영향을 연결한다.
3. Platform accessibility requirement는 `docs/game/12-build-release-platforms.md`와 연결한다.
4. 변경 후 `docs/game/06-ui-ux-flow.md`, `docs/game/03-player-and-controls.md`, `docs/game/12-build-release-platforms.md` 갱신 여부를 판단한다.

## Verification

- Long text, missing key, fallback font, RTL 또는 CJK 표시 위험을 확인한다.
- Color-only signal, contrast, subtitle timing, controller-only navigation을 확인한다.
- Accessibility requirement를 target platform과 연결해 기록한다.
- 실제 platform certification은 이 spec 범위 밖이지만, known requirement와 gap은 문서화한다.
