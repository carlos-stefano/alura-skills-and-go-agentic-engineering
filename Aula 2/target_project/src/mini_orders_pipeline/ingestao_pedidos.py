from mini_orders_pipeline.validacao_schema import validar_pedido
from mini_orders_pipeline.transformacao_pedidos import transformar_pedido


def processar_lote_pedidos(pedidos_brutos):
    """Processa um lote de pedidos brutos.

    Implementação propositalmente simples para fins didáticos.
    """
    pedidos_processados = []

    for pedido in pedidos_brutos:
        validar_pedido(pedido)
        pedidos_processados.append(transformar_pedido(pedido))

    return pedidos_processados
