class PVCNotInitializedException(Exception):
    def __init__(self, message="pvc is not initialized on this project. Run 'python main.py init'"):
        super().__init__(message)