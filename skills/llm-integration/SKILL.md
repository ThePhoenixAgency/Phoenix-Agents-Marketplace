---
name: llm-integration
description: Streaming, function calling, RAG, cost optimization
---
# LLM Integration
## Streaming
```typescript
async function* streamCompletion(prompt: string) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, stream: true }),
  });
  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    yield decoder.decode(value, { stream: true });
  }
}
```
## Function Calling
```typescript
const tools = [{
  type: 'function',
  function: {
    name: 'get_weather',
    description: 'Get current weather for a location',
    parameters: {
      type: 'object',
      properties: {
        location: { type: 'string' },
        unit: { type: 'string', enum: ['celsius', 'fahrenheit'] },
      },
      required: ['location'],
    },
  },
}];
```
## RAG (Retrieval Augmented Generation)
```
1. INDEXATION : Documents -> Chunks -> Embeddings -> Vector DB
2. RECHERCHE : Query -> Embedding -> Similarity search -> Top K chunks
3. GENERATION : System prompt + Chunks + User query -> LLM -> Response
```
## Cost Optimization
| Technique | Impact |
|-----------|--------|
| Prompt caching | -40-60% tokens |
| Context compression | -20-30% tokens |
| Model routing (T1/T2/T3) | -50-80% cout |
| Batch requests | -30% latence |
| Streaming | UX meilleure, meme cout |
