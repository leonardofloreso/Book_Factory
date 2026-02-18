# Book Factory

Book Factory is a modular book-generation system designed to produce structured, validated, and reproducible narrative content through deterministic and LLM-based pipelines.

This repository contains multiple pipeline implementations under a single architecture.

## Repository Structure

Book_Factory/
- Book-factory-pipeline-deterministic/  
  Deterministic narrative engine (template-driven, schema-validated)
- gemini/  
  (Planned) LLM-based pipeline using Google ADK

## Current Version

The deterministic pipeline is the active production version.

It provides:

- Structured outline generation
- Deterministic chapter generation
- JSON schema validation
- Paragraph formatting guards
- Markdown rendering
- Book assembly
- Manifest and run reporting

No external LLM dependency is required.

## Design Principles

- Deterministic and reproducible outputs
- Strict schema contracts
- Separation of orchestration and narrative engine
- Clean artifact generation
- Extensible architecture for future LLM integration

## Future Direction

A second pipeline implementation based on Gemini (Google ADK) will be developed under the same repository to demonstrate LLM-based generation while preserving architectural separation.

---

Author: Leonardo Flor  
Status: Active Development
