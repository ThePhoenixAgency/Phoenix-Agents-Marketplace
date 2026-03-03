---
name: react-patterns
description: Hooks, Server Components, Suspense, Error Boundaries
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# React Patterns

## Custom Hooks

```typescript
function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);

  useEffect(() => {
    const handler = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
}
```

## Server Components (RSC)

```typescript
// server component (par defaut dans Next.js App Router)
async function UserList() {
  const users = await db.users.findMany();
  return (
    <ul>
      {users.map(user => <li key={user.id}>{user.name}</li>)}
    </ul>
  );
}

// client component (interactif)
'use client';
function SearchBar({ onSearch }: { onSearch: (q: string) => void }) {
  const [query, setQuery] = useState('');
  return <input value={query} onChange={e => setQuery(e.target.value)} />;
}
```

## Error Boundaries

```typescript
class ErrorBoundary extends React.Component<
  { children: React.ReactNode; fallback: React.ReactNode },
  { hasError: boolean }
> {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    logErrorToService(error, info.componentStack);
  }

  render() {
    if (this.state.hasError) return this.props.fallback;
    return this.props.children;
  }
}
```

## Suspense

```typescript
function App() {
  return (
    <ErrorBoundary fallback={<ErrorPage />}>
      <Suspense fallback={<LoadingSpinner />}>
        <UserProfile />
      </Suspense>
    </ErrorBoundary>
  );
}
```

## Anti-patterns

- Props drilling excessif (utiliser Context ou Zustand)
- useEffect pour la synchronisation de state (deriver plutot)
- State dans des refs quand il faut re-render
- Closures stale dans les handlers
