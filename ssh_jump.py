# -- coding: utf-8 --
import sys
from jumpssh import SSHSession
gateway_session = SSHSession('39.97.235.87','tanlei',port='2222', password='amtb791127').open()
#remote_session = gateway_session.get_remote_session('39.97.235.87','tanlei',port='2222', password='amtb791127')