from .config import BANNER, AMARELO, CIANO, CINZA, RESET
from .logger import log
from .server import C2
from .commands import COMANDOS


def loop():
    c2 = C2()

    print(BANNER)
    log(
        f"configurado: LHOST={AMARELO}{c2.opcoes['LHOST']}{RESET}{CINZA} "
        f"LPORT={AMARELO}{c2.opcoes['LPORT']}{RESET}",
        CIANO,
    )
    log("use 'help' para comandos, 'run' para iniciar o listener", CINZA)

    while c2.rodando:
        c2.prompt()
        try:
            linha = input()
        except (EOFError, KeyboardInterrupt):
            break

        if not linha.strip():
            continue

        cmd, _, args = linha.partition(" ")
        cmd = cmd.lower()

        if cmd in ("exit", "quit"):
            break
        elif cmd in ("run", "start", "exploit"):
            c2.iniciar_listener()
        elif cmd == "stop":
            c2.parar_listener()
        elif cmd == "background":
            c2.ativo = None
            log("sessao em background", CINZA)
        elif cmd in COMANDOS:
            COMANDOS[cmd](c2, args)
        else:
            c2.enviar(linha)

    c2.encerrar()


if __name__ == "__main__":
    loop()
