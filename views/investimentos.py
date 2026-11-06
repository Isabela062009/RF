import flet as ft


def mostrar_investimentos(ui, page, e=None):

    aporte = ft.TextField(
        label="Valor do aporte",
        hint_text="Ex: 1000"
    )

    ivv = ft.Text("IVV (70%): R$ 0,00")
    vxus = ft.Text("VXUS (30%): R$ 0,00")

    def calcular_aporte(e):
        try:
            total = float(aporte.value.replace(",", "."))

            ivv.value = f"IVV (70%): R$ {total * 0.7:.2f}"
            vxus.value = f"VXUS (30%): R$ {total * 0.3:.2f}"

            page.update()

        except ValueError:
            pass

    aporte.on_change = calcular_aporte

    ui.conteudo.controls.clear()
    ui.conteudo.controls.extend(
         [   
                ft.Text(
                    "💰 Investimentos",
                    size=25,
                    weight=ft.FontWeight.BOLD
                ),

                aporte,
                ivv,
                vxus,

         ] 
    )


    page.update()

