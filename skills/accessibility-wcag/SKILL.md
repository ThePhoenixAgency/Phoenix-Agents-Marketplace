---
name: accessibility-wcag
description: ARIA, keyboard navigation, contraste, WCAG 2.2 AAA
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Accessibility (WCAG 2.2 AAA)
## Regles obligatoires
- Navigation clavier complete (Tab, Shift+Tab, Enter, Escape, Arrows)
- Hierarchie semantique correcte (un seul H1, H2-H6 ordonnes)
- Labels sur tous les champs de formulaire
- Alt text sur toutes les images
- Contraste suffisant (AAA: 7:1 texte normal, 4.5:1 texte large)
- Focus visible sur tous les elements interactifs
- Annonces dynamiques via aria-live
## ARIA patterns
```html
<!-- Bouton avec etat -->
<button aria-pressed="false" aria-label="Ajouter aux favoris">Favoris</button>
<!-- Dialog modal -->
<div role="dialog" aria-modal="true" aria-labelledby="dialog-title">
  <h2 id="dialog-title">Confirmation</h2>
  <p>Etes-vous sur ?</p>
  <button autofocus>Confirmer</button>
  <button>Annuler</button>
</div>
<!-- Live region -->
<div aria-live="polite" aria-atomic="true">
  3 resultats trouves
</div>
```
## Checklist
- [ ] Navigation clavier sans souris
- [ ] VoiceOver/NVDA lisible
- [ ] Contraste AAA verifie
- [ ] Focus trap dans les modals
- [ ] Skip links en haut de page
- [ ] Responsive zoom 200%
- [ ] Texte redimensionnable (Dynamic Type)
- [ ] Pas de contenu uniquement visuel
