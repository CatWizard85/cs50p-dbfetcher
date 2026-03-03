from flask import Flask, render_template, request, g
from helpers.form_manager import FORM_MAP, clean_form
from helpers.query_manager import build_conditions
from helpers.download_manager import create_excel, HEADERS_MAP
from helpers.entrate_uscite_manager import create_excel_entrate_uscite
from config import DB_PATH
import sqlite3


# FLASK STUFF

app = Flask(__name__)
app.config["DATABASE"] = DB_PATH
app.config["DEBUG"] = True # Togliere in versione finale
app.config["TEMPLATES_AUTO_RELOAD"] = True

# After every request, this prevents browser from using cache (TOGLIERE TUTTA LA FUNZIONE IN VERSIONE FINALE)
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# DATABASE STUFF

def get_db():
    if "db" not in g:
        try:
            g.db = sqlite3.connect(app.config["DATABASE"])
            g.db.row_factory = sqlite3.Row
            g.db.execute('PRAGMA foreign_keys = ON')
            print("Connessione DB aperta")
        except sqlite3.Error as e:
            print(f"Errore connessione DB: {e}")
            g.db = None
    return g.db

# After every request, Flask does this
@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        print("Chiudendo connessione DB")
        db.close()


# SEARCH ROUTES

@app.route("/art_search", methods=["GET", "POST"])
def art_search():
    results = []
    form_data = {}
    is_popup = request.args.get("popup") == "1" or request.form.get("popup") == "1"

    if request.method == "GET":
        #Render template
        if is_popup:
            return render_template("popup_art_search.html", form_data=form_data, HEADERS_MAP=HEADERS_MAP)
        else:
            return render_template("art_search.html", form_data=form_data)

    if request.method == "POST":
        form_data = clean_form(request.form.to_dict())
        results = handle_art_search(form_data)

        #Render template
        if is_popup:
            return render_template("popup_art_search.html", results=results, form_data=form_data, HEADERS_MAP=HEADERS_MAP)
        else:
            return render_template("art_search.html", results=results, form_data=form_data)

def handle_art_search(form_data):
    conditions, params, order_condition, order_param = build_conditions(form_data)
    query = """
    SELECT
        art.codart,
        codice,
        spessore,
        scelta,
        grammi,
        lato_a,
        lato_b,
        descrizione,
        um,
        giacenza,
        recenti.prezzo,
        ubicazione
    FROM articoli AS art
    LEFT JOIN (
        SELECT
            codart,
            prezzo
        FROM (
            SELECT
                *, ROW_NUMBER() OVER (PARTITION BY codart ORDER BY data DESC) AS rn
            FROM movimenti
            WHERE tipo_mov = 'carico'
        )
        WHERE rn = 1
    ) AS recenti
    ON art.codart = recenti.codart
    WHERE 1=1
    """
    if conditions:
        query += " AND " + " AND ".join(conditions)
    if order_condition and order_param in set(FORM_MAP.keys()):
        query += f" ORDER BY {order_param}"
    print(query)
    print(params)

    db = get_db()
    cur = db.execute(query, params)
    rows = cur.fetchall()

    return [{HEADERS_MAP.get(k, k): row[k] for k in row.keys()} for row in rows]


@app.route("/lot_search", methods=["GET", "POST"])
def lot_search():
    results = []
    form_data = {}

    if request.method == "GET":
        #Render template
        return render_template("lot_search.html", form_data=form_data)

    if request.method == "POST":
        form_data = clean_form(request.form.to_dict())
        results = handle_lot_search(form_data)

        #Render template
        return render_template("lot_search.html", results=results, form_data=form_data)

def handle_lot_search(form_data):
    conditions, params, order_condition, order_param = build_conditions(form_data)
    query = "SELECT cod_lotto, codart, giacenza FROM lotti WHERE 1=1"
    if conditions:
        query += " AND " + " AND ".join(conditions)

    query += f" ORDER BY cod_lotto"

    print(query)
    print(params)

    db = get_db()
    cur = db.execute(query, params)
    rows = cur.fetchall()

    return [{HEADERS_MAP.get(k, k): row[k] for k in row.keys()} for row in rows]


@app.route("/clie_search", methods=["GET", "POST"])
def clie_search():
    results = []
    form_data = {}
    is_popup = request.args.get("popup") == "1" or request.form.get("popup") == "1"

    if request.method == "GET":
        #Render template
        if is_popup:
            return render_template("popup_clie_search.html", form_data=form_data, HEADERS_MAP=HEADERS_MAP)
        else:
            return render_template("clie_search.html", form_data=form_data)

    if request.method == "POST":
        form_data = clean_form(request.form.to_dict())
        results = handle_clie_search(form_data)

        #Render template
        if is_popup:
            return render_template("popup_clie_search.html", results=results, form_data=form_data, HEADERS_MAP=HEADERS_MAP)
        else:
            return render_template("clie_search.html", results=results, form_data=form_data)

def handle_clie_search(form_data):
    conditions, params, order_condition, order_param = build_conditions(form_data)
    query = "SELECT cod_clie, nome, indirizzo, citta, provincia, num_tel FROM clienti WHERE 1=1"
    if conditions:
        query += " AND " + " AND ".join(conditions)
    print(query)
    print(params)

    db = get_db()
    cur = db.execute(query, params)
    rows = cur.fetchall()

    return [{HEADERS_MAP.get(k, k): row[k] for k in row.keys()} for row in rows]


@app.route("/forn_search", methods=["GET", "POST"])
def forn_search():
    results = []
    form_data = {}
    is_popup = request.args.get("popup") == "1" or request.form.get("popup") == "1"

    if request.method == "GET":
        #Render template
        if is_popup:
            return render_template("popup_forn_search.html", form_data=form_data, HEADERS_MAP=HEADERS_MAP)
        else:
            return render_template("forn_search.html", form_data=form_data)

    if request.method == "POST":
        form_data = clean_form(request.form.to_dict())
        results = handle_forn_search(form_data)

        #Render template
        if is_popup:
            return render_template("popup_forn_search.html", results=results, form_data=form_data, HEADERS_MAP=HEADERS_MAP)
        else:
            return render_template("forn_search.html", results=results, form_data=form_data)

def handle_forn_search(form_data):
    conditions, params, order_condition, order_param = build_conditions(form_data)
    query = "SELECT cod_forn, nome, indirizzo, citta, provincia, num_tel FROM fornitori WHERE 1=1"
    if conditions:
        query += " AND " + " AND ".join(conditions)
    print(query)
    print(params)

    db = get_db()
    cur = db.execute(query, params)
    rows = cur.fetchall()

    return [{HEADERS_MAP.get(k, k): row[k] for k in row.keys()} for row in rows]


@app.route("/mov_search", methods=["GET", "POST"])
def mov_search():
    results = []
    form_data = {}

    if request.method == "GET":
        #Render template
        return render_template("mov_search.html", form_data=form_data)

    if request.method == "POST":
        form_data = clean_form(request.form.to_dict())
        results = handle_mov_search(form_data)

        #Render template
        return render_template("mov_search.html", results=results, form_data=form_data)

def handle_mov_search(form_data):
    conditions, params, order_condition, order_param = build_conditions(form_data, is_mov=True)
    query = """
    SELECT
        movimenti.record,
        movimenti.data,
        movimenti.tipo_doc,
        movimenti.num_doc,
        movimenti.cod_clie,
        clienti.nome AS nome_clie,
        movimenti.cod_forn,
        fornitori.nome AS nome_forn,
        movimenti.codart,
        movimenti.cod_lotto,
        movimenti.descrizione,
        movimenti.um,
        movimenti.quantita,
        movimenti.prezzo
    FROM movimenti
    LEFT JOIN clienti ON movimenti.cod_clie = clienti.cod_clie
    LEFT JOIN fornitori ON movimenti.cod_forn = fornitori.cod_forn
    WHERE 1=1
    """
    if conditions:
        query += " AND " + " AND ".join(conditions)
    print(query)
    print(params)

    db = get_db()
    cur = db.execute(query, params)
    rows = cur.fetchall()

    return [{HEADERS_MAP.get(k, k): row[k] for k in row.keys()} for row in rows]


# EXCEL DOWNLOAD ROUTE

HANDLERS_MAP = {
    "art_search": handle_art_search,
    "lot_search": handle_lot_search,
    "clie_search": handle_clie_search,
    "forn_search": handle_forn_search,
    "mov_search": handle_mov_search,
}

@app.route("/download", methods=["GET", "POST"])
def download():
    search_function_name = request.args.get("function")
    is_lista = request.args.get("is_lista")
    search_function = HANDLERS_MAP.get(search_function_name)
    results = []
    form_data = {}

    if request.method == "POST":
        form_data = clean_form(request.form.to_dict())
        results = search_function(form_data)

        return create_excel(results, search_function_name, is_lista)


# DOWNLOAD RIEPILOGO ENTRATE/USCITE ROUTE

def fetch_as_dict(db, query):
    cur = db.execute(query)
    rows = cur.fetchall()
    return [{k: row[k] for k in row.keys()} for row in rows]

@app.route("/download_entrate_uscite", methods=["GET", "POST"])
def download_entrate_uscite():
    lista_entrate = []
    lista_uscite = []

    if request.method == "POST":
        db = get_db()

        query_entrate = """
        SELECT record, data, codart, um, quantita, prezzo
        FROM movimenti
        WHERE tipo_doc = 'ddt_carico'
        ORDER BY data
        """
        query_uscite = """
        SELECT record, data, codart, um, quantita, prezzo
        FROM movimenti
        WHERE tipo_doc = 'ddt_scarico'
        ORDER BY data
        """

        lista_entrate = fetch_as_dict(db, query_entrate)
        lista_uscite = fetch_as_dict(db, query_uscite)

        return create_excel_entrate_uscite(lista_entrate, lista_uscite)


# INDEX ROUTE

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0", port=5000, debug=True)
