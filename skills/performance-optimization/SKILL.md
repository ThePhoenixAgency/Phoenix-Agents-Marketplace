---
name: performance-optimization
description: Code splitting, image optimization, Core Web Vitals
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Performance Optimization
## Core Web Vitals Targets
| Metrique | Bon | A ameliorer | Mauvais |
|----------|-----|-------------|---------|
| LCP | < 2.5s | 2.5-4s | > 4s |
| FID/INP | < 100ms | 100-300ms | > 300ms |
| CLS | < 0.1 | 0.1-0.25 | > 0.25 |
## Code Splitting
```typescript
const Dashboard = lazy(() => import('./pages/Dashboard'));
function App() {
  return (
    <Suspense fallback={<Spinner />}>
      <Routes>
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Suspense>
  );
}
```
## Image Optimization
```html
<picture>
  <source srcset="image.avif" type="image/avif" />
  <source srcset="image.webp" type="image/webp" />
  <img src="image.jpg" alt="Description" loading="lazy" decoding="async"
       width="800" height="600" />
</picture>
```
## Checklist Lighthouse > 90
- [ ] Code splitting par route
- [ ] Images optimisees (WebP/AVIF, lazy loading, dimensions)
- [ ] Font preloading, font-display: swap
- [ ] Critical CSS inline
- [ ] Gzip/Brotli compression
- [ ] Cache-Control headers
- [ ] Prefetch routes probables
- [ ] Service Worker pour cache offline
