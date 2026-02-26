from fastapi import FastAPI, Request, Query
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Annotated
from pydantic import BaseModel
from lib import tcl, parser

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

class RefreshBody(BaseModel):
    lines: str
    directions: str
    stop_ids: str

@app.get('/', response_class=HTMLResponse)
def get_index(
    request: Request,
    lines: Annotated[list[str] | None, Query()] = ['T1', 'C17'],
    directions: Annotated[list[int] | None, Query()] = [],
    stops: Annotated[list[int] | None, Query()] = [34067, 34068, 43114]
    ):
    return templates.TemplateResponse(
        request=request, 
        name="index.html",
        context={
            "lines": ','.join(lines),
            "directions": directions,
            "stop_ids": stops
        }
        )

@app.post('/refresh')
def refresh_index(body: RefreshBody):
    lines = [] if body.lines == '' else body.lines.split(',')
    directions = [] if body.directions == '' else body.directions.split(',')
    stop_ids = [] if body.stop_ids == '' else body.stop_ids.split(',')

    raw_tcl_wait_times = tcl.get_wait_times_from_tcl(lines, directions, stop_ids)

    raw_tcl_stops = tcl.get_stops_from_tcl(body.stop_ids.split(','))
    tcl_stops_to_names = parser.get_stop_names_from_tcl_data(raw_tcl_stops)

    return parser.prepare_tcl_data(raw_tcl_wait_times, tcl_stops_to_names)