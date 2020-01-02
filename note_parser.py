"""Parser component of the anki client"""

import re
import os
import shutil
import secrets
import markdown

media_folder = os.path.join(
    r"/Users/skoli/Library", r"Application Support/Anki2/", r"User 1/collection.media"
)

structure = "\t<QUESTION>\n\t<ANSWER>\n\t[TAGS]"


class NoteError(BaseException):
    pass


def create_note(data):
    if len(data) != 3:
        raise NoteError(
            f"Not enough fields to constuct note structure.\nStructure should be\n{structure}"
        )

    front = data[0]
    back = data[1]
    tags = data[2].split(" ")

    # When you do want to insert a <br /> break tag using Markdown,
    # you end a line with two or more spaces , then type return ("  \n").
    front = front.replace("\n", "  \n")
    front = markdown.markdown(front)
    back = back.replace("\n", "  \n")
    back = markdown.markdown(back)

    fields = {"Front": front, "Back": back}

    options = {"allowDuplicate": False}

    note = {
        "modelName": "Basic",
        "fields": fields,
        "tags": tags,
        "options": options,
    }

    return note


def parse_note(deck_name):
    notes = []
    with open("notes.md") as file:
        file_content = file.read().split("\n-")

        for raw_note in file_content:

            note_parts = raw_note.split("///")

            # TODO: Improvement on how to mark when skipping notes
            # We strip because every note_parts[0] (except the first one) starts with \n
            note_parts[0] = note_parts[0].strip()
            if note_parts[0][0] == "!":
                continue

            # The answer and tags are always the last index after the split
            answer_and_tags = note_parts.pop().strip().split("\n")

            note_parts += answer_and_tags

            for index, part in enumerate(note_parts):
                try:
                    found = re.findall("!\[\]\((.+?)\)", part)
                    for item in found:
                        image_hash = secrets.token_urlsafe(16)
                        os.rename('images/' + item, 'images/' + image_hash + item)
                        note_parts[index] = f'![]({image_hash + item})'
                        shutil.copy('images/' + image_hash + item, media_folder)
                        note_parts[index] = re.sub("!\[\]\((.+?)\)", f'![]({image_hash + item})', note_parts[index])
                        
                except AttributeError as e:
                    print(e)

            try:
                note = create_note(note_parts)
                note["deckName"] = deck_name
                notes.append(note)
            except NoteError as e:
                print(f"{e}")
                return None

    return notes
