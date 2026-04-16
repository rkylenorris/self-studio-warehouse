# Project Overview: Self-Studio-Warehouse

## 1. Executive Summary

Self-Studio-Warehouse is a modular, personal health data ecosystem designed to bridge the gap between clinical data analysis and creative self-expression. By consolidating disparate data streams�subjective (mood tracking via Daylio), objective (biometrics via Fitbit), and clinical (symptom/medication monitoring via Human)�the project empowers the user to explore their health dimensions through two distinct lenses: an Analytical Dashboard for healthcare providers and a Creative Studio for artistic sonification and visualization.

## 2. Core Architecture: The Data Warehouse

The foundation is a Medallion Architecture built on PostgreSQL (hosted via rootless Podman containers). This ensures data integrity, domain isolation, and scalability.

### Data Schemas

mind (Daylio): Subjective mood, activities, and custom scales (Energy, Anxiety, Focus).

body (Fitbit): Objective biometrics including sleep stages, heart rate variability (HRV), and activity levels.

clinical (Human App/Manual): Medication logs, specific symptom tracking, and provider access logs.

### The "Adaptive" ETL Pipeline

Bronze (Raw): Preserves immutable JSON/CSV extracts with schema-drift detection.

Silver (Standardized): Employs Pydantic models for validation and an Entity-Attribute-Value (EAV) pattern to ingest new data dimensions (like new Daylio scales) without manual database migrations.

Gold (Curated): Pre-aggregated views optimized for the Dashboard and Studio engines.

## 3. The Analytics Dashboard

The dashboard serves as a secure interface for clinical collaboration, providing high-fidelity data visualizations tailored to specific medical contexts.

### The User Controller (Admin View)

Access Management: Invite and authorize specific providers (Therapist, Psychiatrist, GP).

Granular Permissions: Designate exactly which data "dimensions" each provider can see (e.g., the Psychiatrist sees Medication and Mood; the GP sees Sleep and Bio-data).

Context Injection: Allows the user to add clarifying notes to specific data trends to provide a narrative for the analytics.

### Provider-Specific Dashes

Isolation Protocol: Providers operate in "silos." No provider has knowledge of the existence or data access of another unless explicitly authorized by the user.

Clinical Communication: A built-in messaging system. To ensure transparency, any communication between providers must include the user.

Specialized Views: * Psychiatry: Focuses on "Mixed State" indicators (High Energy + Low Mood) and medication efficacy.

Therapy: Focuses on activity/tag correlations and behavioral habit loops.

## 4. The Studio: Artistic Sonification & Visualization

The Studio transforms raw data into an immersive aesthetic experience, allowing the user to "feel" their data patterns through sound and art.

### Music & Sonification

The Musical Matrix: Data dimensions are mapped to MIDI parameters.

Mood: Controls pitch and scale (e.g., Pentatonic Major for high mood, Diminished for low).

Energy Scale: Controls Tempo (BPM).

Anxiety/Stress: Controls dissonance and harmonic complexity.

Sleep Quality: Controls velocity and "brightness" of the timbre.

Mixing Engine: Users can select specific timeframes (e.g., "The January Depression" or "The Spring Coding Sprint") to generate unique compositions.

### Abstract Visualizations

Generative Art: Visual representations of health dimensions using the same data logic.

Temporal "Mixing": Overlaying multiple timeframes to see (and hear) how personal growth or seasonal changes alter the "shape" of the data.

## 5. Technical Stack & Philosophy

Language: Python 3.12+ (managed via uv).

Database: PostgreSQL (Rootless Podman container).

Infrastructure: Modular, containerized, and local-first to ensure privacy.

License: MIT (to encourage open-source community contributions to ingestors and artistic modules).

Privacy Philosophy: The user is the sole proprietor of the data. All clinical sharing is opt-in, time-bound, and strictly monitored.

## 6. Implementation Phases

Phase 1 (Data Pipeline): Building the Bronze/Silver/Gold ETL, Postgres schema, and schema-drift alerting system.

Phase 2 (The Dashboard): Developing the User Controller and secure Provider Views.

Phase 3 (The Studio): Implementing the MIDI generation engine and visualization layers.
