---
name: golang-idioms
description: Error handling, interfaces, concurrency, project layout
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Go Idioms
## Error Handling
```go
func fetchUser(id string) (*User, error) {
    user, err := db.FindByID(id)
    if err != nil {
        return nil, fmt.Errorf("fetchUser(%s): %w", id, err)
    }
    return user, nil
}
```
## Interfaces
```go
type Repository interface {
    FindByID(id string) (*Entity, error)
    Save(entity *Entity) error
    Delete(id string) error
}
// Accepter des interfaces, retourner des structs
func NewService(repo Repository) *Service {
    return &Service{repo: repo}
}
```
## Concurrency
```go
func processItems(items []Item) []Result {
    results := make([]Result, len(items))
    var wg sync.WaitGroup
    for i, item := range items {
        wg.Add(1)
        go func(i int, item Item) {
            defer wg.Done()
            results[i] = process(item)
        }(i, item)
    }
    wg.Wait()
    return results
}
```
## Project Layout
```
cmd/myapp/main.go
internal/
  service/
  repository/
  handler/
pkg/
  utils/
go.mod
go.sum
```
