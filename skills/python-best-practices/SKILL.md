---
name: python-best-practices
description: Type hints, dataclasses, async/await, packaging
---
# Python Best Practices
## Type Hints
```python
from typing import Optional
def process_user(user_id: int, name: str, email: Optional[str] = None) -> dict[str, str]:
    return {"id": str(user_id), "name": name, "email": email or ""}
```
## Dataclasses
```python
from dataclasses import dataclass, field
@dataclass(frozen=True)
class User:
    id: int
    name: str
    email: str
    roles: list[str] = field(default_factory=list)
```
## Async/Await
```python
import asyncio
import httpx
async def fetch_users() -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.example.com/users")
        response.raise_for_status()
        return response.json()
```
## Project Layout
```
src/
  mypackage/
    __init__.py
    core/
    models/
    services/
tests/
  test_core.py
  test_models.py
pyproject.toml
```
