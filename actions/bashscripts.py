import subprocess

#Wget ile ses dosyası indirme

def bash_wget(file_path: str, url: str):
    try:
        subprocess.run(["wget","-P",file_path,url],check=True)
    
    except subprocess.CalledProcessError as e:
        return {"subprocess_error": e} 
