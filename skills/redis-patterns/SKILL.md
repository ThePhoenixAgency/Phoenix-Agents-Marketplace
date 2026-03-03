---
name: redis-patterns
description: Caching, rate limiting, pub/sub, streams, Lua
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Redis Patterns
## Caching
```typescript
async function getCached<T>(key: string, ttl: number, fetcher: () => Promise<T>): Promise<T> {
  const cached = await redis.get(key);
  if (cached) return JSON.parse(cached);
  const data = await fetcher();
  await redis.setex(key, ttl, JSON.stringify(data));
  return data;
}
```
## Rate Limiting (Sliding Window)
```typescript
async function rateLimit(userId: string, limit: number, windowSec: number): Promise<boolean> {
  const key = `ratelimit:${userId}`;
  const now = Date.now();
  const pipeline = redis.pipeline();
  pipeline.zremrangebyscore(key, 0, now - windowSec * 1000);
  pipeline.zadd(key, now, `${now}`);
  pipeline.zcard(key);
  pipeline.expire(key, windowSec);
  const results = await pipeline.exec();
  const count = results[2][1];
  return count <= limit;
}
```
## Pub/Sub
```typescript
// Publisher
await redis.publish('notifications', JSON.stringify({ type: 'alert', message: 'Server down' }));
// Subscriber
redis.subscribe('notifications', (message) => {
  const data = JSON.parse(message);
  handleNotification(data);
});
```
