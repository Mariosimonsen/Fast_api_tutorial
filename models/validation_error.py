class ValidationError(Exception):
    def __init__(self, error_message: str, status_code: int):
        super().__init__(error_message)
        self.error_message = error_message
        self.status_code = status_code