import flet as ft


def criar_menu(
        page,
        abrir_inicio,
        abrir_investimentos,
        abrir_despesas,
        abrir_mercado
):
    # Menu lateral
    drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Text(
                    "Menu",
                    size=22,
                    weight=ft.FontWeight.BOLD
                ),
                padding=20
            ),

            ft.Divider(),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.HOME),
                title=ft.Text("Início"),
                on_click=abrir_inicio,
    ),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.SAVINGS),
                title=ft.Text("Investimentos"),
                on_click=abrir_investimentos,
            ),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.HOUSE),
                title=ft.Text("Despesas"),
                on_click=abrir_despesas
            ),

            ft.ListTile(
                leading=ft.Icon(ft.Icons.SHOPPING_CART),
                title=ft.Text("Mercado"),
                on_click=abrir_mercado
            ),
        ]
    )
    page.drawer = drawer

    return drawer