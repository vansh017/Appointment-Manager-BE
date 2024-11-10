class OpenApiTags:
    AUTH = "auth"


    _TAGS_METADATA = [
        {
            "name": AUTH,
            "description": "Authorization Routes"
        },
    ]

    @classmethod
    def get_tags_metadata(cls):
        return OpenApiTags._TAGS_METADATA


ACCESS_TOKEN_EXPIRE_MINUTES = 30