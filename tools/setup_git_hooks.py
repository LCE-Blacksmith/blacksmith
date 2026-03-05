import shutil
import pathlib
import subprocess
import os

hooks_dir = pathlib.Path("tools/repo")
git_hooks = pathlib.Path(".git/hooks")

for hook in hooks_dir.iterdir():
    target = git_hooks / hook.name
    shutil.copy(hook, target)

    # Grant "Read & Execute" permissions for the current user
    subprocess.run(["icacls", str(target), "/grant", f"{os.getlogin()}:RX"], check=True)
