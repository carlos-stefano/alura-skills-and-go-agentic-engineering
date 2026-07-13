from mini_orders_pipeline.transformacao_pedidos import transformar_pedido


def test_transformar_pedido_valido():
    pedido = {
        "order_id": "ORD-001",
        "customer_id": "CUST-123",
        "order_total": 99.9,
        "created_at": "2026-07-08T10:00:00Z",
        "items": [{"sku": "A12", "quantity": 1}],
    }

    transformado = transformar_pedido(pedido)

    assert transformado["order_total"] == 99.9
    assert transformado["created_date"] == "2026-07-08"
    assert transformado["items_count"] == 1
