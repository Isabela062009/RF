import flet as ft


# Resumo financeiro
def criar_resumo():
     
    txt_receitas = ft.Text(
        "Receitas: R$ 0,00",
        size=16,
        color=ft.Colors.GREEN
    )
     
    txt_despesas = ft.Text(
        "Despesas: R$ 0,00",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.RED
    )

    txt_saldo = ft.Text(
        "Saldo: R$ 0,00",
        size=20,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE
    )

    return txt_receitas, txt_despesas, txt_saldo

def criar_formulario():

    dropdown_tipo = ft.Dropdown(
        label="Tipo",
        options=[
            ft.dropdown.Option("Receita"),
            ft.dropdown.Option("Despesa"),

        ],
        value="Despesa",
    )
    txt_categoria = ft.TextField(label="Categoria (ex: Almoço, Salário)")
    txt_valor = ft.TextField(label="Valor (R$)", keyboard_type=ft.KeyboardType.NUMBER)
    txt_parcelas = ft.TextField(
          label="Parcelas",
          value="1",
          keyboard_type = ft.KeyboardType.NUMBER
    )

    txt_forma_de_pagamento = ft.Dropdown(
          label="Forma de pagamento",
          value="Crédito",
          options=[
                ft.dropdown.Option("Crédito"),
                ft.dropdown.Option("Débito"),
                ft.dropdown.Option("Pix"),
                ft.dropdown.Option("Dinheiro"),
                ft.dropdown.Option("Transferência"),
          ]
    )
    return dropdown_tipo, txt_categoria, txt_forma_de_pagamento, txt_parcelas, txt_valor

def criar_btn_adicionar(on_click):

    return ft.Button(
        "Adicionar",
        on_click=on_click,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_600, color=ft.Colors.WHITE),
    )

def criar_lista_historico():
    
    lista = ft.ListView(
        expand=1,
        spacing=10,
        padding=10
    )
    return lista

