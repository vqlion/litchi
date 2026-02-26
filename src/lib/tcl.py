import requests
from dotenv import load_dotenv
import os

load_dotenv()

TCL_BASE_URL = "https://data.grandlyon.com/fr/datapusher/ws/rdata/"
TCL_USER = os.getenv('TCL_USER')
TCL_PASS = os.getenv('TCL_PASS')

def get_wait_times_from_tcl(lines: [str], directions: [int], stop_ids: [int]):
    tcl_endpoint = "tcl_sytral.tclpassagearret/all.json"
    extra_params = ""

    if len (lines) > 0:
        extra_params += f"?ligne__in="
        for line in lines:
            extra_params += f"{line},"
        extra_params = extra_params.rstrip(',')
    
    if len(directions) > 0: 
        extra_params += "&idtarretdestination__in="
        for direction in directions:
            extra_params += f"{direction},"
        extra_params = extra_params.rstrip(',')

    if len(stop_ids) > 0:
        extra_params += "&id__in="
        for stop_id in stop_ids:
            extra_params += f"{stop_id},"
        extra_params = extra_params.rstrip(',')

    complete_url = TCL_BASE_URL + tcl_endpoint + extra_params
    print(complete_url)
    return make_tcl_get_request(complete_url)

def get_stops_from_tcl(stop_ids: [int]):
    tcl_endpoint = "tcl_sytral.tclarret/all.json"
    extra_params = ""

    if len(stop_ids) > 0: extra_params += f"?id__in="
    for stop in stop_ids:
        extra_params += f"{stop},"
    extra_params = extra_params.rstrip(',')

    complete_url = TCL_BASE_URL + tcl_endpoint + extra_params

    return make_tcl_get_request(complete_url)

def make_tcl_get_request(url: str):
    res = requests.get(url, auth=(TCL_USER, TCL_PASS))
    res.raise_for_status()
    return res.json()
