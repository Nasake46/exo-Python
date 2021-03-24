from functools import lru_cache
from flask import Flask
import csv
import dns.resolver

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False


@lru_cache()
def parse_the_csv():
     with open(
        "short.csv", encoding="latin1"
    ) as csvfile:
        reader = csv.DictReader(csvfile, delimiter=";")
        domains = {}
        registrars = {}
        for i, data in enumerate(reader):
            domains[data["Nom de domaine"]] = {
                "fqdn": data["Nom de domaine"],
                "registrar": f"/api/registrars/{data['Nom BE']}",
                "tld": data["Sous domaine"],
                "owner": {
                    "type": data["Type du titulaire"],
                    "country": data["Pays titulaire"],
                    "departement": data["Departement titulaire"],
                },
                "idn": data["Domaine IDN"],
                "created_at": data["Date de création"],
                "domain": f"/api/domains/{data['Nom de domaine']}",
            }
            registrars[data["Nom BE"]] = (
                {
                    "self": f"/api/registrars/{data['Nom BE']}",
                    "country": data["Pays BE"],
                    "departement": data["Departement BE"],
                    "city": data["Ville BE"],
                    "name": data["Nom BE"],
                },
            )
        return domains, registrars

@app.route("/")
def hello_world():
    return "Hello World !"

@app.route("/api/domains/")
def api_world():
    response = {"items": parse_the_csv()}
    return response

@app.route("/api/domains/<fqdn>")
def api_world_select(fqdn):
    response = {"items": []}
    domains, registrars =  parse_the_csv()
    for name, data in domains.items():
        if data["fqdn"] == fqdn:
            response["items"].append(data)
    return response

@app.route("/test/")
def api_dns(fqdn):
    answer = dns.resolver.query(fqdn, "MX")
    for rdata in answer:
        data.append({
            "exchange" : str(rdata.exchange),
            "preference" : str(rdata.preference),
            "nom" : fqdn,
            "type" : "MX"
        })
    return data