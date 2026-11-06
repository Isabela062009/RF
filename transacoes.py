import uuid
from datetime import datetime

from database import conectar


def salvar_transacao(
        valor,
        parcelas,
        tipo,
        categoria,
        forma_pagamento):

    conn = conectar()
    cur = conn.cursor()

    hoje = datetime.now()
    compra_id = str(uuid.uuid4())
    valor_parcela = valor / parcelas

    for i in range(parcelas):
        mes = hoje.month + i
        ano = hoje.year

        while mes > 12:
            mes -= 12
            ano += 1

        data = f"{hoje.day:02d}/{mes:02d}/{ano}"

        cur.execute(
            """
            INSERT INTO transacoes
            (data, valor, tipo, categoria, forma_pagamento, parcelas, parcela_atual, compra_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                data,
                valor_parcela,
                tipo,
                categoria,
                forma_pagamento,
                parcelas,
                i + 1,
                compra_id
            )
        )

    conn.commit()
    conn.close()

    

