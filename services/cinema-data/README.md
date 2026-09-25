# CinemaOS Cinema Data Layer

CINE002 data boundary for historical cinema intelligence.

Pipeline:
collector -> raw records -> normalization -> entity resolution -> historical store -> API/UI.

The layer is source-aware and append-oriented. New collection runs must preserve previous career events, credits, media and evidence rather than replacing history.

A collector returns normalized dictionaries with identity, aliases, languages, roles, career_events, filmography, awards, social_links, media, sources and collected_at where available.
