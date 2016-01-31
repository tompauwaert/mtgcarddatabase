import os

_path_to_raw_mtgjson_cards = "data" + os.sep + "raw_mtgjson_cards.json"

data_with_cards_SETS = ["ISD", "CPK", "p2HG", "GPT", "DRK"]
data_with_cards_SETS_NR_CARDS = {
    "ISD": 6,
    "CPK": 12,
    "p2HG": 1,
    "GPT": 26,
    "DRK": 0
}

with open(_path_to_raw_mtgjson_cards, 'r') as raw_json:
    data_with_cards = raw_json.read()
