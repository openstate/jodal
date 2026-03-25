#!/bin/sh

# Add --reload if ENV variable DEVELOPMENT is set to true
if [ "$ENVIRONMENT" = "development" ]; then
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
else
    exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 8
fi
