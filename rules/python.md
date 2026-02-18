# Rules: Python
# Created: 2026-02-18

## Style
- PEP 8 strict
- Type hints sur toutes les fonctions publiques
- Docstrings Google style
- Black pour le formatting
- isort pour les imports

## Conventions
- dataclasses ou pydantic pour les modeles
- pathlib au lieu de os.path
- f-strings au lieu de .format()
- enumerate() au lieu de range(len())
- Comprehensions raisonnables (pas de one-liners illisibles)
