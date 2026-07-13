from datetime import datetime


def transformar_pedido(pedido):
    """Transforma um pedido validado para o formato analítico.

    Esta função assume que `order_total` já é numérico e que `created_at` está
    em formato ISO-8601. Essas hipóteses são úteis para discutir contratos
    entre validação e transformação.
    """
    return {
        "order_id": pedido["order_id"],
        "customer_id": pedido["customer_id"],
        "order_total": float(pedido["order_total"]),
        "created_date": datetime.fromisoformat(
            pedido["created_at"].replace("Z", "+00:00")
        ).date().isoformat(),
        "items_count": len(pedido["items"]),
    }
