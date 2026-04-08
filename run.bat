@echo off
pip install -r .\requirements.txt

cd src

cls
uvicorn main:app --reload
