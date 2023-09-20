class CustomException(Exception):
    def __init__(self, titulo="erro interno", detalhes=None, status_code=500, criar_log=True):
        
        self.detalhes = detalhes
        self.titulo = titulo
        self.status_code = status_code

class LogErroException(Exception):
    def __init__(self, titulo="erro ao registrar log no banco", detalhes=None, status_code=500, criar_log=True):
        
        self.detalhes = detalhes
        self.titulo = titulo
        self.status_code = status_code
