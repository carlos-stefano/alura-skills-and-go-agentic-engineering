import pytest

from mini_orders_pipeline.validacao_schema import validar_pedido


def pedido_valido():
    return {
        "order_id": "ORD-001",
        "customer_id": "CUST-123",
        "order_total": 99.9,
        "created_at": "2026-07-08T10:00:00Z",
        "items": [{"sku": "A12", "quantity": 1}],
    }


def test_pedido_valido_deve_passar():
    assert validar_pedido(pedido_valido()) is True


def test_customer_id_vazio_deve_falhar():
    pedido = pedido_valido()
    pedido["customer_id"] = ""

    with pytest.raises(ValueError):
        validar_pedido(pedido)
