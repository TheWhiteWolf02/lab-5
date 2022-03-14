import os
import sys
import subprocess
from pathlib import Path
import filecmp
import tarfile
import shutil

os.environ['LD_PRELOAD'] = 'faultinjectors/fi_{param}.so'.format(param=sys.argv[1])

def removeOldTestFiles():
    if os.path.exists("temp.tar"):
        os.remove("temp.tar")
    
    if Path('temp').exists():
        shutil.rmtree(Path('temp'))

    if Path('content').exists():
        shutil.rmtree(Path('content'))

def getTarState():
    if not os.path.exists('temp.tar'):
        return 'no_tar'

    if os.stat('temp.tar').st_size == 0:
        return 'empty'

    #extract the directory and files
    subprocess.run(['mkdir', 'temp'])
    subprocess.run(['tar', 'xf', 'temp.tar', '--directory', 'temp'])

    if not Path('temp/content').exists():
        return "corrupted"

    result = filecmp.dircmp('content', 'temp/content')

    if len(result.diff_files) == 0:
        return 'okay'
    else:
        return 'corrupted'

def printResultDetails(processState, tarState):
    print('Injected: ' + sys.argv[1])
    print('ProcessState: ' + processState)
    print('TarState: ' + tarState)

    removeOldTestFiles()

def main():
    #os.spawnl(os.P_WAIT, "/bin/tar", "cf", "temp.tar", "content/")
    try:
        my_tar = tarfile.open('content.tar')
        my_tar.extractall('./')
        my_tar.close()
        #subprocess.run(['tar', 'xf', 'content.tar', '--directory', 'content'])
    finally:
        try:
            result = subprocess.run(['tar', 'cf', 'temp.tar', 'content/'], timeout = 5)
            if result.returncode == 0:
                state = getTarState()
                printResultDetails('success', state)
            elif result.returncode != 0:
                state = getTarState()
                printResultDetails('exited', state)
            elif result.returncode < 0:
                state = getTarState()
                printResultDetails('signaled', state)
        except subprocess.TimeoutExpired:
            state = getTarState()
            printResultDetails('timeout', state)

if __name__ == "__main__":
    main()