import requests
from lib import grandlyon as gl

def get_parks_dispos(parking_ids: [int]):
    velov_endpoint = "tcl_sytral.tclparcrelaistr/all.json"
    extra_params = ""

    if len (parking_ids) > 0:
        extra_params += f"?id__in="
        for id in parking_ids:
            extra_params += f"{id},"
        extra_params = extra_params.rstrip(',')
    
    complete_url = gl.GRANDLYON_BASE_URL + velov_endpoint + extra_params
    return gl.make_grandlyon_request(complete_url)