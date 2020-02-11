def error_responses(model: str):
    return dict({
        404: {
            "description": f"{model} Not Found"
        }
    })
