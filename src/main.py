from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
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
    st_from: str
    st_to: str

@app.get('/tcl', response_class=HTMLResponse)
def get_tcl_index(
    request: Request,
    lines: Annotated[list[str] | None, Query()] = ['T1', 'C17'],
    directions: Annotated[list[int] | None, Query()] = [],
    stops: Annotated[list[int] | None, Query()] = [34067, 34068, 43114]
    ):
    return templates.TemplateResponse(
        request=request, 
        name="tcl_index.html",
        context={
            "lines": ','.join(lines),
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
    st_from: Annotated[list[int] | None, Query()] = [7027],
    st_to: Annotated[list[int] | None, Query()] = [7009]
    ):
    return templates.TemplateResponse(
        request=request, 
        name="velov_index.html",
        context={
            "from": st_from,
            "to": st_to
        })

@app.post('/refresh/velov')
def refresh_velov(body: VELOVRefreshBody):
    st_from = [] if body.st_from == '' else body.st_from.split(',')
    st_to = [] if body.st_to == '' else body.st_to.split(',')

    pair_count = min(len(st_from), len(st_to))
    pairs = []
    for i in range(pair_count):
        pairs.append((int(st_from[i]), int(st_to[i])))
    
    raw_velov_data = velov.get_stations_info(st_from + st_to)

    return parser.prepare_velov_data(raw_velov_data, pairs)