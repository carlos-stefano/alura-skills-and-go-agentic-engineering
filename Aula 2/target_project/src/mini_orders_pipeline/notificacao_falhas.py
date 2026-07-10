def montar_notificacao_falha(incident_id, resumo, severidade):
    """Monta uma mensagem simples de falha para revisão humana."""
    return {
        "incident_id": incident_id,
        "severidade": severidade,
        "resumo": resumo,
        "acao": "revisar incidente e validar proposta antes de qualquer alteração",
    }
