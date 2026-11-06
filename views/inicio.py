import flet as ft

from ui import UI


def mostrar_inicio(
        ui: UI,
        page,
        e=None
):
        ui.conteudo.controls.clear()
        ui.conteudo.controls.extend([
            ft.Text(
                "🏠 Início",
                size=25,
                weight=ft.FontWeight.BOLD,
                ),

            ft.Divider(),
                ui.barra_mes,

            ft.Divider(),
                ui.txt_saldo,

            ft.Row(
                [
                    #ui.txt_receitas, (receita não aparece na tela de inicio)
                    ui.txt_despesas
                ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                ),

            ft.Divider(),

            ui.dropdown_tipo,

            ui.txt_categoria,

            ui.txt_valor,

            ui.txt_forma_de_pagamento,

            ui.txt_parcelas,

            ui.btn_adicionar,

            ft.Divider(),

            ft.Text(
                "Histórico",
                size=20,
                weight=ft.FontWeight.BOLD
                ),
            ui.lista_historico,
        ])


        page.update()