---
name: rust-systems
description: Ownership, traits, async, error handling
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Rust Systems
## Ownership
```rust
fn process_data(data: String) -> String {
    // data est owned par cette fonction
    format!("Processed: {}", data)
    // data est drop ici
}
fn borrow_data(data: &str) -> usize {
    // emprunt immutable, data n'est pas consomme
    data.len()
}
```
## Traits
```rust
trait Repository {
    fn find_by_id(&self, id: &str) -> Result<Entity, AppError>;
    fn save(&self, entity: &Entity) -> Result<(), AppError>;
}
impl Repository for PostgresRepo {
    fn find_by_id(&self, id: &str) -> Result<Entity, AppError> {
        // implementation
    }
    fn save(&self, entity: &Entity) -> Result<(), AppError> {
        // implementation
    }
}
```
## Error Handling
```rust
use thiserror::Error;
#[derive(Error, Debug)]
enum AppError {
    #[error("Not found: {0}")]
    NotFound(String),
    #[error("Database error: {0}")]
    Database(#[from] sqlx::Error),
    #[error("IO error: {0}")]
    Io(#[from] std::io::Error),
}
```
## Async
```rust
async fn fetch_data(url: &str) -> Result<String, reqwest::Error> {
    let response = reqwest::get(url).await?;
    let body = response.text().await?;
    Ok(body)
}
```
