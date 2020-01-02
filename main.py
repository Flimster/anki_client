"""Client to post new notes to the Anki"""

import json
import requests
from pprint import pprint
from note_parser import parse_note
from cli import parser

payload = {"action": "addNotes", "version": 6, "params": {"notes": []}}

args = parser.parse_args()
notes = parse_note(args.deck_name[0])
if notes is not None:
    payload["params"]["notes"] = notes

    print("Request: ")
    pprint(payload["params"]["notes"])
    print()

    send_request = input("Do you want to go ahead and send the request (yes/no)? ")
    if send_request == "yes":
        payload = json.dumps(payload)
        response = requests.post("http://localhost:8765", data=payload)
        print(response.content)

