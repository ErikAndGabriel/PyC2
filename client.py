import threading


class Client:
    def __init__(self, conn, addr, cid):
        self.conn = conn
        self.addr = addr
        self.id = cid
        self.lock = threading.Lock()
        self.arquivo = None
        self.arquivo_nome = None
        self.arquivo_tamanho = 0
        self.arquivo_recebido = 0
        self.buffer = b""

    def enviar(self, texto):
        with self.lock:
            try:
                self.conn.sendall((texto + "\n").encode())
                return True
            except Exception:
                return False

    def fechar(self):
        try:
            self.conn.close()
        except Exception:
            pass
