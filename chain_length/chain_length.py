import psycopg2
from flask import Flask, request, render_template, redirect, escape
from chain import chain_length
import time


app = Flask(__name__)

def insert_length(frase: str) -> None:
    dbconfg = {'host': '127.0.0.1',
               'user': 'angel',
               'password': '123',
               'database': 'recuperacion', }
    connection = psycopg2.connect(**dbconfg)
    resultado = chain_length(frase)
    ahora = str(time.strftime("%c"))
    _SQL = """INSERT INTO chain_length(chain, length, ts) VALUES(%s, %s, %s)"""
    cursor = connection.cursor()
    cursor.execute(_SQL, (frase,
                          resultado, ahora,))
    connection.commit()
    cursor.close()
    connection.close()

@app.route('/')
def home() -> '302':
    return redirect('/entry')


@app.route('/chain_length', methods=['POST'])
def do_search() -> 'html':
    chain = request.form['chain']
    title = 'Aqui estan tus resultados:'
    length = chain_length(chain)
    insert_length(chain)
    return render_template('results.html',
                           the_title=title,
                           the_chain=chain,
                           the_length=length,)


@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html',
                           the_title='Bienvenido a mi web')


@app.route('/data')
def view_data() -> 'html':
    params = {'host': '127.0.0.1',
              'user': 'angel',
              'password': '123',
              'database': 'recuperacion', }
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    _sql = """SELECT chain, length, ts FROM chain_length ORDER BY ts"""
    cur.execute(_sql)
    rows = cur.fetchall()
    contents = []
    for row in rows:
        contents.append(row)
    cur.close()
    conn.close()
    titles = ('Frase', 'Longitud de caracteres', 'Fecha')
    return render_template('data.html',
                           the_title='Vista de la informacion',
                           the_row_titles=titles,
                           the_data=contents, )

app.run(debug=True)
