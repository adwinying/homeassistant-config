#!/usr/bin/env python3

#
# Sesame commands
#

import base64, datetime, json, requests, sys
from Crypto.Cipher import AES
from Crypto.Hash import CMAC

COMMANDS = {
    "lock": 82,
    "unlock": 83,
    "toggle": 88,
}

def main():
    try:
        command = sys.argv[1]
        api_key = sys.argv[2]
        uuid = sys.argv[3]
        secret = sys.argv[4]
    except IndexError:
        print("Usage: sesame <lock|unlock|toggle> <api_key> <uuid> <secret>")
        sys.exit(1)

    cmd = COMMANDS[command]

    history = base64.b64encode("HomeAssistant".encode()).decode()

    ts = int(datetime.datetime.now().timestamp())
    msg = ts.to_bytes(4, byteorder="little").hex()[2:8]

    cmac = CMAC.new(bytes.fromhex(secret), ciphermod=AES)
    cmac.update(bytes.fromhex(msg))
    sign = cmac.hexdigest()

    url = f'https://app.candyhouse.co/api/sesame2/{uuid}/cmd'
    headers = { "x-api-key": api_key }
    body = { "cmd": cmd, "history": history, "sign": sign }

    res = requests.post(url, json.dumps(body), headers=headers)
    print(url, headers, body)
    print(res.status_code, res.text)

if __name__ == "__main__":
    main()
