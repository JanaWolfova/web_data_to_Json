from flask import Flask, request, render_template  
import requests
from bs4 import BeautifulSoup
import json
import os



"""
Načítání dat z formuláře, který uživatel vyplní a odešle. 
vytvoříme jednoduchý formulář v HTML a připravíme Flask aplikaci, 
aby tato data přijímala.
"""

app = Flask(__name__)

@app.route("/") # určí URL cestu, na kterou se má daná funkce navázat.

def index(): #func zobrazí hlavní stránku, která obsahuje formulář
    return render_template("index.html")   #vykreslení HTML šablon


@app.route("/search", methods=["POST"]) #přijme data z formuláře

def search():
    query = request.form["query"]  # načte klíčové slovo
    html = google_search(query)  # provede vyhledávání na Googlu
    results = process_results(html)  # zpracuje výsledky vyhledávání
    
    return render_template("results.html", results=results)  # zobrazí výsledky na nové stránce



def google_search(query):
    """
    funkce na vyhledávání google 
    """
    formatted_query = query.replace(" ", "+")
    url = f"https://www.google.com/search?q={formatted_query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)



    return response.text


def process_results(html) -> dict:
    """
    funkce z beautifulsoup rozděluje text na html stránce podle  a uloží do seznamu slovníků.
    """
    soup = BeautifulSoup(html, "html.parser")
    results = []

    for g in soup.find_all(class_="g"):
        title = g.find("h3")
        link = g.find("a")["href"]
        snippet = g.find(class_="aCOpRe")

        if title and link:
            results.append({
                "title": title.text,
                "link": link,
                "snippet": snippet.text if snippet else ''
            })

    return results

def format_and_save_to_json(results):
    # Převést seznam slovníků na řetězec JSON
    formatted_data = json.dumps(results, indent=4, ensure_ascii=False)

    # Uložit řetězec JSON do souboru
    with open("results.json", mode="w", encoding="utf-8") as file:
        file.write(formatted_data)



if __name__ == "__main__":
    #řešení pro Heroku
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)