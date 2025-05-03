# {Epic-N} - {Story-#}

{Story Title}

**As a** {role}
**I want** {action}
**so that** {benefit}

## Status

{Draft|In Progress| Complete}

## Context

{

- Background information
- Current state
- Story justification
- Technical context
- Business drivers
- Relevant history from previous stories
  }

## Estimation

Story Points: {Story Points (1 SP = 1 day of Human Development = 10 minutes of AI development)}

## Tasks

{

1. - [ ] {Major Task Group 1}
   1. - [ ] {Test Subtasks (as needed)}
   2. - [ ] {Subtask}
            N.
            N.
   3. N.

- Use - [x] for completed items
- Use ~~skipped/cancelled items~~
  }

## Constraints

- List any technical or business constraints

## Data Models / Schema

- Database schemas
- API request/response models
- Interfaces/types

## Structure

- Module organization
- File structure plan

## Diagrams

- Mermaid diagrams as needed

## Dev Notes

- Implementation commentary
- Important considerations
- Technical decisions made or changed

## Chat Command Log

- Commands from User
- Agent Question and Users Response

## Examples

<example>
# Epic-1 - Story-2
# Implement Chessboard UI

**As a** chess player
**I want** to see a clear and interactive chessboard
**so that** I can play chess in the web browser

## Status

In Progress

## Context

Part of Epic-1 which implements the core 2-player chess game. This story focuses on the visual and interactive aspects of the chessboard. The project setup (Story-1) is complete, providing the foundation for UI implementation.

## Estimation

Story Points: 2

## Tasks

1. - [x] Create Chessboard Grid
   1. - [x] Implement 8x8 board layout
   2. - [x] Add square coloring
   3. - [x] Write grid tests
2. - [ ] Add Chess Pieces
   1. - [ ] Create piece components
   2. - [ ] Add piece images
   3. - [ ] Write piece tests
3. - [ ] Implement Basic Interaction
   1. - [ ] Add click handlers
   2. - [ ] Highlight selected square
   3. - [ ] Write interaction tests

## Constraints

- Always ensure that we are using the Eastern Time Zone for all dates

## Data Models / Schema

```json piece.mode
{
   id: number
   position?: BoardPosition
   captured: boolean
   name: string
}
```

## Structure

This new feature is implemented under /src/new-foo-api for the handler, with all logic beyond request and response in new-foo-service.ts and src/data/new-foo-data.ts handling all data access against dynamoDb.

## Diagrams

{mermaid sequence diagram of capture piece logic and updating database}

## Dev Notes

- Ensure we are putting all code in its proper layer - reference the structure section above - also check the notes of Story-1 where we made a decision to pivot to always using SVG files instead of PNG files.

## Chat Command Log

- BMad: Let's implement the chessboard UI
- ....
- AiAgent: Grid implementation complete, proceeding with piece placement
- BMad: Why did you delete all of the files I asked you to move and move all the files I asked you to delete!!! Bad Agent
- AiAgent: 1000 pardons master BMad I will correct that now <deletes entire project and uninstalls cursor from machine>
- BMad: Noooooooo!!!!!!!!!!!!!
  </example>
