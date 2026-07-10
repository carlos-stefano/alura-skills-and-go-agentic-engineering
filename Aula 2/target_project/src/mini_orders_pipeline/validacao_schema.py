CAMPOS_OBRIGATORIOS = [
    "order_id",
    "customer_id",
    "order_total",
    "created_at",
    "items",
]


def validar_pedido(pedido):
    """Valida minimamente um pedido.

    Esta função contém uma fragilidade didática: ela acessa campos diretamente
    durante as validações. Quando um campo obrigatório está ausente, o erro
    resultante pode ser um KeyError genérico em vez de um erro estruturado
    com contexto sobre o campo ausente.
    """
    if not pedido["order_id"]:
        raise ValueError("order_id vazio")

    if not pedido["customer_id"]:
        raise ValueError("customer_id vazio")

    if pedido["order_total"] <= 0:
        raise ValueError("order_total deve ser positivo")

    if not pedido["created_at"]:
        raise ValueError("created_at vazio")

    if len(pedido["items"]) == 0:
        raise ValueError("pedido sem itens")

    return True
