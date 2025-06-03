class Logger:
    def __init__(self):
        pass
        
    def info(self, *args):
        print("[INFO]", *args)
        
    def error(self, *args):
        print("[ERROR]", *args)
        
    def debug(self, *args):
        print("[DEBUG]", *args)