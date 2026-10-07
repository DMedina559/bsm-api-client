from enum import StrEnum


class APIErrorResponseCode(StrEnum):
    APPLICATION_ERROR = "application_error"
    CONFLICT = "conflict"
    FORBIDDEN = "forbidden"
    HTTP_ERROR = "http_error"
    INTERNAL_ERROR = "internal_error"
    INVALID_SERVER_NAME = "invalid_server_name"
    NOT_FOUND = "not_found"
    OPERATION_CANCELED = "operation_canceled"
    SERVER_ERROR = "server_error"
    SERVER_START_FAILED = "server_start_failed"
    SERVER_STOP_FAILED = "server_stop_failed"
    UNAUTHORIZED = "unauthorized"
    VALIDATION_ERROR = "validation_error"

    def __str__(self) -> str:
        return str(self.value)
