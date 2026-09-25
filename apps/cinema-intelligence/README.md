# CinemaOS Cinema Intelligence MVP

Streamlit-first research UI for the CinemaOS knowledge layer.

This MVP is intentionally separate from the Next.js application. It is designed to become a client of the future CinemaOS API without throwing away collector and data-model work.

## Run

cd apps/cinema-intelligence
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py

## MVP capabilities

- South Indian cinema artist search
- Historical career timeline
- Filmography and credits
- Awards and milestones
- Images/media references
- Social links
- Source/evidence tracking
- Collector status
- JSON import of normalized records

The sample data is clearly marked as demo data. Replace it with records produced by the collector layer.
