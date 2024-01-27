class PVCAlreadyInitializedException(Exception):
    def __init__(self, message="pvc is already initialized on this project"):
        super().__init__(message)

    