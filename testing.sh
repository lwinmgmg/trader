#!/bin/bash

# Pytest
echo "Pytest is running"
poetry run coverage run -m pytest .
echo "Done..."

echo "Done..."
# Coverage Report
echo "Coverage Report"
poetry run coverage report -m
echo "Done..."