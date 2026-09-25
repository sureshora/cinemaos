# CINE002.15 — Temporal Knowledge & Historical State Reconstruction

Status: IMPLEMENTED ON FEATURE BRANCH

## Objective

Make CinemaOS time-aware so facts can be evaluated according to their historical validity rather than only their current stored value.

## Temporal fact

A temporal fact contains:

- fact ID
- entity ID
- property
- value
- valid_from
- valid_to
- observed_at
- source references

This distinguishes:
- when something was true
- when CinemaOS observed it
- where the evidence came from

## Historical reconstruction

Given an entity and date, CinemaOS selects the latest applicable valid fact for each property.

Example:

    Artist
      |
      +-- role = Actor
          valid_from = 1975
          valid_to   = 1990
      |
      +-- role = Producer
          valid_from = 1985

A query for 1980 and a query for 1990 can therefore produce different historical states.

## API

GET /api/v1/cinema/entities/{entity_id}/state?at=YYYY-MM-DD

## UI

apps/cinema-intelligence/timeline.py provides a point-in-time explorer.

## Important distinction

valid_from/valid_to represent the modeled validity period of a fact. observed_at represents when CinemaOS collected or observed the evidence. These are intentionally separate.

## Next

CINE002.16 — temporal event graph, career timelines and historical filmography reconstruction.
