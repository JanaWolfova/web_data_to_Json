from flask import Flask, request, render_template  
from googleapiclient.discovery import build  
import json  
import os
from dotenv import load_dotenv

# Načíst proměnné prostředí ze souboru .env
load_dotenv()

# Získat API klíč a CSE ID z proměnných prostředí
my_api_key = os.getenv('API_KEY')
my_cse_id = os.getenv('CSE_ID')

app = Flask(__name__)  # Inicializace Flask aplikace




def google_search(query):
    """
    Funkce na vyhledávání Google pomocí Google Custom Search API.
    """
    service = build("customsearch", "v1", developerKey=my_api_key)  # Vytvoření služby pro vyhledávání
    res = service.cse().list(q=query, cx=my_cse_id).execute()  # Provedení vyhledávání s dotazem a ID vyhledávače
    return res.get('items', [])  # Vrácení výsledků vyhledávání

def process_results(results) -> list:
    """
    Funkce na zpracování výsledků vyhledávání z Google Custom Search API.
    """
    processed_results = []  # Inicializace seznamu pro zpracované výsledky
    for item in results:  # Procházení každého výsledku
        processed_results.append({  # Přidání zpracovaného výsledku do seznamu
            "title": item.get("title", ""),  # Získání titulu
            "link": item.get("link", ""),  # Získání odkazu
            "snippet": item.get("snippet", "")  # Získání úryvku textu
        })
    return processed_results  # Vrácení zpracovaných výsledků

def save_to_json(data):
    # Uložit data do souboru JSON
    with open("results.json", mode="w", encoding="utf-8") as file:  # Otevření souboru pro zápis
        json.dump(data, file, indent=4, ensure_ascii=False)  # Uložení dat do souboru

@app.route("/")  # Definice routy pro hlavní stránku
def index():
    # Vykreslení HTML šablony s formulářem pro zadání klíčového slova
    return render_template("index.html")  # Návrat HTML šablony

@app.route("/search", methods=["POST"])  # Definice routy pro vyhledávání
def search():
    query = request.form["query"]  # načte klíčové slovo z formuláře
    print("Query:", query)  # Výpis klíčového slova pro kontrolu
    results = google_search(query)  # provede vyhledávání na Google
    print("Results:", results)  # Výpis výsledků vyhledávání pro kontrolu
    processed_results = process_results(results)  # zpracuje výsledky vyhledávání
    save_to_json(processed_results)  # uloží zpracované výsledky do JSON souboru
    return "Výsledky vyhledávání byly uloženy do souboru results.json."  # zpráva o úspěšném uložení
port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    

    app.run(host='0.0.0.0', port=port)