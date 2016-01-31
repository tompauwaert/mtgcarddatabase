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

data_extended = """
{
    "ISD": {
        "code": "ISD",
        "magicCardsInfoCode": "isd",
        "oldCode": "ISD",
        "gathererCode": "ISD",
        "onlineOnly": false,
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
        "block": "Innistrad"
    },
    "p2HG": {
        "code": "p2HG",
        "magicCardsInfoCode": "thgt",
        "oldCode": "p2HG",
        "gathererCode": "p2HG",
        "onlineOnly": false,
        "name": "Two-Headed Giant Tournament",
        "type": "promo",
        "releaseDate": "2005-12-09",
        "cards": [],
        "magicRaritiesCodes": "13-rarities-two-headed-giant",
        "border": "black"
    },
    "GPT": {
        "code": "GPT",
        "magicCardsInfoCode": "gp",
        "oldCode": "GPT",
        "gathererCode": "GPT",
        "onlineOnly": false,
        "name": "Guildpact",
        "border": "black",
        "releaseDate": "2006-02-03",
        "cards": [],
        "type": "expansion",
        "block": "Ravnica"
    },
    "DRK": {
        "code": "DRK",
        "gathererCode": "DK",
        "magicCardsInfoCode": "dk",
        "oldCode": "DRK",
        "onlineOnly": false,
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
        "border": "black"
    },
    "ARC": {
        "code": "ARC",
        "magicCardsInfoCode": "v14",
        "oldCode": "ARC",
        "gathererCode": "ARC",
        "onlineOnly": false,
        "name": "Archenemy",
        "border": "black",
        "releaseDate": "2010-06-18",
        "cards": [],
        "type": "from the vault"
    },
    "7ED": {
        "code": "7ED",
        "oldCode": "7ED",
        "onlineOnly": false,
        "gathererCode": "7E",
        "magicCardsInfoCode": "7e",
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
        "border": "white"
    },
    "HOP": {
        "code": "HOP",
        "gathererCode": "P2",
        "oldCode": "PCH",
        "magicCardsInfoCode": "pch",
        "onlineOnly": false,
        "name": "Planechase",
        "type": "planechase",
        "releaseDate": "2009-09-04",
        "cards": [],
        "border": "black"
    }
}
"""
_SETS_ZIPPED = 'mtgjson_testdata_sets.zip'
_SETS_CONTENT_NAME = 'Allsets-x.json.zip'

import StringIO, io
import zipfile
import json
from mtgdb.core.data_labels import SET_LABELS as d_id

def data_zipped(data=data):
    zip_buffer = io.BytesIO()
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

def data_sets(data=data, info=None):
    if info is None:
        info = []

    data_loaded = json.loads(data)
    sets = [{d_id.CODE: key,
             d_id.NAME: data_loaded[key].get('name')}
            for key in data_loaded]

    if d_id.RELEASE_DATE in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('releaseDate') is not None:
                set[d_id.RELEASE_DATE] = data_loaded[set[d_id.CODE]].get('releaseDate')

    if d_id.BORDER in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('border') is not None:
                set[d_id.BORDER] = data_loaded[set[d_id.CODE]].get('border')

    if d_id.BLOCK in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('block') is not None:
                set[d_id.BLOCK] = data_loaded[set[d_id.CODE]].get('block')

    if d_id.TYPE in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('type') is not None:
                set[d_id.TYPE] = data_loaded[set[d_id.CODE]].get('type')

    if d_id.BOOSTER in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('booster') is not None:
                set[d_id.BOOSTER] = data_loaded[set[d_id.CODE]].get('booster')

    if d_id.GATHERER_CODE in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('gathererCode') is not None:
                set[d_id.GATHERER_CODE] = data_loaded[set[d_id.CODE]].get('gathererCode')

    if d_id.OLD_CODE in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('oldCode') is not None:
                set[d_id.OLD_CODE] = data_loaded[set[d_id.CODE]].get('oldCode')

    if d_id.MCI_CODE in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('magicCardsInfoCode') is not None:
                set[d_id.MCI_CODE] = data_loaded[set[d_id.CODE]].get('magicCardsInfoCode')

    if d_id.LANGUAGES in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('languagesPrinted') is not None:
                set[d_id.LANGUAGES] = data_loaded[set[d_id.CODE]].get('languagesPrinted')

    if d_id.ONLINE_ONLY in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('onlineOnly') is not None:
                set[d_id.ONLINE_ONLY] = data_loaded[set[d_id.CODE]].get('onlineOnly')

    if d_id.CARDS in info:
        for set in sets:
            if data_loaded[set[d_id.CODE]].get('cards') is not None:
                set[d_id.CARDS] = data_loaded[set[d_id.CODE]].get('cards')

    return sets


from pprint import pprint
if __name__ == "__main__":
    pprint(data_sets(data, [d_id.RELEASE_DATE, d_id.BORDER]))




