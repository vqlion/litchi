import requests
from lib import grandlyon as gl

def get_stations_info(stations_ids: [int]):
    velov_endpoint = "jcd_jcdecaux.jcdvelov/all.json"
    extra_params = ""

    if len (stations_ids) > 0:
        extra_params += f"?number__in="
        for id in stations_ids:
            extra_params += f"{id},"
        extra_params = extra_params.rstrip(',')
    
    complete_url = gl.GRANDLYON_BASE_URL + velov_endpoint + extra_params
    return gl.make_grandlyon_request(complete_url)