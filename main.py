"""Client to post new notes to the Anki"""

import json
import requests
from parser import parse

payload = {
    "action": "addNotes",
    "version": 6,
    "params": {
        "notes": []
    }
}

notes = parse()
payload["params"]["notes"] = notes
payload = json.dumps(payload)
print(payload)

response = requests.post("http://localhost:8765", data=payload)

print(response.content)

