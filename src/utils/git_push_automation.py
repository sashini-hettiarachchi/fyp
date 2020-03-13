import subprocess as cmd
from src.utils.file_manipulation import PATH


def git_push_automation():
    try:
        cp = cmd.run(PATH+"\\er.txt", check=True, shell=True)
        print("cp", cp)
        cmd.run('git add data/er.txt', check=True, shell=True)
        cmd.run('git commit -m "update the er.txt file"', check=True, shell=True)
        cmd.run("git push -u origin master -f", check=True, shell=True)
        print("Success")
        return True
    except:
        print("Error git automation")
        return False


# git_push_automation()
