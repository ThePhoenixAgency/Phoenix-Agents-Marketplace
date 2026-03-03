---
name: data-engineering
description: ETL pipelines, Spark, star schema, qualite donnees
author: PhoenixProject
version: 1.0.0
created: 2026-02-18
last_updated: 2026-02-23
---
# Data Engineering
## ETL Pipeline
```python
def extract(source: str) -> pd.DataFrame:
    return pd.read_csv(source)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(subset=['email'])
    df['email'] = df['email'].str.lower().str.strip()
    df['created_at'] = pd.to_datetime(df['created_at'])
    return df

def load(df: pd.DataFrame, target: str):
    engine = create_engine(target)
    df.to_sql('users', engine, if_exists='append', index=False)
```
## Star Schema
```
Fact Table: sales
  - sale_id, date_id, product_id, customer_id, amount, quantity
Dimension Tables:
  - dim_date: date_id, year, month, day
  - dim_product: product_id, name, category
  - dim_customer: customer_id, name, segment
```
## Data Quality
```
REGLES :
- Completude : pas de NULL sur les champs obligatoires
- Unicite : pas de doublons sur les cles
- Coherence : formats uniformes (dates, emails)
- Fraicheur : donnees a jour (SLA de latence)
```
