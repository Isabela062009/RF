import flet as ft

from database import conectar

MESES = {
    "01": "Janeiro",
    "02": "Fevereiro",
    "03": "Março",
    "04": "Abril",
    "05": "Maio",
    "06": "Junho",
    "07": "Julho",
    "08": "Agosto",
    "09": "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro",
}

def abrir_mes(conteudo, page, mes, ano):
        conteudo.controls.clear()

        conteudo.controls.append(
            ft.Text(
                f"🏠 Despesas - {MESES[mes]}/{ano}",
                size=25,
                weight=ft.FontWeight.BOLD,
            )
        )
        tabela = ft.DataTable(
              columns=[
                    ft.DataColumn(ft.Text("Categoria")),
                    ft.DataColumn(ft.Text("Valor")),
                    ft.DataColumn(ft.Text("Pagamento")),
              ],
              rows=[]
        )
        conn = conectar()
        cur = conn.cursor()

        cur.execute("""
                SELECT categoria,
                    SUM(valor) as total,
                    forma_pagamento
                FROM transacoes
                WHERE tipo='Despesa'
                AND data LIKE ?
                GROUP BY categoria, forma_pagamento
                ORDER BY categoria
            """, (f"%/{mes}/{ano}",))

        for categoria, total, pagamento in cur.fetchall():

            tabela.rows.append(
                ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(categoria)),
                    ft.DataCell(ft.Text(f"R$ {total:.2f}")),
                    ft.DataCell(ft.Text(pagamento))
                ]
            )
        )
        conteudo.controls.append(tabela)
            

        conn.close()

        page.update()

def mostrar_despesas(ui, page, e=None,):
            ui.conteudo.controls.clear()
            ui.conteudo.controls.append(
                ft.Text(
                    "🏠 Despesas ",
                    size=25,
                    weight=ft.FontWeight.BOLD
                )
            )
            conn = conectar()
            cur = conn.cursor()

            cur.execute("""
            SELECT DISTINCT data
            FROM transacoes
            WHERE tipo='Despesa'
            ORDER BY data
            """)
            datas = cur.fetchall()
            conn.close()

            meses = []

            for (data,) in datas:
                  mes_num = data.split("/")[1]
                  ano = data.split("/")[2]


                  texto = f"{MESES[mes_num]}/{ano}"

                  if texto not in meses:
                        meses.append((texto, mes_num, ano))
            for texto, mes_num, ano in meses:
                  ui.conteudo.controls.append(
                        ft.Button(
                              texto,
                              width=250,
                              on_click=lambda e, m=mes_num, a=ano: abrir_mes(ui.conteudo, page, m, a)
                        )
                  )


            page.update()       