# Hittite Cuneiform Pipeline

An automated data pipeline written in Python to extract, parse, deduplicate, and analyze (Hittite) cuneiform sign frequencies and orthographic patterns (e.g. plene spelling) from the available digitized Hittite corpora (primarily from *TLHdig* / HPM).

## Features
- **Epigraphic Cleaning:** Tiered filtering of damage brackets (`[...]` vs `⌜...⌝`) at the sign-token level.
- **Manuscript Stratification:** Strict isolation of Original Script (`/OS`) manuscripts from Middle Script (`/MS`) and New Script (`/NS`) copies to prevent diachronic corruption of the data.
- **Fragment Deduplication:** Canonical CTH/manuscript ID tracking to prevent double-counting joined fragments.
- **Anki Deck Export:** Automated generation of dynamic study decks for Hittite sign readings and sign combinations.

## Project Setup

1. Clone this repository:
```bash
git clone git@github.com:edwardwilk3/hittite-cuneiform-pipeline.git
cd hittite-cuneiform-pipeline
```