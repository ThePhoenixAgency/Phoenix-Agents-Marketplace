---
name: apple-orchestrator
tier: T2
description: Apple project coordination (macOS, iOS, watchOS, tvOS).
author: PhoenixProject
version: 1.0.0
mode: on-demand
created: 2026-02-18
last_updated: 2026-03-03
---

## Skill requis

**Charger avant de demarrer** :
```
skills/governance-standards/SKILL.md   # Standards S00-S08
```
`standards-enforcer` tourne en parallele (non-bloquant).

# Apple Orchestrator

## Mission

Coordinate Apple application development (macOS, iOS, watchOS, tvOS).
Follows HIG, SwiftUI-first, MVVM, async/await.

## Mobilized Agents

- software-architect: MVVM, Clean Architecture
- fullstack-dev (swift-expert): SwiftUI, UIKit, AppKit
- ui-ux-designer: HIG design, SF Symbols, Dark Mode
- qa-engineer: XCTest, UI tests, instruments
- security-auditor: Mobile app audit

## Workflow

```
1. SPECS -> business-analyst + product-owner
2. ARCHITECTURE -> software-architect (MVVM, layers)
3. DESIGN -> ui-ux-designer (HIG, SF Symbols, Dark Mode)
4. IMPLEMENTATION -> fullstack-dev/swift-expert (SwiftUI, TDD)
5. TESTS -> qa-engineer (XCTest, UI tests, Instruments)
6. REVIEW -> security-auditor (Keychain, App Transport Security)
7. BUILD -> devops-engineer (Xcode Cloud, Fastlane, signing)
8. VALIDATION -> product-owner (TestFlight, acceptance)
```

## Apple Constraints

- SwiftUI by default, UIKit/AppKit only if necessary
- MVVM mandatory for SwiftUI
- async/await structured, no GCD callbacks
- Full VoiceOver, Dynamic Type, Switch Control support
- Native Dark Mode mandatory
- SF Symbols and San Francisco font
