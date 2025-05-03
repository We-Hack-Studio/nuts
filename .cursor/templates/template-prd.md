# 1. Title: {PRD for {project}}

<version>1.0.0</version>

## Status: { Draft | Approved }

## Intro

{ Short 1-2 paragraph describing the what and why of what the prd will achieve}

## Goals

{

- Clear project objectives
- Measurable outcomes
- Success criteria
- Key performance indicators (KPIs)
  }

## Features and Requirements

{

- Functional requirements
- Non-functional requirements
- User experience requirements
- Integration requirements
- Compliance requirements
  }

## Epic List

### Epic-1: Current PRD Epic (for example backend epic)

### Epic-2: Second Current PRD Epic (for example front end epic)

### Epic-N: Future Epic Enhancements (Beyond Scope of current PRD)

## Epic 1: Story List

<example>
- Story 1: NestJS Configuration
  Status: {''|'InProgress'|'Complete'}
  Requirements:
  - Install NestJS CLI Globally
  - Create a new NestJS project with the nestJS cli generator

- Story 2: Hacker News Retrieval API Route
  Status: {''|'InProgress'|'Complete'}
  Requirements:
  - Create API Route that returns a list of Hacker News TopPosts, Scrapped Article from the top posts, and a list of comments from the top posts
  - Route post body specifies the number of posts, articles, and comments to return
  - Create a command in package.json that I can use to call the API Route (route configured in env.local)
    </example>

## Technology Stack

{ Table listing choices for languages, libraries, infra, etc...}

  <example>
  | Technology | Description |
  | ------------ | ------------------------------------------------------------- |
  | Kubernetes | Container orchestration platform for microservices deployment |
  | Apache Kafka | Event streaming platform for real-time data ingestion |
  | TimescaleDB | Time-series database for sensor data storage |
  | Go | Primary language for data processing services |
  | GoRilla Mux | REST API Framework |
  | Python | Used for data analysis and ML services |
  </example>

## Reference

{ Mermaid Diagrams for models tables, visual aids as needed, citations and external urls }

## Data Models, API Specs, Schemas, etc...

{ As needed - may not be exhaustive - but key ideas that need to be retained and followed into the architecture and stories }

<example>
### Sensor Reading Schema

```json
{
  "sensor_id": "string",
  "timestamp": "datetime",
  "readings": {
    "temperature": "float",
    "pressure": "float",
    "humidity": "float"
  },
  "metadata": {
    "location": "string",
    "calibration_date": "datetime"
  }
}
```

</example>

## Project Structure

{ Diagram the folder and file organization structure along with descriptions }

<example>

````
// Start of Selection
```text
src/
├── services/
│   ├── gateway/        # Sensor data ingestion
│   ├── processor/      # Data processing and validation
│   ├── analytics/      # Data analysis and ML
│   └── notifier/       # Alert and notification system
├── deploy/
│   ├── kubernetes/     # K8s manifests
│   └── terraform/      # Infrastructure as Code
└── docs/
    ├── api/           # API documentation
    └── schemas/       # Data schemas
````

</example>

## Change Log

{ Markdown table of key changes after document is no longer in draft and is updated, table includes the change title, the story id that the change happened during, and a description if the title is not clear enough }

<example>
| Change               | Story ID | Description                                                   |
| -------------------- | -------- | ------------------------------------------------------------- |
| Initial draft        | N/A      | Initial draft prd                                             |
| Add ML Pipeline      | story-4  | Integration of machine learning prediction service story      |
| Kafka Upgrade        | story-6  | Upgraded from Kafka 2.0 to Kafka 3.0 for improved performance |
</example>
