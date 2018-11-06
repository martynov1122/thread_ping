#!/usr/bin/env python
from collections import deque
import queue
import csv
import datetime
import os
import re
import subprocess
import multiprocessing as mp
import time

def loadIPFiles():
  ip_files = []
  with open('ping_ip_address_list.csv', encoding="utf-16", errors='ignore') as file:
    reader = csv.reader(file)
    headers = next(reader) 
    for row in reader:
      client = row[1]
      ip = row[2]
      filename = client + '-' + ip + "-simple-ping" + '-' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ".txt"
      file = open(filename, "w+")
      file.close()
      ip_files.append({'ip': ip, 'file': filename, 'client': client})
  return ip_files

def pinger(ip_file):
  file = open(ip_file['file'], "a")
  """ test an IP address to see if it's up with one ping"""
  """ will feed this an array with mp.Pool.map() """
  IPup = []
  IPdown = []
  str = ''
  with open(os.devnull, "w") as fnull:
    if subprocess.call(['ping','-c 1', '-W 1',ip_file['ip'],],stdout=fnull, stderr=fnull)==0:
      str = '%s : %s : %s : UP\n' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip_file['client'], ip_file['ip'])
      print(str)
    else:
      str = '%s : %s : %s : DOWN\n' % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ip_file['client'], ip_file['ip'])
      print(str)
    file.write(str)
  # file.close()

# numThreads = 2 * mp.cpu_count()
numThreads = 20

ip_files = loadIPFiles()
p = mp.Pool(numThreads)


# """ IPout is a list of the devices that are UP """

while True:
  print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
  IPout = p.map(pinger, ip_files)
  time.sleep(3) # Delay for 1 minute (60 seconds).


p.close()
p.join()