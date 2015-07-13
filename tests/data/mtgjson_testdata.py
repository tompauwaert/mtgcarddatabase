"""
TEST DATA FOR MTG JSON TESTING.
This hold some json_data that can be used for testing.
"""

data = """
{
    "ISD": {
        "code": "ISD",
        "name": "Innistrad",
        "border": "black",
        "releaseDate": "2011-09-30",
        "cards": [],
        "booster": [
            [
                "rare",
                "mythic rare"
            ],
            "uncommon",
            "uncommon",
            "uncommon",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            [
                "land",
                "checklist"
            ],
            "marketing",
            "double faced"
        ],
        "type": "expansion",
        "block": "Innistrad",
        "magicCardsInfoCode": "isd"
    },
    "p2HG": {
        "code": "p2HG",
        "name": "Two-Headed Giant Tournament",
        "type": "promo",
        "releaseDate": "2005-12-09",
        "cards": [],
        "magicRaritiesCodes": "13-rarities-two-headed-giant",
        "border": "black",
        "magicCardsInfoCode": "thgt"
    },
    "GPT": {
        "code": "GPT",
        "name": "Guildpact",
        "border": "black",
        "releaseDate": "2006-02-03",
        "cards": [],
        "type": "expansion",
        "block": "Ravnica",
        "magicCardsInfoCode": "gp"
    },
    "DRK": {
        "code": "DRK",
        "name": "The Dark",
        "type": "expansion",
        "releaseDate": "1994-08-01",
        "booster": [
            "uncommon",
            "uncommon",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common"
        ],
        "cards": [],
        "gathererCode": "DK",
        "border": "black",
        "magicCardsInfoCode": "dk"
    },
    "ARC": {
        "code": "ARC",
        "name": "Archenemy",
        "border": "black",
        "releaseDate": "2010-06-18",
        "cards": [],
        "type": "from the vault",
        "magicCardsInfoCode": "v14"
    },
    "7ED": {
        "code": "7ED",
        "name": "Seventh Edition",
        "type": "core",
        "releaseDate": "2001-04-11",
        "booster": [
            "rare",
            "uncommon",
            "uncommon",
            "uncommon",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "common",
            "land"
        ],
        "cards": [],
        "gathererCode": "7E",
        "border": "white",
        "magicCardsInfoCode": "7e"
    },
    "HOP": {
        "code": "HOP",
        "name": "Planechase",
        "type": "planechase",
        "oldCode": "PCH",
        "releaseDate": "2009-09-04",
        "cards": [],
        "gathererCode": "P2",
        "border": "black",
        "magicCardsInfoCode": "pch"
    }
}
"""
data_malformed_json = """
{
    "ISD": {
        "code": "ISD",
        "name": "Innistrad",
        "border": "black",
                "land",
                "checklist"
            ],
            "marketing",
            "double faced"
        ],
        "type": "expansion",
        "block": "Innistrad",
        "magicCardsInfoCode": "isd"
    },
        "cards": [],
        "gathererCode": "DK",
        "border": "black",
        "magicCardsInfoCode": "dk"
    },
    "ARC": {
        "code": "ARC",
        "name": "Archenemy",
        "border": "black",
        "releaseDate": "2010-06-18",
        "cards": [],
        "type": "from the vault",
        "magicCardsInfoCode": "v14"
    },
"""
_SETS_ZIPPED = 'mtgjson_testdata_sets.zip'
_SETS_CONTENT_NAME = 'Allsets-x.json.zip'

import StringIO
import zipfile
import json

def data_zipped(data=data):
    zip_buffer = StringIO.StringIO()
    zip_archive = zipfile.ZipFile(zip_buffer, mode='w')

    data_buffer = StringIO.StringIO()
    data_buffer.write(data)

    zip_archive.writestr(_SETS_CONTENT_NAME, data_buffer.getvalue())
    zip_archive.close()
    return zip_buffer.getvalue()

def data_file(data=data):
    output = StringIO.StringIO()
    # after writing the data, put the reading pointer back to the beginning of the file.
    output.write(data)
    output.seek(0)
    return output

def faulty_zipped():
    zip_corrupted = StringIO.StringIO(data_zipped())
    zip_corrupted.truncate(len(zip_corrupted.getvalue())-128)
    return zip_corrupted.getvalue()

def data_sets():
    data_loaded = json.loads(data)
    sets = [{"code": key,
             "name": data_loaded[key].get('name')}
            for key in data_loaded]

    return sets


if __name__ == "__main__":
    faulty_zipped()




