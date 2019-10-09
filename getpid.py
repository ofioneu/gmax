import os
import subprocess
import psutil
name = "java.exe"


ls = []
for p in psutil.process_iter(attrs=["name", "exe"]):
    if name == p.info['name'] or p.info['exe'] and os.path.basename(p.info['exe']) == name:
        ls.append(p)
        a=p.pid
        psutil.Process(a).kill()
        
        