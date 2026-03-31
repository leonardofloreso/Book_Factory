# Book Factory

A modular Python pipeline for generating structured, validated, and 
reproducible book and audiobook content — from outline to audio output.

![Status](https://img.shields.io/badge/status-active%20development-brightgreen)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)

---

## Why this exists

Creating books and audiobooks manually requires coordinating writing, 
formatting, narration, audio chunking, and platform constraints at every 
stage. Book Factory replaces that ad-hoc process with a repeatable, 
schema-validated pipeline that produces consistent outputs on every run.

---

## Pipeline overview
```
Outline → Chapter Generation → JSON Validation → 
Markdown Rendering → Audio Chunking → Book Assembly → Manifest Report
```

---

## Repository structure
```
Book_Factory/
├── Book-factory-pipeline-deterministic/   # Active production version
│   └── Template-driven, schema-validated narrative engine
├── gemini/                                # In development
│   └── LLM-based pipeline using Google ADK + Gemini
├── docs/
└── README.md
```

---

## Current version — Deterministic pipeline

No external LLM dependency required.

| Feature | Description |
|---|---|
| Outline generation | Structured chapter-level planning |
| Chapter generation | Deterministic, template-driven content |
| JSON schema validation | Enforced output contracts at every stage |
| Paragraph formatting guards | Consistency across long-form content |
| Markdown rendering | Clean text output for ebook formatting |
| Book assembly | Full manuscript from modular chapters |
| Manifest + run reporting | Traceability and reproducibility per run |

---

## Design principles

- Deterministic and reproducible outputs
- Strict schema contracts between pipeline stages
- Separation of orchestration and narrative engine
- Clean artifact generation
- Extensible architecture for future LLM integration

---

## In development — Gemini pipeline

A second pipeline using Google ADK and Gemini will be added to the same 
repository, demonstrating LLM-based generation while preserving the same 
architectural separation and schema contracts.

---

## Tools

Python · JSON Schema · Markdown · ElevenLabs · Google ADK (planned) · 
Amazon KDP (target platform)

---

**Author:** Leonardo Flores  
**Status:** Active Development  
**Contact:** [LinkedIn](https://www.linkedin.com/in/tu-perfil)
