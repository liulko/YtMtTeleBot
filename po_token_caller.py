import os
import json
import subprocess
def getPOToken():
    homeFolder = os.path.expanduser("~")
    process = subprocess.Popen([f'{homeFolder}/.nvm/versions/node/v22.14.0/bin/node',
                                f'{homeFolder}/.nvm/versions/node/v22.14.0/bin/youtube-po-token-generator'],
                               stdout=subprocess.PIPE)
    out = json.loads(process.communicate()[0].decode("utf-8"))
    out_dict = {
        'visitorData': out['visitorData'],
        'po_token': out['poToken'],
    }
    # print(out)
    with open('tokensfile.json', 'w', encoding='utf-8') as f:
        json.dump(out_dict, f, ensure_ascii=False)

    return 'tokensfile.json'

print(getPOToken())