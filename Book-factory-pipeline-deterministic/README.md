# Book Factory Pipeline (Deterministic)

## Overview

Book Factory Pipeline is a deterministic, contract-driven book generation system.
It generates structured multi-chapter books from a validated JSON input and produces reproducible artifacts in a timestamped output directory.

This version does not use external LLMs. All generation logic is rule-based and deterministic.

The project demonstrates structured pipeline orchestration, schema validation, formatting enforcement, and artifact management.


## Architecture

Execution flow:

- CLI
    → PipelineController.run_all()
    → OutlinePlannerAgent
    → ChapterWriterAgent (per chapter loop)
    → Schema Validation
    → Format Guard
    → Markdown Rendering
    → Book Assembly
    → Manifest + Run Report

There is a single public entrypoint (run_all).
Internally, the controller separates planning and writing stages to preserve clarity and testability.


## Core Components

- PipelineController
    Orchestrates execution, manages run directory, coordinates stages.

- OutlinePlannerAgent
    Generates a structured outline from the validated book input.

- ChapterWriterAgent
    Generates structured chapter JSON objects using deterministic logic.

- SchemaValidator
    Validates input, outline, and chapter structures against JSON schemas.

- Format Guard
    Ensures paragraphs respect formatting constraints and forbidden tokens.

- Markdown Renderer
    Converts structured chapter JSON into markdown format.

- Book Assembler
    Combines chapter markdown files into a full book.

- Manifest Builder
    Creates metadata describing the run for traceability.


## Execution Model

The system uses a deterministic content engine.

### Characteristics:

        - Template-driven structure
        - Tone-sensitive adjustments
        - Structured sections (Setup → Twist → Close)
        - Controlled variation logic
        - No stochastic behavior
        - This guarantees:
        - Reproducibility
        - Schema compliance
        - Stable formatting
        - No external API dependencies


## Input Contract

The system expects a structured input_book.json file containing:

- book_id
- title
- topic
- content_brief
- target_audience
- book_type
- tone_profile
- chapter_count

### Constraints

    All inputs are validated against JSON schemas before execution.


## Output Structure

Each run creates a timestamped directory:

outputs/<book_id>_<timestamp>/

### Contents:

    - input_book.json (copy of input)
    - outline.json
    - chapters/
        - ch1.json
        - ch1.md
        - ch2.jsonc
        - ch2.md
    ...
    - book_full.md
    - manifest.json
    - run_report.json

This structure ensures traceability and reproducibility of each generation.

## How to Run

From project root:

$env:PYTHONPATH="$PWD\src"
python -m book_factory.cli examples/input_book.json


The system prints the path of the generated run directory.


## Design Decisions

- Single public command
    The CLI exposes only one entrypoint to simplify user experience and reduce ambiguity.

- Internal stage separation
    Planning and writing stages are kept internally to maintain separation of concerns and enable future extensibility.

- Deterministic first approach
    The system prioritizes architectural clarity and reproducibility before introducing probabilistic generation.

- Strict validation
    Schema validation and formatting guards prevent malformed content from propagating downstream.


## Scope and Limitations

This version is deterministic. It does not:

    - Call external language models
    - Learn from previous runs
    - Perform semantic reasoning
    - Adapt dynamically beyond rule-based variation
    - The focus is structural integrity and system design, not creative generation depth.


## Future Direction

Potential future extensions include:

    - Optional LLM-backed generation layer
    - Hybrid deterministic + generative mode
    - Cross-chapter state memory
    - Human-in-the-loop editing interface
    - Pluggable content engines

The current architecture allows these features to be added without restructuring the pipeline.