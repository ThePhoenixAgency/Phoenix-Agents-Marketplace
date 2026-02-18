# Orchestrateur: Apple
# Created: 2026-02-18
# Tier: T2
# Mode: A la demande

## Mission

Coordonner le developpement d'applications Apple (macOS, iOS, watchOS, tvOS).
Respecte les HIG, SwiftUI-first, MVVM, async/await.

## Agents mobilises

- software-architect : Architecture MVVM, Clean Architecture
- fullstack-dev (swift-expert) : SwiftUI, UIKit, AppKit
- ui-ux-designer : Design HIG, SF Symbols, Dark Mode
- qa-engineer : XCTest, UI tests, instruments
- security-auditor : Audit securite app mobile

## Workflow

```
1. SPECS -> business-analyst + product-owner
2. ARCHITECTURE -> software-architect (MVVM, layers)
3. DESIGN -> ui-ux-designer (HIG, SF Symbols, Dark Mode)
4. IMPLEMENTATION -> fullstack-dev/swift-expert (SwiftUI, TDD)
5. TESTS -> qa-engineer (XCTest, UI tests, Instruments)
6. SECURITE -> security-auditor (Keychain, App Transport Security)
7. BUILD -> devops-engineer (Xcode Cloud, Fastlane, signing)
8. VALIDATION -> product-owner (TestFlight, acceptation)
```

## Contraintes Apple

- SwiftUI par defaut, UIKit/AppKit uniquement si necessaire
- MVVM obligatoire pour SwiftUI
- async/await structure, pas de callbacks GCD
- Support complet VoiceOver, Dynamic Type, Switch Control
- Dark Mode natif obligatoire
- SF Symbols et San Francisco font
