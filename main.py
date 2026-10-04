import os
import subprocess
import time
from pathlib import Path
import shutil
from datetime import datetime
import psutil
import socket
import platform

import send2trash


#Files and OS functions

def pathr(name: str):
    e=os.path.expanduser(name)
    if(os.path.exists(e)):
        return e
    homedir=os.path.expanduser('~')
    comdir=os.path.join(homedir,name)
    if (os.path.exists(comdir)):
        return comdir
    p = subprocess.check_output(['mdfind', '-name', name], text=True, stderr=subprocess.DEVNULL).strip()
    if (p != ""):
        for i in p.split('\n'):
            ignlist=[
                        '/System/',
                        '/Library/',
                        '/usr/',
                        '/.idea',
                        '/Caches/',
                        '/.venv',
                        '/.git',
                        '/Mobile Documents/',
                ]
            if(not i in ignlist):
                pass


            if (os.path.exists(i)):
                return i

def listdir(dirname: str):
    p = pathr(dirname)
    if(p!=""):
        for i in p.split('\n'):
            if(os.path.isdir(i)):
                return os.listdir(i)
        return "error: listdir not working"
    else:
        return "error: listdir not working"

def readtxtfile(filename: str):
    p = pathr(filename)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isfile(i)):
                return Path(i).read_text(encoding="utf-8", errors="ignore")
        return "error: readtxtfile not working"
    else:
        return "error: readtxtfile not working"

def writefile(filename: str, content: str):
    p = pathr(filename)
    if(p!=""):
        for i in p.split('\n'):
            if(os.path.isfile(i)):
                with Path(i).open(mode="w", encoding="utf-8") as f:
                    f.write(content)
                return f"success: wrote content"
        return "error: writefile not working"
    else:
        with Path(filename).open(mode="w", encoding="utf-8") as f:
            f.write(content)
        return f"success: created new {filename} and wrote content"

def appendfile(filename: str, content: str):
    p = pathr(filename)
    if(p!=""):
        for i in p.split('\n'):
            if(os.path.isfile(i)):
                with Path(i).open("a", encoding="utf-8") as f:
                    f.write(content)
                return f"success: appended content"
        return "error: appendfile not working"
    else:
        with Path(filename).open("a", encoding="utf-8") as f:
            f.write(content)
        return f"success: created new {filename} and appended content"

def deletefile(filename: str):
    p = pathr(filename)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isfile(i)):
                delthing(i)
                return f"success: deleted file {filename}(sended it to the trash)"
        return "error: deletefile not working"
    else:
        return "error: deletefile not working"

def deletedir(dirname: str):
    p = pathr(dirname)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isdir(i)):
                os.rmdir(i)
                return f"success: deleted dir {dirname}"
        return "error: deletedir not working"
    else:
        return "error: deletedir not working"

def renames(name: str,newn: str):
    p = pathr(name)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isdir(i) or os.path.isfile(i)):
                np=Path(i).parent / newn
                os.rename(i,np)
                return f"success: renamed file {name} into {newn}"
        return "error: renames not working"
    else:
        return "error: renames not working"

def moves(name: str,newp: str):
    p = pathr(name)
    np = pathr(newp)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isdir(i) or os.path.isfile(i)):
                if (np != ""):
                    for j in np.split('\n'):
                        if (os.path.isdir(j)):
                            shutil.move(i, j)
                            return f"success: moved file {name} into {newp}"
                    return "error: moves not working"
                else:
                    return "error: moves not working"
        return "error: moves not working"
    else:
        return "error: moves not working"

def copydirorf(name: str, newp: str):
    p = pathr(name)
    np = pathr(newp)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.exists(i)):
                if (np != ""):
                    for j in np.split('\n'):
                        if(os.path.isdir(j)):
                            if (os.path.isdir(i)):
                                dp=os.path.join(j, os.path.basename(i))
                                shutil.copytree(i, dp, dirs_exist_ok=True)
                                return f"success: copied dir {name} into {newp}"
                            elif (os.path.isfile(i)):
                                shutil.copy(i, j)
                                return f"success: copied file {name} into {newp}"
                    return "error: copydirorf not working"
                else:
                    return "error: copydirorf not working"
        return "error: copydirorf not working"
    else:
        return "error: copydirorf not working"

def metastats(name: str):
    p = pathr(name)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.exists(i)):
                stats=os.stat(i)
                statde=[]

                for attr in dir(stats):
                    if attr.startswith("st_"):
                        v=getattr(stats, attr)
                        if(attr in ('st_mtime','st_atime','st_ctime','st_birthtime')):
                            dt = datetime.fromtimestamp(v)
                            formatted = dt.strftime(
                                '%Y-%m-%d %H:%M:%S (An: %Y)'
                            )
                            statde.append(
                                f'{attr}: {formatted} [{v}]'
                            )
                        elif(attr=='st_size'):
                            kb = round(v/1024,2)
                            mb = round(v / (1024*1024), 2)
                            statde.append(
                                f'{attr}: {v} bytes ({kb} KB / {mb} MB)'
                            )
                        else:
                            statde.append(
                                f'{attr}: {v}'
                            )
                output = f"success: full stat metadata for '{i}':\n" + '\n'.join(
                    statde
                )
                return output
        return "error: metastats not working"
    else:
        return "error: metastats not working"

def compress(dirname: str):
    p = pathr(dirname)
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isdir(i)):
                pdir=os.path.dirname(i)
                bdir = os.path.basename(i)
                archive=os.path.join(pdir,bdir)
                shutil.make_archive(archive,'zip',pdir,bdir)
                return f"succes: compressed {dirname}"
        return "error: compress not working"
    else:
        return "error: compress not working"

#Monitor the System and Hardware

def syscpuramusage():
    usage={
        "cpu%":psutil.cpu_percent(interval=0.1),
        "ram":round(psutil.virtual_memory().used/1024**3,2),
        "ram%": psutil.virtual_memory().percent
    }
    return usage

def diskusage():
    list=[]
    p=psutil.disk_partitions()
    for i in range(0,len(p)):
        list.append(round(psutil.disk_usage(psutil.disk_partitions()[i].mountpoint).used / 1024**3,2))
        list.append(round(psutil.disk_usage(psutil.disk_partitions()[i].mountpoint).free / 1024**3,2))
    return list

def lsprosses():
    p=psutil.process_iter(['pid','name','cpu_percent','memory_percent'])
    l=[]
    for i in p:

        try:
            if(i.pid!=0):
                l.append(i.info)

        except Exception:
            pass
    return l

def battery():
    batt=psutil.sensors_battery()
    if(batt!=None):
        return [batt.percent,batt.power_plugged]
    else:
        return "error: battery not working"

def netinfo():
    l1=psutil.net_if_addrs()
    l2 = psutil.net_if_stats()
    r=[]
    mac=0
    for n,i in l1.items():
        ip=None

        for j in i:
            if(j.family==socket.AF_INET):
                r.append(n)
                r.append(j.address)
                ip=j.address
            elif (j.family == psutil.AF_LINK and mac==0):
                r.append(j.address)
                mac+=1
        if(ip):
            if(n in l2):
                r.append(l2[n].isup)
                if(l2[n].speed!=0):
                    r.append(l2[n].speed)
                else:
                    r.append("N/A")

    return r

def whatos():
    return platform.platform()

def delthing(name: str):
    p=pathr(name)
    send2trash.send2trash(p)
    return f"succes: deleted {name} (moved to trash for safety)"

def guptime():
    uptime=time.time()-psutil.boot_time()
    return round(uptime,2)

