AUTH_SCHEMA = {
    "type": "object",
    "properties": {
        "authenticated": {"type": "boolean"},
        "token": {"type": "string"}
    },
    "required": ["authenticated"],
    "additionalProperties": False
}

BEARER_SUCCESS_SCHEMA = {
    "type": "object",
    "properties": {
        "authenticated": {"type": "boolean"},
        "token": {"type": "string"}
    },
    "required": ["authenticated"],
    "additionalProperties": False
}
BEARER_ERROR_SCHEMA = {
    "type": "object",
    "properties": {
        "authenticated": {"type": "boolean"}
    },
    "required": ["authenticated"],
    "additionalProperties": False
}

HEADERS_SCHEMA = {
    "type": "object",
    "properties": {
        'headers' :{
            'type': 'object',
            'properties': {
                'User-Agent' : {'type': 'string'}
            },
            'required': ['User-Agent']
        }
    },
    "required": ["headers"],
    'additionalProperties': False
}

