class DLCError(Exception):
    pass


class DeploymentError(DLCError):
    def __init__(self, code, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = code
