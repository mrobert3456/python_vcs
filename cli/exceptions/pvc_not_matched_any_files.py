class PVCNotMatchedAnyFiles(Exception):
    def __init__(self, file_name):
        message = f"error: {file_name} did not mached any files or files are not modified"
        super().__init__(message)