"""
Defines different types of data that might be available for cards.

Each content_provider can create a mapping of the general data_id's to their
own specific identifiers for that type of data, if is available for their
content.
"""

class SET_DATA(object):

    # variable -> label
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

    # special -> label
    BORDER = 'set_border'
    BOOSTER = 'set_booster'



