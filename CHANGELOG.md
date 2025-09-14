# Changelog

## [Unreleased]

### Major Changes
- Refactored project structure for clarity and maintainability:
  - Moved all main Python scripts and modules to `src/`.
  - Created `notebooks/` folder for Jupyter notebooks, organized by approach.
  - Merged previous `approaches/` and `comparison/` into `notebooks/`.
  - Centralized raw input data in `data/` with subfolders for PDFs, texts, and database.
  - Consolidated generated artifacts (indexes, KGs, ontologies) in `results/`.
  - Standardized test scripts and notebooks in `tests/`.
  - Renamed and clarified folder names for consistency (e.g., `utilities` to `utils` if applicable).
- Updated `README.md` to reflect new structure and usage instructions.
- Documented main components and their locations in the new structure.

### Minor Changes
- Improved documentation for onboarding and usage.
- Added this `CHANGELOG.md` to track future changes.

---
For details on usage and structure, see `README.md`.
