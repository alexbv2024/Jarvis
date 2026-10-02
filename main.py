import os
import subprocess
from pathlib import Path


#Files and OS functions
def listdir(dirname: str):
    p = subprocess.check_output(['mdfind', '-name', dirname], text=True).strip()
    if(p!=""):
        for i in p.split('\n'):
            if(os.path.isdir(i)):
                return os.listdir(i)
        return "error: listdir not working"
    else:
        return "error: listdir not working"

def readtxtfile(filename: str):
    p = subprocess.check_output(['mdfind', '-name', filename], text=True).strip()
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isfile(i)):
                return Path(i).read_text(encoding="utf-8", errors="ignore")
        return "error: readtxtfile not working"
    else:
        return "error: readtxtfile not working"

def writefile(filename: str, content: str):
    p = subprocess.check_output(['mdfind', '-name', filename], text=True).strip()
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
    p = subprocess.check_output(['mdfind', '-name', filename], text=True).strip()
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
    p = subprocess.check_output(['mdfind', '-name', filename], text=True).strip()
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isfile(i)):
                os.remove(i)
                return f"success: deleted file {filename}"
        return "error: deletefile not working"
    else:
        return "error: deletefile not working"

def deletedir(dirname: str):
    p = subprocess.check_output(['mdfind', '-name', dirname], text=True).strip()
    if (p != ""):
        for i in p.split('\n'):
            if (os.path.isdir(i)):
                os.rmdir(i)
                return f"success: deleted dir {dirname}"
        return "error: deletedir not working"
    else:
        return "error: deletedir not working"