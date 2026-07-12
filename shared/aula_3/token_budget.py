def estimate_tokens(text, model_name="gpt-4o-mini"):
    try:
        import tiktoken
        encoding = tiktoken.encoding_for_model(model_name)
        return len(encoding.encode(text))
    except Exception:
        return max(1, round(len(text.split()) * 1.3))
