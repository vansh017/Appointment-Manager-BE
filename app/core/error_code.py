"""
Description: File contains all the error codes that will be sent to client in case of
    any failure or exception
"""

"""
OAuth Error Codes: For any error that will be raised from OAuthLib while authorizing client
"""
oauth_error_description = {
    "default": "Unexpected Client Error - Undocumented",
    "token_expired": "Supplied token has expired",
    "missing_code": "Authorization Code is missing",
    "missing_token": "access_token or refresh_token is missing",
    "missing_token_type": "token type is missing",
    "invalid_request": "Invalid request",
    "access_denied": "The resource owner or authorization server denied the request.",
    "unsupported_response_type": "The authorization server does not support obtaining an authorization code using "
                                 "this method.",
    "invalid_scope": "The requested scope is invalid. Check scopes defined",
    "server_error": "The authorization server encountered an unexpected condition that prevented it from fulfilling "
                    "the request.",
    "temporarily_unavailable": "The authorization server is currently unable to handle the request due to a temporary "
                               "overloading or maintenance of the server.",
    "invalid_client": "Client authentication failed. Client Authorization header is not valid",
    "invalid_grant": "The provided authorization grant (e.g. authorization code, resource owner credentials) or "
                     "refresh token is invalid, expired or revoked",
    "unauthorized_client": "The authenticated client is not authorized to use supplied authorization grant type.",
    "unsupported_grant_type": "The authorization grant type is not supported by the authorization",
}


class ErrorMessages:
    """
    Constant Error Class for showing various types of errors in server

    """

    #  Prefix: CI_ 1XX1-1XXX => client related errors ------------------------------------------------------
    INVALID_CLIENT = dict(code=1001, description="invalid client")
    UNAUTHORIZED_CLIENT = dict(code=1002, description="unauthorized client")
    CI_NO_SV_USER = dict(code=1003, description="given service user not found")
    CI_NOT_AUTH_SCOPE = dict(code=1004, description="not authorized to access scopes")  # list of additional
    # scopes will be added in additional info
    # ------------------------------------------------------------------------------------

    # 2XX1-2XXX => user/facility/pharmacy/caretaker/patient related errors ----------------
    #   user: 20X1-20XX -----------------------------------------------------------------------------------------------
    INVALID_USER_CRED = dict(code=2001, description="invalid username or password")
    INVALID_USERNAME = dict(code=2002, description="invalid username provided")
    USER_ACC_INACTIVE = dict(code=2003, description="account is locked, follow password reset procedure")
    INSUFFICIENT_ROLES = dict(code=2004, description="invalid roles for request")
    INVALID_EMAIL = dict(code=2005, description="invalid email of the user")
    UNAUTHORIZED_ACCESS_TO_FACILITY = dict(code=2006, description="not authorized to access facility info")
    OTP_REQUEST_LIMIT_EXCEEDED = dict(code=2007, description="max OTP request reached in one hour")
    INVALID_OTP = dict(code=2008, description="invalid otp")
    USER_NOT_FOUND = dict(code=2009, description="user not found")
    EMAIL_NOT_AVAILABLE = dict(code=2010, description="email not available")
    EMAIL_REQUIRED = dict(code=2011, description="email required for the user")
    INVALID_PASSWORD = dict(
        code=2012, description="invalid password; password should be of min 8 characters, should contain at least one: "
                               "lowercase letter, uppercase letter, number and "
                               "one special character among: '! @ # $ % ^ & * ?'")
    OTP_EXPIRED = dict(code=2013, description="otp expired")
    FAILED_LOGIN_ATTEMPT_LIMIT_EXCEEDED = dict(code=2014, description="unsuccessful login limit exceeded for the user, "
                                                                      "follow password reset procedure")
    INVALID_OTP_LIMIT_EXCEEDED = dict(code=2015, description="otp submission limit exceeded for user, "
                                                             "follow password reset procedure")
    INVALID_NEW_PWD = dict(code=2016, description="new password cannot be one of the last three used passwords")
    RESET_TOKEN_LIMIT_EXCEEDED = dict(code=2017, description="max limit reached for password reset request, "
                                                             "try again after 24 hrs")
    PATIENT_NOT_FOUND_FACILITY = dict(code=2018, description="patient not found for given facility")
    USER_HAS_OTHER_ROLES = dict(code=2019, description="user already exists and has other roles assigned")
    ACCOUNT_INACTIVE = dict(code=2020, description="account is inactive")
    DETAILS_AL_VERIFIED = dict(code=2011, description="details already verified")

    #   pharmacy: 21X1-21XX ----------------------------------------------------------------------------------------


    # ---------------------------------------------------------------------------------------------------------------

    INTERNAL_SV_ERROR = dict(code=5001, description="internal server error")


    # -----------------------------------------------------------------------------------------

    REQUEST_IN_PROGRESS = dict(code=10011, description="Another Request is in progress.")
