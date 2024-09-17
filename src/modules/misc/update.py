import stat
import os
import requests
import zipfile
import shutil
from io import BytesIO
from modules.misc.messageBox import msgBox
def update(t = "e"):
    protectedFiles = ["settings", ".git"] #files/folders that should not be replaced
    destination = os.getcwd().replace("/src","") #the target folder to replace the files. Should be the parent directory of the /src folder
    
    link = "https://github.com/existancepy/bss-macro-py/archive/master.zip"
    source = f"{destination}/bss-macro-py-main"
    e_macroPath = f"{destination}/e_macro.command"
    
    if t == "e":
        link = "https://github.com/existancepy/bss-macro-py-experimental/archive/master.zip"
        source = f"{destination}/bss-macro-py-experimental-main"

    print(os.listdir(destination))
    #delete all files
    for f in os.listdir(destination):
        if f in protectedFiles: continue
        if "." in f:
            os.remove(f"{destination}/{f}")
        else:
            shutil.rmtree(f"{destination}/{f}")

    #download new files
    req = requests.get(link)
    zipf= zipfile.ZipFile(BytesIO(req.content))
    zipf.extractall(destination)
    files = os.listdir(source)
    
    #move the files from the download folder to the source folder
    for file in files: 
        if file in protectedFiles: continue
        file_name = os.path.join(source, file) 
        shutil.move(file_name, destination) 
    print("Files Moved")

    #delete the download folder
    shutil.rmtree(source)
    
    #set execute permission for e_macro.command
    st = os.stat(e_macroPath)
    os.chmod(e_macroPath, st.st_mode | stat.S_IEXEC)
    
    msgBox("Update success", "Update complete. You can now relaunch the macro")
