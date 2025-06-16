# https://github.com/PyGithub/PyGithub/issues/2300
# https://stackoverflow.com/questions/61631955/python-requests-ssl-error-during-requests
import ssl

import requests
from urllib3 import poolmanager

url = "https://live.euronext.com/fr/product/equities/FR0000120271-XPAR"


class TLSAdapter(requests.adapters.HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        """Create and initialize the urllib3 PoolManager."""
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        self.poolmanager = poolmanager.PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLS,
            ssl_context=ctx,
        )


session = requests.session()
session.mount("https://", TLSAdapter())
res = session.get(url)
print(res)
