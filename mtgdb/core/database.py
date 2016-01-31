import content_provider

class Database(object):

    _CONTENT_PROVIDERS = [
        content_provider.MtgjsonContent,
    ]

    def clear_cache(self):
        """
        Clear the cache of all the content providers. They should
        get the data for the next call remotely.
        """
        for t_provider in self._CONTENT_PROVIDERS:
            provider = t_provider()
            provider.clear_cache()