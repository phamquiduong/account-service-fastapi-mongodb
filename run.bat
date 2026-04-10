@echo off
pip install -r .\requirements.txt

cd src

cls
uvicorn main:app --reload --host 0.0.0.0 --port 80
