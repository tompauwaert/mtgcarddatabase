
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


