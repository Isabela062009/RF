from dataclasses import dataclass
from datetime import datetime

import flet as ft


@dataclass

class UI:
    conteudo: ft.Column 
    txt_receitas: ft.Text
    txt_despesas: ft.Text
    txt_saldo: ft.Text
    dropdown_tipo: ft.Dropdown
    txt_categoria: ft.TextField
    txt_valor: ft.TextField
    txt_forma_de_pagamento: ft.Dropdown
    txt_parcelas: ft.TextField
    btn_adicionar: ft.Control
    lista_historico: ft.ListView
    barra_mes: ft.Row
    calendario: "Calendario"

    
class Calendario:
    def __init__(self):
        hoje = datetime.now()
        self.mes = hoje.month
        self.ano = hoje.year
