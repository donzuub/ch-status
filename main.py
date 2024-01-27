from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import json

app = FastAPI()

@app.get("/ch-status")
async def ch_status():
    url = "https://status.changehealthcare.com/"
    response = requests.get(url)
    if response.status_code == 200:
        return parse_unresolved_incidents(response.text)
    else:
        return {"error": "Failed to retrieve data"}

def parse_unresolved_incidents(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    incidents = []

    for incident in soup.find_all("div", class_="unresolved-incident"):
        title = incident.find("a", class_="actual-title").text.strip()
        status_updates = []
        for update in incident.find_all("div", class_="update"):
            status = update.strong.text.strip()
            description = ' '.join(update.span.text.split())
            status_updates.append({"status": status, "description": description})
        
        incidents.append({"title": title, "updates": status_updates})

    return incidents
