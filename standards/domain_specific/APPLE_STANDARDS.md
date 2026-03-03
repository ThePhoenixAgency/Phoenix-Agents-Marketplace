---
version: 1.0.1
last_updated: 2026-02-04
author: PhoenixProject
status: Stable
---

# STANDARDS APPLE (macOS & iOS)

## PROTOCOLE D'EXÉCUTION OBLIGATOIRE
1.  **START** : Lire `docs/BACKLOG.md` et les Standards de Gouvernance.
2.  **PROCESS** : Appliquer les règles sans déviation.
3.  **END** : Mettre à jour `docs/BACKLOG.md` et `docs/CHANGELOG.md` avant tout commit.

Ce document définit les règles spécifiques à respecter lors du développement d'applications pour l'écosystème Apple, afin de garantir une intégration parfaite et le respect des Human Interface Guidelines (HIG).

## 1. DESIGN ET INTERFACES (HIG)
- **Esthétique Native** : Utilisation des composants système standards.
- **Réactivité** : Fluidité des animations et respect des fréquences de rafraîchissement.
- **Adaptabilité** : Support du Mode Sombre (Dark Mode) et des tailles d'écran dynamiques (SF Symbols).

## 2. ÉCOSYSTÈME TECHNIQUE
- **Swift/SwiftUI** : Prioriser les technologies déclaratives modernes d'Apple.
- **Gestion Mémoire** : Optimisation stricte de l'usage mémoire et de la batterie.
- **Sandboxing** : Respect des contraintes de sécurité d'Apple (Permissions, Entitlements).

## 3. ACCESSIBILITÉ APPLE
- **VoiceOver** : Support complet pour les lecteurs d'écran.
- **Dynamic Type** : Respect des préférences de taille de texte de l'utilisateur.
- **Contraste** : Utilisation des palettes de couleurs système pour un contraste optimal.

## 4. DÉPLOIEMENT
- **App Store Ready** : Préparation des métadonnées et respect des consignes de révision.
- **Signatures** : Gestion correcte des profils de provisionnement et des certificats de signature.
