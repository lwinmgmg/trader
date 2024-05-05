#!/bin/bash
# Black Formatter
echo "Black Formatter is running"
poetry run black .
echo "Done..."

# Flake8 Linter
echo "Flake8 Linter is running"
poetry run flake8
echo "Done..."


# Pylint Linter
echo "Pylint Linter is running"
poetry run coverage run -m pylint src/trader
echo "Done..."
