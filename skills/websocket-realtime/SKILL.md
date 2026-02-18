---
name: websocket-realtime
description: Socket.io, SSE, reconnection, scaling
---
# WebSocket & Realtime
## Socket.io Server
```typescript
const io = new Server(httpServer, { cors: { origin: '*' } });
io.on('connection', (socket) => {
  socket.join(`user:${socket.handshake.auth.userId}`);
  socket.on('message', (data) => {
    io.to(`room:${data.roomId}`).emit('message', data);
  });
  socket.on('disconnect', () => { /* cleanup */ });
});
```
## SSE (Server-Sent Events)
```typescript
app.get('/events', (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');
  const interval = setInterval(() => {
    res.write(`data: ${JSON.stringify({ time: Date.now() })}\n\n`);
  }, 1000);
  req.on('close', () => clearInterval(interval));
});
```
## Reconnection
```typescript
const socket = io('https://server.com', {
  reconnection: true,
  reconnectionAttempts: 5,
  reconnectionDelay: 1000,
  reconnectionDelayMax: 10000,
});
```
