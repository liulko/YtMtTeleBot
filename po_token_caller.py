import os
import json
import subprocess
def getPOToken():
    homeFolder = os.path.expanduser("~")
    process = subprocess.Popen([f'{homeFolder}/.nvm/versions/node/v22.14.0/bin/node',
                                f'{homeFolder}/.nvm/versions/node/v22.14.0/bin/youtube-po-token-generator'],
                               stdout=subprocess.PIPE)
    out = json.loads(process.communicate()[0].decode("utf-8"))
    # print(out)
    return {
        'visitorData': out['visitorData'],
        'poToken': out['poToken'],
    }
