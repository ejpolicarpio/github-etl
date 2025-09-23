from fastapi import FastAPI
from src.main import create_app

app: FastAPI = create_app()
