---
name: monitoring-observability
description: OpenTelemetry, Prometheus, structured logging
---
# Monitoring & Observability
## Les 3 piliers
### Metrics (Prometheus)
```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'app'
    scrape_interval: 15s
    static_configs:
      - targets: ['app:3000']
```
### Logs (structured)
```typescript
logger.info('User login', {
  userId: user.id,
  ip: req.ip,
  userAgent: req.headers['user-agent'],
  timestamp: new Date().toISOString(),
  traceId: span.traceId,
});
// [INTERDIT] logger.info("User " + user.id + " logged in from " + req.ip);
```
### Traces (OpenTelemetry)
```typescript
const tracer = trace.getTracer('app');
async function handleRequest(req) {
  return tracer.startActiveSpan('handleRequest', async (span) => {
    span.setAttribute('http.method', req.method);
    span.setAttribute('http.url', req.url);
    try {
      const result = await processRequest(req);
      span.setStatus({ code: SpanStatusCode.OK });
      return result;
    } catch (error) {
      span.setStatus({ code: SpanStatusCode.ERROR, message: error.message });
      throw error;
    } finally {
      span.end();
    }
  });
}
```
## Alerting rules
```yaml
groups:
- name: app-alerts
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "Error rate > 5% for 5 minutes"
```
