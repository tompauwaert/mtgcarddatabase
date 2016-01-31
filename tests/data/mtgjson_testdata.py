"""
TEST DATA FOR MTG JSON TESTING.
This hold some json_data that can be used for testing.
"""
from mtgjson_sets import data
from mtgjson_sets import data_extended
from mtgjson_sets import data_malformed_json
from mtgjson_cards import data_with_cards

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




