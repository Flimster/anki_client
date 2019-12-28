"""Parser component of the anki client"""


# TODO: actually get name of deck
deck_name = "tmp"


def create_note(data):
    try:
        front = data[0]
        back = data[1]
        tags = data[2].split(" ")
    except IndexError:
        return None
    fields = {'Front': front, 'Back': back}
    options = {"allowDuplicate": False}

    note = {
        'deckName': deck_name,
        'modelName': 'Basic',
        'fields': fields,
        'tags': tags,
        'options': options
    }

    return note


def parse():
    notes = []
    with open('notes.txt') as file:
        file_content = file.read().split("\n\n")
        for note_content in file_content:
            note = note_content.strip().split('\n')
            note = create_note(note)
            if note is not None:
                notes.append(note)
    print(notes)
    return notes

