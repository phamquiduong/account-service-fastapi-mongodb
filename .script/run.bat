@echo off

REM Install dependencies from pyproject.toml
pip install .

cd src

cls
uvicorn main:app --reload --host 0.0.0.0 --port 80
