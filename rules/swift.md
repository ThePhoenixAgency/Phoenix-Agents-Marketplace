# Rules: Swift
# Created: 2026-02-18

## Style
- SwiftLint strict
- SwiftFormat obligatoire

## Conventions
- SwiftUI + MVVM
- struct par defaut, class si reference semantics
- guard let pour les sorties anticipees
- @Observable pour les ViewModels (Swift 5.9+)
- async/await structure, pas de callbacks
- [weak self] dans les closures qui capturent self
- Extensions pour les conformites protocoles
- SF Symbols pour les icones
- Dark Mode natif obligatoire
- Accessibilite: VoiceOver labels, Dynamic Type
