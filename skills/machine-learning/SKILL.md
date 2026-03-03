---
name: machine-learning
description: Pipelines ML, training, evaluation, deploiement
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Machine Learning
## Pipeline
```
1. Data Collection -> Extract, clean, validate
2. Feature Engineering -> Transform, encode, normalize
3. Model Selection -> Baseline, experiment, compare
4. Training -> Train/val/test split, cross-validation
5. Evaluation -> Metrics (accuracy, F1, AUC, RMSE)
6. Deployment -> Model serving, monitoring, A/B testing
7. Monitoring -> Data drift, model drift, retraining
```
## Evaluation Metrics
| Tache | Metriques |
|-------|-----------|
| Classification | Accuracy, Precision, Recall, F1, AUC-ROC |
| Regression | MSE, RMSE, MAE, R-squared |
| Ranking | NDCG, MAP, MRR |
| Clustering | Silhouette, Davies-Bouldin |
## Anti-patterns
- Pas de baseline simple avant modele complexe
- Data leakage (features du futur dans le training)
- Evaluer sur le training set
- Ignorer le desequilibre des classes
- Deployer sans monitoring de drift
