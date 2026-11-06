import flet as ft

from database import (adicionar_mercado, carregar_precos_personalizados,
                      carregar_produtos_mercados, excluir_mercado,
                      excluir_tabela_mercado, listar_mercados,
                      salvar_preco_personalizado, salvar_produto_mercado)
from mercado_lista import gerar_lista


def mostrar_mercado(ui, page, e=None):

    txt_produto = ft.TextField(
        label="Produto",
        width=230,
    )

    txt_mercado = ft.TextField(
        label="Novo Mercado",
        width=230,
    )

    resultado = ft.Column()
    produtos = {}
    precos_salvos = {
        (produto_id, mercado_id): preco 
        for produto_id, mercado_id, preco in carregar_precos_personalizados()
    }
    mercados = listar_mercados()

    tabela = ft.DataTable(
        columns=[
            ft.DataColumn(
                ft.Container(
                    content=ft.Text("Produto"),
                    width=170,
                )
            )
            
        ],
        rows=[],
        column_spacing=12,
    )

    
    def confirmar_exclusao_mercado(mercado_id, nome_mercado):
        def apagar(e):
            excluir_mercado(mercado_id)
            page.pop_dialog()
            mostrar_mercado(ui, page)

        def cancelar(e):
            page.pop_dialog()

        dialogo_excluir = ft.AlertDialog(
            modal=True,
            title=ft.Text("Excluir mercado"),
            content=ft.Text(
                f"Deseja excluir o mercado '{nome_mercado}'? "
                "Os preços desse mercado também serão apagados."
            ),
            actions=[
                ft.Button("Cancelar", on_click=cancelar),
                ft.Button("Excluir", on_click=apagar),
            ],
        )
        page.show_dialog(dialogo_excluir)


    for mercado_id, nome in mercados:
        tabela.columns.append(
            ft.DataColumn(
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    nome,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                width=85,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.CLOSE,
                                tooltip="Excluir mercado",
                                icon_size=16,
                                on_click=lambda e, mid=mercado_id, nm=nome:
                                    confirmar_exclusao_mercado(mid, nm),
                            ),
                        ],
                        spacing=2,
                        tight=True,
                    ),
                    width=150,
                )

            )
        )

    def criar_linha(produto_id, nome_produto):
        produtos[nome_produto] = {}

        celulas = [
            ft.DataCell(
                ft.Container(
                    content=ft.Text(nome_produto, max_lines=2, overflow=ft.TextOverflow.ELLIPSIS),
                    width=170,
                )
            )
        ]


        for mercado_id, nome_mercado in mercados:
            valor = precos_salvos.get((produto_id, mercado_id), "")
            campo = ft.TextField(
                value="" if valor is None else str(valor).replace(".", ","),
                width=100,
                dense=True,
                keyboard_type=ft.KeyboardType.NUMBER,
                )

            produtos[nome_produto][nome_mercado] = campo
            celulas.append(
                ft.DataCell(campo)
            )



            def salvar_ao_sair(e, pid=produto_id, mid=mercado_id, controle=campo):
                try:
                    salvar_preco_personalizado(pid, mid, controle.value)
                    controle.error_text = None
                except ValueError:
                    controle.error_text = "Preço inválido"
                page.update()

            campo.on_blur = salvar_ao_sair

        tabela.rows.append(ft.DataRow(cells=celulas))



    def adicionar_produto(e):
        nome = (txt_produto.value or "").strip()

        if not nome:
            return

        salvar_produto_mercado(
            nome, None, None, None, None, None, None, None
        )
        txt_produto.value = ""
        mostrar_mercado(ui, page)

    def adicionar_novo_mercado(e):
        nome = (txt_mercado.value or "").strip()
        sucesso, mensagem = adicionar_mercado(nome)

        if sucesso:
            txt_mercado.value = ""
            mostrar_mercado(ui, page)
        else:
            aviso.value = mensagem
            page.update()

    def clicar_gerar_lista(e):
        lista = gerar_lista(produtos, [nome for _, nome in mercados])
        resultado.controls.clear()
        resultado.controls.append(
            ft.Text(
                "Lista de compras",
                size=22,
                weight=ft.FontWeight.BOLD,
            )
        )

        for _, mercado in mercados:
            resultado.controls.append(
                ft.Text(
                    f"🛒 {mercado}",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                )
            )
            for produto in lista[mercado]:
                resultado.controls.append(ft.Text(f" - {produto}"))

        page.update()

    def limpar_tabela(e):
        excluir_tabela_mercado()
        resultado.controls.clear()
        page.pop_dialog()
        mostrar_mercado(ui, page)

    def fechar_dialogo(e):
        page.pop_dialog()

    def confirmar_limpeza(e):
        page.show_dialog(dialogo)

    dialogo = ft.AlertDialog(
        modal=True,
        title=ft.Text("Limpar tabela"),
        content=ft.Text(
            "Deseja apagar todos os produtos e preços? "
            "Os mercados cadastrados serão mantidos."
        ),
        actions=[
            ft.Button("Cancelar", on_click=fechar_dialogo),
            ft.Button("Apagar", on_click=limpar_tabela),
        ],
    )

    btn_produto = ft.Button(
        "Adicionar produto",
        on_click=adicionar_produto,
    )
    btn_mercado = ft.Button(
        "Adicionar mercado",
        on_click=adicionar_novo_mercado,
    )
    btn_gerar = ft.Button(
        "Gerar lista",
        on_click=clicar_gerar_lista,
    )
    btn_limpar = ft.Button(
        "Limpar tabela",
        on_click=confirmar_limpeza,
    )

    aviso = ft.Text()

    dados = carregar_produtos_mercados()
    for registro in dados:
        criar_linha(registro[0], registro[1])

    ui.conteudo.controls.clear()
    ui.conteudo.controls.append(
        ft.Text("🛒 Mercado", size=25, weight=ft.FontWeight.BOLD)
    )
    ui.conteudo.controls.append(
        ft.Row([txt_produto, btn_produto], wrap=True)
    )
    ui.conteudo.controls.append(
        ft.Row([txt_mercado, btn_mercado], wrap=True)
    )
    ui.conteudo.controls.append(
        ft.Row([btn_gerar, btn_limpar], wrap=True)
    )
    ui.conteudo.controls.append(aviso)
    ui.conteudo.controls.append(
        ft.Row(
            controls=[tabela],
            scroll=ft.ScrollMode.ALWAYS,
        )
    )
    ui.conteudo.controls.append(ft.Divider())
    ui.conteudo.controls.append(resultado)
    page.update()
