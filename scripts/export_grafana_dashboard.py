import os
import requests
import json

# Variables d'environnement (à configurer dans ton CI/CD ou localement)
GRAFANA_URL = os.getenv("GRAFANA_URL", "http://localhost:3000")
GRAFANA_API_KEY = os.getenv("GRAFANA_API_KEY", "admin:admin")  # à remplacer par ton API token
DASHBOARD_UID = os.getenv("GRAFANA_DASHBOARD_UID", "obesitrack")  # UID de ton dashboard

# Endpoint API Grafana
url = f"{GRAFANA_URL}/api/dashboards/uid/{DASHBOARD_UID}"
headers = {
    "Authorization": f"Bearer {GRAFANA_API_KEY}",
    "Content-Type": "application/json"
}

def export_dashboard():
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise requests.exceptions.HTTPError(f"Erreur export dashboard: {response.status_code}, {response.text}")
    
    data = response.json()
    dashboard = data.get("dashboard")
    
    # Sauvegarde dans docs/
    os.makedirs("docs", exist_ok=True)
    with open("docs/grafana-dashboard.json", "w", encoding="utf-8") as f:
        json.dump(dashboard, f, indent=2)
    
    print(" Dashboard exporté vers docs/grafana-dashboard.json")

if __name__ == "__main__":
    export_dashboard()
