---
name: game-input-and-camera-design
description: Use when changing player controls, input mapping, Unity Input System, Unreal Enhanced Input, camera behavior, camera states, aiming, lock-on, or control accessibility.
---

# Game Input and Camera Design

## Overview

Player controls와 camera behavior는 player verbs, UI prompts, accessibility, motion comfort에 직접 영향을 준다. Input mapping과 camera state를 같은 change surface로 본다.

## Workflow

1. Player verbs, input action mapping, rebinding, device switching, camera states를 정리한다.
2. Input latency, deadzone, invert axis, sensitivity, accessibility 영향을 확인한다.
3. Camera movement, aim, lock-on, obstruction, clipping, motion sickness risk를 함께 본다.
4. UI focus/navigation이나 prompts가 바뀌면 `game-ui-implementation`을 함께 사용한다.
5. 변경 후 `docs/game/02-gameplay-design.md` 갱신을 유도한다.

## Verification

- Keyboard/mouse, gamepad, touch 등 target input device별 smoke path를 확인한다.
- Camera clipping, target loss, obstruction handling, motion sickness risk, UI input conflict를 확인한다.
- Control changes가 tutorial, HUD prompt, localization key에 미치는 영향을 점검한다.
