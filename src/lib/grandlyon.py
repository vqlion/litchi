from dotenv import load_dotenv
import requests
import os

load_dotenv()

GRANDLYON_BASE_URL = "https://data.grandlyon.com/fr/datapusher/ws/rdata/"
GRANDLYON_USER = os.getenv('GRANDLYON_USER')
GRANDLYON_PASS = os.getenv('GRANDLYON_PASS')

def make_grandlyon_request(url: str):
    res = requests.get(url, auth=(GRANDLYON_USER, GRANDLYON_PASS))
    res.raise_for_status()
    return res.json()
