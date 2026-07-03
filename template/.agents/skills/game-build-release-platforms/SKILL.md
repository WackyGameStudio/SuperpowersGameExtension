---
name: game-build-release-platforms
description: Use when changing build scenes/maps, packaging, platform targets, CI build scripts, store submission, release checklist, platform-specific configuration, or certification constraints.
---

# Game Build Release Platforms

## Overview

Build/release work changes how the game is packaged, validated, and delivered. Treat build target, platform constraints, content inclusion, versioning, and release evidence as one surface.

## Workflow

1. Identify target engine, target platform, build configuration, and distribution path.
2. Check build scenes/maps/content inclusion.
3. Check platform-specific input, rendering, save path, networking, localization, accessibility, and performance constraints.
4. Verify whether CI/build scripts, project settings, packaging config, or store metadata changed.
5. Update `docs/game/05-validation-release.md` or an expanded `platform/build-release.md`.

## Verification

- Build command/configuration is recorded.
- Included scenes/maps/content are verified.
- Platform-specific blockers and unverified certification gaps are documented.
- Build output path/version/build number are recorded when available.
- If a build cannot be run, final response states why and what risk remains.
