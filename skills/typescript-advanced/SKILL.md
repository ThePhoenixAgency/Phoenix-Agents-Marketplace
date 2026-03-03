---
name: typescript-advanced
description: Generics, conditional types, mapped types, discriminated unions
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# TypeScript Advanced
## Generics
```typescript
function createRepository<T extends { id: string }>(items: T[]) {
  return {
    findById: (id: string): T | undefined => items.find(i => i.id === id),
    findAll: (): T[] => [...items],
    add: (item: T): void => { items.push(item); },
  };
}
```
## Conditional Types
```typescript
type ApiResponse<T> = T extends Array<infer U>
  ? { data: U[]; total: number }
  : { data: T };
type IsString<T> = T extends string ? true : false;
```
## Mapped Types
```typescript
type Readonly<T> = { readonly [K in keyof T]: T[K] };
type Optional<T> = { [K in keyof T]?: T[K] };
type Nullable<T> = { [K in keyof T]: T[K] | null };
```
## Discriminated Unions
```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };
function handleResult<T>(result: Result<T>) {
  if (result.success) {
    console.log(result.data); // TypeScript sait que c'est T
  } else {
    console.error(result.error); // TypeScript sait que c'est Error
  }
}
```
## Template Literal Types
```typescript
type HTTPMethod = 'GET' | 'POST' | 'PUT' | 'DELETE';
type Route = `/${string}`;
type Endpoint = `${HTTPMethod} ${Route}`;
```
