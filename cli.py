import argparse

parser = argparse.ArgumentParser(description="<description goes here>")

parser.add_argument(
    "deck_name",
    metavar="Name",
    type=str,
    nargs=1,
    help="The deck the cards are supposed to be added to",
)

