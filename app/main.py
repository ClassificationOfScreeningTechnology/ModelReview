from fastapi import FastAPI
from app.api import router as api_router
import yaml

app = FastAPI()

# Dodanie routera z endpointami
app.include_router(api_router)

with open("app/doc.yaml", "r") as f:
    openapi_spec = yaml.safe_load(f)

app.openapi_schema = openapi_spec