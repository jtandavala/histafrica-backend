#!/bin/bash

uv sync --frozen

/app/.venv/bin/python src/manage.py migrate  # Run migrations
/app/.venv/bin/python src/manage.py runserver 0.0.0.0:8000  # Start Django server
