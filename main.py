from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

class Region(BaseModel):
  id: int
  geo_type: str
  name: str


class Location(BaseModel):
  id: int
  region: Region
  sub_region: Optional[str] = None
  country: Optional[str] = None


class DirectionRequest(BaseModel):
  location: Location
  transportation_type: str
  request_date: str
  requests: float
  locked: bool


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
  return templates.TemplateResponse('index.html', {'request': request})


@app.get("/api/regions/{geo_type}")
def read_regions(geo_type: str):
  return {'geoType': geo_type, 'regions': []}


@app.get("/api/locations/{region_id}")
def read_locations(region_id: int):
  return {'locations': []}


@app.get("/api/traffic")
def read_traffic():
  return {'locations': []}


@app.put("/api/traffic")
def update_traffic():
  return {'locations': []}