class PVCNotMatchedAnyFiles(Exception):
    def __init__(self, file_name):
        message = f"error: {file_name} did not mached any files"
        super().__init__(message)