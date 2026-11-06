

def gerar_lista(produtos, mercados):
        
    lista_compras = {}

    for mercado in mercados:
        lista_compras[mercado] = []

    for produto, mercado_produto in produtos.items():
        
        menor_preco = float('inf') 
        melhor_mercado = "" 


        for mercado, campo in mercado_produto.items():
            if campo.value == "":
                continue
                
            preco = float(campo.value.replace(",", "."))
            if preco < menor_preco:
                menor_preco = preco
                melhor_mercado = mercado

        if melhor_mercado != "":
            lista_compras[melhor_mercado].append(produto)

    return lista_compras