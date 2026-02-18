---
name: cloud-patterns
description: Lambda, DynamoDB, CDK, S3, services manages
---
# Cloud Patterns
## Serverless (Lambda)
```typescript
export const handler = async (event: APIGatewayEvent) => {
  try {
    const body = JSON.parse(event.body || '{}');
    const result = await processRequest(body);
    return { statusCode: 200, body: JSON.stringify(result) };
  } catch (error) {
    return { statusCode: 500, body: JSON.stringify({ error: 'Internal error' }) };
  }
};
```
## Infrastructure as Code (CDK)
```typescript
const api = new apigateway.RestApi(this, 'Api');
const handler = new lambda.Function(this, 'Handler', {
  runtime: lambda.Runtime.NODEJS_20_X,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda'),
  timeout: Duration.seconds(30),
  memorySize: 256,
});
api.root.addResource('users').addMethod('GET', new apigateway.LambdaIntegration(handler));
```
## Patterns
| Pattern | Usage |
|---------|-------|
| Fan-out | SQS -> Lambda -> traitement parallele |
| CQRS | Read model separe du write model |
| Event Sourcing | Stocker les events, pas l'etat |
| Circuit Breaker | Proteger contre les cascades d'echecs |
