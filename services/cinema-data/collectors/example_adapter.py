"""Reference adapter for an existing user collector.

Replace the implementation with the user's real collector logic. Keeping the
adapter contract stable lets CinemaOS consume legacy .py collectors without
moving their code into the UI.
"""

name="example-adapter"

def collect() -> list[dict]:
    return []
