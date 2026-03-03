---
name: kubernetes-operations
description: Deployments, Helm charts, HPA, troubleshooting
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---

# Kubernetes Operations

## Deployments

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  labels:
    app: myapp
spec:
  replicas: 3
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0
  selector:
    matchLabels:
      app: myapp
  template:
    metadata:
      labels:
        app: myapp
    spec:
      containers:
      - name: app
        image: myapp:1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "64Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 10
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 10
```

## HPA (Horizontal Pod Autoscaler)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Troubleshooting

```bash
# Pod ne demarre pas
kubectl describe pod <pod-name>
kubectl logs <pod-name> --previous

# CrashLoopBackOff
kubectl logs <pod-name> -f
kubectl exec -it <pod-name> -- /bin/sh

# Service inaccessible
kubectl get endpoints <service-name>
kubectl port-forward svc/<service-name> 8080:80
```

## Checklist production

- [ ] Resource requests et limits configures
- [ ] Health checks (liveness + readiness)
- [ ] PodDisruptionBudget configure
- [ ] Secrets dans des Secret objects (pas en clair)
- [ ] NetworkPolicy configuree
- [ ] HPA configure
- [ ] Monitoring et alerting
