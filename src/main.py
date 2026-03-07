from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import BaseModel
from lib import tcl, velov, parser

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class TCLRefreshBody(BaseModel):
    lines: str
    directions: str
    stop_ids: str

class VELOVRefreshBody(BaseModel):
    pairs: str

@app.get('/')
def get_index():
    return RedirectResponse(url="/tcl")

@app.get('/tcl', response_class=HTMLResponse)
def get_tcl_index(
    request: Request,
    lines: Annotated[str | None, Query()] = 'T1,C17',
    directions: Annotated[str | None, Query()] = "",
    stops: Annotated[str | None, Query()] = "34067,34068,43114"
    ):
    return templates.TemplateResponse(
        request=request, 
        name="tcl_index.html",
        context={
            "lines": lines,
            "directions": directions,
            "stop_ids": stops
        })

@app.post('/refresh/tcl')
def refresh_tcl_index(body: TCLRefreshBody):
    lines = [] if body.lines == '' else body.lines.split(',')
    directions = [] if body.directions == '' else body.directions.split(',')
    stop_ids = [] if body.stop_ids == '' else body.stop_ids.split(',')

    raw_tcl_wait_times = tcl.get_wait_times_from_tcl(lines, directions, stop_ids)

    raw_tcl_stops = tcl.get_stops_from_tcl(body.stop_ids.split(','))
    tcl_stops_to_names = parser.get_stop_names_from_tcl_data(raw_tcl_stops)

    return parser.prepare_tcl_data(raw_tcl_wait_times, tcl_stops_to_names)

@app.get('/velov', response_class=HTMLResponse)
def get_velov_index(
    request: Request,
    pairs: Annotated[list[str] | None, Query()] = ["10002,7009"]
    ):
    print(pairs)
    return templates.TemplateResponse(
        request=request, 
        name="velov_index.html",
        context={
            "pairs": pairs
        })

@app.post('/refresh/velov')
def refresh_velov(body: VELOVRefreshBody):
    request_pairs = [] if body.pairs == '' else body.pairs.split('-')
    
    pairs = []
    stations = []
    for pair in request_pairs:
        p = pair.split(',')
        pairs.append((int(p[0]), int(p[1])))
        stations.append(int(p[0]))
        stations.append((int(p[1])))

    raw_velov_data = velov.get_stations_info(stations)

    return parser.prepare_velov_data(raw_velov_data, pairs)