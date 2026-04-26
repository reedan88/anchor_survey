# ==============================================================
# Anchor Survey - Makefile
#
# Usage:
#   make env        Create or update Conda environment
#   make gui        Launch the Panel GUI
#   make test       Run tests with pytest
#   make lint       Run flake8 code style checks
#   make build      Build distribution packages
#   make clean      Remove build artifacts and caches
# ==============================================================

ENV_NAME := anchor_survey
CONDA := $(shell command -v conda 2>/dev/null)

# ==============================================================
# Help
# ==============================================================

.PHONY: help
help:
	@echo ""
	@echo "Anchor Survey - Available commands:"
	@echo "  make env     Create or update Conda environment"
	@echo "  make gui     Launch the Panel GUI"
	@echo "  make test    Run tests with pytest"
	@echo "  make lint    Run flake8 code style checks"
	@echo "  make build   Build distribution packages"
	@echo "  make clean   Remove build artifacts and caches"
	@echo ""

# ==============================================================
# Environment setup
# ==============================================================

.PHONY: env
env:
ifndef CONDA
	$(error conda not found. Install Miniconda: https://docs.conda.io/en/latest/miniconda.html)
endif
	conda env update -f environment.yml --prune

# ==============================================================
# Run & Test
# ==============================================================

.PHONY: gui
gui:
	@echo ">>> Starting Anchor Survey GUI (http://localhost:5006)"
ifdef CONDA
	conda run -n $(ENV_NAME) panel serve gui/survey_gui.py --show
else
	panel serve gui/survey_gui.py --show
endif

.PHONY: test
test:
ifdef CONDA
	conda run -n $(ENV_NAME) pytest
else
	pytest
endif

.PHONY: lint
lint:
ifdef CONDA
	conda run -n $(ENV_NAME) flake8 survey gui tests
else
	flake8 survey gui tests
endif

# ==============================================================
# Build & Publish
# ==============================================================

.PHONY: build
build:
	python -m build

# ==============================================================
# Cleanup
# ==============================================================

.PHONY: clean
clean:
	rm -rf build dist *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
