# ==============================================================
# Anchor Survey Project - Makefile 
# Author: Andrew Reed
# ==============================================================

# Environment name (must match environment.yml)
ENV_NAME := anchor_survey

# ==============================================================
# Help
# ==============================================================

.PHONY: help
help:
	@echo ""
	@echo "Anchor Survey - Available commands:"
	@echo "  make env          Create or update Conda environment"
	@echo "  make activate     Print command to activate the environment"
	@echo "  make gui          Launch the Panel GUI"
	@echo "  make test         Run all tests using pytest"
	@echo "  make lint         Run code style checks with flake8"
	@echo "  make clean        Remove build artifacts and caches"
	@echo ""

# ==============================================================
# Environment setup
# ==============================================================

.PHONY: env
env:
	@echo ">>> Creating or updating Conda environment '$(ENV_NAME)'..."
	conda env update -f environment.yml --prune

.PHONY: activate
activate:
	@echo ">>> To activate this environment, run:"
	@echo "conda activate $(ENV_NAME)"

# ==============================================================
# Run & Test
# ==============================================================

.PHONY: gui
gui:
	conda run -n $(ENV_NAME) panel serve gui/survey_gui.py --show

.PHONY: test
test:
	conda run -n $(ENV_NAME) pytest -v --maxfail=1 --disable-warnings

.PHONY: lint
lint:
	conda run -n $(ENV_NAME) flake8 survey gui tests

# ==============================================================
# Cleanup
# ==============================================================

.PHONY: clean
clean:
	rm -rf __pycache__ */__pycache__ .pytest_cache build dist *.egg-info
