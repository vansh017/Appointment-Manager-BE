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
MAX_FAILED_LOGIN_FOR_USER = 5
MAX_OTP_REQUEST_PER_HR = 5
OTP_EXPIRATION_TIME = 10 * 60