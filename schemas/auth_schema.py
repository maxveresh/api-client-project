AUTH_SUCCESS_SCHEMA = {
    "type": "object",
    "properties": {
        "authenticated": {"type": "boolean"},
        "token": {"type": "string"}
    },
    "required": ["authenticated", "token"],
    "additionalProperties": False
}