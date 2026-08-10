# CINE001 — Project Foundation & Repository Architecture

## Status

READY FOR VERIFICATION

## Objective

Create the stable CinemaOS repository foundation without implementing
production agent behavior.

## Scope

- Monorepo workspace
- Web application shell
- Agent API shell
- Shared package boundaries
- Environment conventions
- Engineering documentation
- Health endpoint
- Basic frontend boot page

## Non-goals

CINE001 does NOT implement:

- agents
- Gemini orchestration
- Parallel research
- production memory
- multimodal artifacts
- scene generation
- live production monitoring

Those belong to later CINE units.

## Acceptance criteria

- [ ] `pnpm install` succeeds
- [ ] web development server starts
- [ ] web production build succeeds
- [ ] API starts
- [ ] `GET /health` returns `status=ok`
- [ ] repository follows CINE directory boundaries
- [ ] no credentials committed
