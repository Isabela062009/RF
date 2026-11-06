from datetime import datetime

import flet as ft

from conta import atualizar_valores
from database import conectar, init_db
from transacoes import salvar_transacao
from ui import UI, Calendario
from views.componentes_inicio import (criar_btn_adicionar, criar_formulario,
                                      criar_lista_historico, criar_resumo)
from views.despesas import mostrar_despesas
from views.inicio import mostrar_inicio
from views.investimentos import mostrar_investimentos
from views.menu import criar_menu
from views.mercado import mostrar_mercado


def main(page: ft.Page):
    init_db()

    page.title = "Romero Finanças"


    meses = [
        "",
        "Janeiro",
        "Fevereiro",
        "Março",
        "Abril",
        "Maio",
        "Junho",
        "Julho",
        "Agosto",
        "Setembro",
        "Outubro",
        "Novembro",
        "Dezembro"
    ]

    calendario = Calendario()

    txt_mes = ft.Text(
        f"{meses[calendario.mes]}/{calendario.ano}",
        size=18,
        weight=ft.FontWeight.BOLD,
    )
    def atualizar_mes():
        txt_mes.value = f"{meses[calendario.mes]}/{calendario.ano}"
        
        atualizar_valores(        
             txt_receitas,
             txt_despesas,
             txt_saldo,
             lista_historico,
             conectar,
             calendario.mes,
             calendario.ano,
             page,
             )
        
        page.update()

    def proximo_mes(e):
        calendario.mes += 1

        if calendario.mes > 12:
            calendario.mes = 1
            calendario.ano += 1

        atualizar_mes()

    def mes_anterior(e):
        calendario.mes -= 1

        if calendario.mes < 1:
            calendario.mes = 12
            calendario.ano -= 1

        atualizar_mes()

    btn_anterior = ft.IconButton(
        icon=ft.Icons.ARROW_BACK,
        on_click=mes_anterior
    )

    btn_proximo = ft.IconButton(
        icon=ft.Icons.ARROW_FORWARD,
        on_click=proximo_mes
    )
   

    barra_mes = ft.Row(
        [
            btn_anterior,
            txt_mes,
            btn_proximo,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.vertical_alignment = ft.MainAxisAlignment.START
    page.padding = 16
    page.scroll = ft.ScrollMode.AUTO
    conteudo = ft.Column()
    # Resumo financeiro
    txt_receitas, txt_despesas, txt_saldo = criar_resumo()

    # Campos de entrada
    dropdown_tipo, txt_categoria, txt_forma_de_pagamento, txt_parcelas, txt_valor = criar_formulario()
    # Lista visual para mostrar o histórico na tela
    lista_historico = criar_lista_historico()

    def adicionar_transacao(e):
    
            if not txt_categoria.value or not txt_valor.value:
                return

            try:
                valor = float(txt_valor.value.replace(",", "."))
            except ValueError:
                return
            
            parcelas = int(txt_parcelas.value)

            salvar_transacao(
                valor,
                parcelas,
                dropdown_tipo.value,
                txt_categoria.value,
                txt_forma_de_pagamento.value
            )

            # Limpa os campos
            txt_categoria.value = ""
            txt_valor.value = ""
            txt_parcelas.value = "1"

            atualizar_valores(
            txt_receitas,
            txt_despesas,
            txt_saldo,
            lista_historico,
            conectar,
            calendario.mes,
            calendario.ano,
            page,
        )
            
    
    btn_adicionar = criar_btn_adicionar(adicionar_transacao)


    ui = UI(
    conteudo=conteudo,
    txt_receitas=txt_receitas,
    txt_despesas=txt_despesas,
    txt_saldo=txt_saldo,
    dropdown_tipo=dropdown_tipo,
    txt_categoria=txt_categoria,
    txt_valor=txt_valor,
    txt_parcelas=txt_parcelas,
    txt_forma_de_pagamento=txt_forma_de_pagamento,
    btn_adicionar=btn_adicionar,
    lista_historico=lista_historico,
    barra_mes=barra_mes,
    calendario=calendario,
    )

    def abrir_inicio(e=None):
        mostrar_inicio(
            ui,
            page,
        )

    def abrir_investimentos(e=None):
        mostrar_investimentos(
            ui,
            page,
            e,
        )

        

    def abrir_despesas(e=None):
        mostrar_despesas(
            ui,
            page,
        e,
    )

    def abrir_mercado(e=None):
        mostrar_mercado(
            ui,
            page,
            e,
        )


    page.drawer = criar_menu(
    page,
    abrir_inicio,
    abrir_investimentos,
    abrir_despesas,
    abrir_mercado,
    )

    # Barra superior
    page.appbar = ft.AppBar(
        title=ft.Text("Controle Financeiro"),
        center_title=True
    )

    # Conteúdo principal
    page.add(conteudo)

    # Tela inicial ao abrir
    abrir_inicio()

    atualizar_valores(
             txt_receitas,
             txt_despesas,
             txt_saldo,
             lista_historico,
             conectar,
             calendario.mes,
             calendario.ano,
             page,
        )


ft.run(main)


