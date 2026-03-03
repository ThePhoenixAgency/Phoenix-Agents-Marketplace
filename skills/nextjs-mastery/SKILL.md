---
name: nextjs-mastery
description: App Router, RSC, ISR, Server Actions, Middleware
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Next.js Mastery
## App Router
Route = dossier dans app/. Layouts persistants, loading states, error boundaries natifs.
```
app/
  layout.tsx       -> Root layout (obligatoire)
  page.tsx         -> Route /
  loading.tsx      -> Loading UI automatique
  error.tsx        -> Error boundary automatique
  not-found.tsx    -> 404 custom
  dashboard/
    layout.tsx     -> Layout nested
    page.tsx       -> Route /dashboard
    [id]/
      page.tsx     -> Route /dashboard/:id
```
## Server Actions
```typescript
'use server';
async function createUser(formData: FormData) {
  const name = formData.get('name') as string;
  const user = await db.user.create({ data: { name } });
  revalidatePath('/users');
  return user;
}
```
## ISR
```typescript
export const revalidate = 3600; // revalider toutes les heures
async function Page() {
  const data = await fetch('https://api.example.com/data');
  return <div>{data}</div>;
}
```
## Middleware
```typescript
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
export function middleware(request: NextRequest) {
  const token = request.cookies.get('token');
  if (!token && request.nextUrl.pathname.startsWith('/dashboard')) {
    return NextResponse.redirect(new URL('/login', request.url));
  }
  return NextResponse.next();
}
export const config = { matcher: ['/dashboard/:path*'] };
```
