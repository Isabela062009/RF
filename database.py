import os
import sqlite3

DB = os.path.join(
    os.environ.get("FLET_APP_STORAGE_DATA", "."),
    "financeiro.db"
)


def conectar():
    return sqlite3.connect(DB)

def init_db():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS transacoes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT,
        valor REAL,
        tipo TEXT,
        categoria TEXT,
        compra_id TEXT
    )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos_mercado(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT,
            Assai REAL,
            Dom REAL,
            SuperMarket REAL,
            Casa_Fruit REAL,
            Esperanca REAL,
            Gomes REAL,
            Green_Fruit REAL
        )
    """)

     # Lista de colunas que você deseja que existam
    colunas = {
          "parcelas": "INTEGER DEFAULT 1",
          "forma_pagamento": "TEXT DEFAULT 'Pix'",
          "parcela_atual": "INTEGER DEFAULT 1",
          "compra_id": "TEXT"
    }
        # Descobre quais colunas já existem
    cur.execute("PRAGMA table_info(transacoes)")
    existentes = [coluna[1] for coluna in cur.fetchall()]
     # Adiciona somente as colunas que estiverem faltando
    for nome, tipo in colunas.items():
        if nome not in existentes:
            cur.execute(f"ALTER TABLE transacoes ADD COLUMN {nome} {tipo}")
            print(f"Coluna '{nome}' adicionada.")


    cur.execute("""
        CREATE TABLE IF NOT EXISTS mercados_personalizados(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL COLLATE NOCASE UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS produtos_mercado_personalizados (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produto TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS precos_personalizados (
            produto_id INTEGER NOT NULL,
            mercado_id INTEGER NOT NULL,
            preco REAL,
            PRIMARY KEY (produto_id, mercado_id)
        )
    """)
    conn.commit()
    conn.close()

def salvar_produto_mercado(produto, assai, dom, supermarket, casa_fruit, esperanca, gomes, green_fruit):
    

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO produtos_mercado
        (produto, Assai, Dom, SuperMarket, Casa_Fruit, Esperanca, Gomes, Green_Fruit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """,
     (produto, assai, dom, supermarket, casa_fruit, esperanca, gomes, green_fruit))
    conn.commit()
    conn.close()

def carregar_produtos_mercados():

    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT *
        FROM produtos_mercado
        """
    )

    dados = cur.fetchall()

    conn.close()
    return dados

def buscar_transacoes(mes,ano):
    conn = conectar()
    cur = conn.cursor()

    mes = f"{mes:02d}"

    cur.execute("""
        SELECT data, valor, tipo, categoria, forma_pagamento, parcelas, parcela_atual
        FROM transacoes 
        WHERE substr(data,4,2)=?
        AND substr(data,7,4)=?
        ORDER BY id DESC
    """, (mes, str(ano))
    )
    dados = cur.fetchall()
    conn.close()
    return dados


def excluir_tabela_mercado():

    conn = conectar()
    cur = conn.cursor()

    cur.execute("""
                DELETE FROM precos_personalizados
                """)
    cur.execute("""
                DELETE FROM produtos_mercado""")
    
    conn.commit()
    conn.close()

def listar_mercados():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, nome FROM mercados_personalizados ORDER BY id 
    """)
    dados = cur.fetchall()
    conn.close()
    return dados

def adicionar_mercado(nome):
    nome = (nome or "").strip()

    if not nome:
        return False, "Digite o nome do mercado."

    conn = conectar()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO mercados_personalizados (nome) VALUES (?)",
            (nome,)
        )
        conn.commit()
        return True, "Mercado adicionado."

    except sqlite3.IntegrityError:
        return False, "Esse mercado já existe."

    finally:
        conn.close()


def excluir_mercado(mercado_id):
    conn = conectar()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM precos_personalizados WHERE mercado_id = ?",
        (mercado_id,)
    )
    cur.execute(
        "DELETE FROM mercados_personalizados WHERE id = ?",
        (mercado_id,)
    )

    conn.commit()
    conn.close()


def salvar_preco_personalizado(produto_id, mercado_id, valor):
    valor = (valor or "").strip().replace(",", ".")

    conn = conectar()
    cur = conn.cursor()

    if not valor:
        cur.execute("""
            DELETE FROM precos_personalizados
            WHERE produto_id = ? AND mercado_id = ?
        """, (produto_id, mercado_id))
    else:
        try:
            preco = float(valor)
            if preco < 0:
                raise ValueError
        except ValueError:
            conn.close()
            raise ValueError("Digite um preço válido.")

        cur.execute("""
            INSERT INTO precos_personalizados
                (produto_id, mercado_id, preco)
            VALUES (?, ?, ?)
            ON CONFLICT(produto_id, mercado_id)
            DO UPDATE SET preco = excluded.preco
        """, (produto_id, mercado_id, preco))

    conn.commit()
    conn.close()


def carregar_precos_personalizados():
    conn = conectar()
    cur = conn.cursor()
    cur.execute("""
        SELECT produto_id, mercado_id, preco
        FROM precos_personalizados
    """)
    dados = cur.fetchall()
    conn.close()
    return dados
