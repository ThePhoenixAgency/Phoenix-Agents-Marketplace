# Rules: Go
# Created: 2026-02-18

## Style
- gofmt obligatoire
- golangci-lint clean
- go vet clean

## Conventions
- Errors wrapping avec fmt.Errorf + %w
- Interfaces petites (1-3 methodes)
- Accept interfaces, return structs
- Context en premier parametre
- Table-driven tests
- internal/ pour le code prive
