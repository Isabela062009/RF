from datetime import datetime

import flet as ft

from ui import Calendario

calendario = Calendario()

def atualizar_valores(
        txt_receitas, 
        txt_despesas, 
        txt_saldo, 
        lista_historico,
        conectar, 
        mes,
        ano,
        page
        ):

    conn = conectar()
    cur = conn.cursor()
    # Calcula receitas
    cur.execute("""
           SELECT COALESCE(SUM(valor),0) 
           FROM transacoes 
           WHERE tipo='Receita'
           AND substr(data,4,2)=?
           AND substr(data,7,4)=?
           """,(f"{mes:02d}", str(ano))
        )
    receitas = cur.fetchone()[0]
   # Calcula despesas
    cur.execute("""
    SELECT COALESCE(SUM(valor),0) 
    FROM transacoes 
    WHERE tipo='Despesa'
    AND substr(data,4,2)=?
    AND substr(data,7,4)=?
        """, (f"{mes:02d}", str(ano))
                )
    despesas = cur.fetchone()[0]

    saldo = receitas - despesas

    # Atualiza resumo
    txt_receitas.value = f"Receitas: R$ {receitas:.2f}"
    txt_despesas.value = f"Despesas: R$ {despesas:.2f}"
    txt_saldo.value = f"Saldo: R$ {saldo:.2f}"
    txt_saldo.color = ft.Colors.BLUE if saldo >= 0 else ft.Colors.RED

        # Atualiza histórico
    lista_historico.controls.clear()

    cur.execute("""
        SELECT id, data, valor, tipo, categoria, parcelas, parcela_atual, compra_id
        FROM transacoes
        WHERE substr(data,4,2)=?
            AND substr(data,7,4)=?
        ORDER BY id DESC
        """, (f"{mes:02d}", str(ano))
        )
    rows = cur.fetchall()


    for tid, data, valor_db, tp, cat, parcelas, parcela_atual, compra_id in rows:
            
            valor_exibido = valor_db

            def excluir(e, grupo=compra_id):
                c = conectar()
                cu = c.cursor()
                cu.execute(
                     "DELETE FROM transacoes WHERE compra_id=?",
                       (grupo,)
                    )
                c.commit()
                c.close()

                fechar_dialogo(e)

                atualizar_valores(
                     txt_receitas,
                     txt_despesas,
                     txt_saldo,
                     lista_historico,
                     conectar,
                     mes,
                     ano,
                     page
                )

            def fechar_dialogo(e):
                page.pop_dialog()

            def confirmar_limpeza(e):
                page.show_dialog(dialogo)



            dialogo = ft.AlertDialog(
                modal=True,
                title=ft.Text("Excluir do Histórico"),
                content=ft.Text(
                    "Deseja realmente apagar esta ação?"
                ),
                actions=[
                    ft.Button(
                        "Cancelar",
                        on_click=fechar_dialogo,
                    ),
                    ft.Button(
                        "Apagar",
                        on_click=excluir,
                    ),
                ],
            )

            lista_historico.controls.append(
                ft.ListTile(
                    title=ft.Text(cat),
                    subtitle=ft.Text(f"{data} | {tp}"),
                    trailing=ft.Row(
                        [
                            ft.Text(
                                f"{'+' if tp=='Receita' else '-'} R$ {valor_exibido:.2f}" + (f" ({parcela_atual}/{parcelas})" if parcelas > 1 else "")
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                on_click=confirmar_limpeza,
                            )
                        ],
                        tight=True
                    )
                )
            )

    conn.close()
    page.update()

