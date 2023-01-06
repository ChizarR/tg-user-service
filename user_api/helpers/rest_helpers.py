from typing import Any, Dict, NamedTuple


class ApiResponseStatus:
    OK = "ok"
    ERROR = "error"
    NO_CONTENT = "no_content"


class ApiResponse(NamedTuple):
    status: str
    message: str | None = None
    result: Any | None = None

    def to_dict(self) -> Dict:
        return {
            "status": self.status,
            "message": self.message,
            "result": self.result,
        }


