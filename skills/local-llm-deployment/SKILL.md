---
name: local-llm-deployment
description: Deploiement LLM local, Ollama, LM Studio, quantization, GPU
author: PhoenixProject
version: 1.0.0
created: 2026-02-23
last_updated: 2026-02-23
---
# Local LLM Deployment

## Competences
- Ollama (install, serve, pull, run, API)
- LM Studio (GUI, server mode)
- Quantization (GGUF, GPTQ, AWQ, EXL2)
- GPU allocation (CUDA, Metal, ROCm)
- Model selection par tache (code, chat, vision)
- API proxy pour routage multi-modele
- Memory management (context window, KV cache)
- Batch inference

## Hardware
- Apple Silicon (M1/M2/M3/M4, Metal)
- NVIDIA GPU (CUDA, 8GB+ VRAM)
- CPU-only fallback (slower but works)
- Mini PC deployment (NUC, Mac Mini)

## Models recommandes
- Code : deepseek-coder, codellama, starcoder
- Chat : llama3, mistral, phi-3
- Vision : llava, bakllava
- Embeddings : nomic-embed-text
