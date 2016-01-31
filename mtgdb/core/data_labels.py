"""
Defines different types of data that might be available for cards.

Each content_provider can create a mapping of the general data_id's to their
own specific identifiers for that type of data, if is available for their
content.
"""

class SET_LABELS(object):

    # code -> label
    CODE = 'set_code'
    GATHERER_CODE = 'set_gatherer_code'
    OLD_CODE = 'set_old_code'
    MCI_CODE = 'set_mci_code'

    # release -> label
    RELEASE_DATE = 'set_release_date'
    LANGUAGES = 'set_languages_printed'
    ONLINE_ONLY = 'set_online_only'

    # general -> label
    BLOCK = 'set_block_name'
    NAME = 'set_name'
    CARDS = 'cards'
    NR_CARDS = 'nr of cards'
    TYPE = 'type'

    # special -> label
    BORDER = 'set_border'
    BOOSTER = 'set_booster'


class CARD_LABELS(object):

    LAYOUT = 'layout'
    NAME = 'name'
    NAMES = 'other_names'
    MANACOST = 'mana_cost'
    CMC = 'cmc'
    COLORS = 'colors'
    FULLTYPE = 'full_type'
    SUPERTYPES = 'super_types'
    TYPES = 'types'
    SUBTYPES = 'sub_types'
    RARITY = 'rarity'
    TEXT = 'text'
    FLAVOR = 'flavor'
    ARTIST = 'artist'
    NUMBER = 'number'
    POWER = 'power'
    TOUGHNESS = 'toughness'
    LOYALTY = 'loyalty'
    MULTIVERSEID = 'multiverseid'
    VARIATIONS = 'variations'
    IMAGENAME = 'image_name'
    WATERMARK = 'watermark'
    BORDER = 'border'
    TIMESHIFTED = 'time_shifted'
    HAND = 'hand_modifier'
    LIFE = 'life_modifier'
    RESERVED = 'reserved'
    RELEASE_DATE = 'release_data'
    STARTER = 'starter'

    def get_id_labels(self):
        return [
            self.NAME,
            self.MULTIVERSEID,
            self.IMAGENAME
        ]

    def get_type_labels(self):
        return [
            self.FULLTYPE,
            self.SUPERTYPES,
            self.TYPES,
            self.SUBTYPES
        ]

    def get_art_labels(self):
        return [
            self.ARTIST,
            self.NUMBER,
            self.VARIATIONS
        ]

    def get_appearance_labels(self):
        return [
            self.LAYOUT,
            self.WATERMARK,
            self.ARTIST,
            self.MULTIVERSEID,
            self.VARIATIONS,
            self.NUMBER,
            self.BORDER
        ]

    def get_char_labels(self):
        return [
            self.NAME,
            self.MANACOST,
            self.CMC,
            self.COLORS,
            self.FULLTYPE,
            self.RARITY,
            self.TEXT,
            self.POWER,
            self.TOUGHNESS,
            self.LOYALTY,
            self.HAND,
            self.LIFE,
        ]

    def get_all_basic_labels(self):
        return [
            self.LAYOUT,
            self.NAME,
            self.NAMES,
            self.MANACOST,
            self.CMC,
            self.COLORS,
            self.FULLTYPE,
            self.SUPERTYPES,
            self.TYPES,
            self.SUBTYPES,
            self.RARITY,
            self.TEXT,
            self.FLAVOR,
            self.ARTIST,
            self.NUMBER,
            self.POWER,
            self.TOUGHNESS,
            self.LOYALTY,
            self.MULTIVERSEID,
            self.VARIATIONS,
            self.IMAGENAME,
            self.WATERMARK,
            self.BORDER,
            self.TIMESHIFTED,
            self.HAND,
            self.LIFE,
            self.RESERVED,
            self.RELEASE_DATE,
            self.STARTER,
        ]

    # extra fields
    RULINGS = 'rulings'
    FOREIGN_NAMES = 'foreign_names'
    PRINTING_CODES = 'printing_codes'
    PRINTING_NAMES = 'printing_names'
    ORIGINAL_TEXT = 'original_text'
    LEGALITIES = 'legalities'
    SOURCE = 'source'

    def get_all_extra_labels(self):
        return [
            self.RULINGS,
            self.FOREIGN_NAMES,
            self.PRINTING_CODES,
            self.PRINTING_NAMES,
            self.ORIGINAL_TEXT,
            self.LEGALITIES,
            self.SOURCE,
        ]

    def __init__(self):
        self._all_labels = None

    def get_all_labels(self):
        if self._all_labels is None:
            self._all_labels = self.get_all_basic_labels().append(self.get_all_extra_labels())
        return self._all_labels



