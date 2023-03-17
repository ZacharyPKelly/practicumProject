import subprocess
import os

installGH = os.path.expanduser('~')
installGH = installGH + "\scoop\shims\scoop install gh"

updateGH = os.path.expanduser('~')
updateGH = updateGH + "\scoop\shims\scoop update gh"

a = subprocess.run(["powershell", "-Command", installGH])
#a = subprocess.run(["powershell", "-Command", updateGH], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(a)