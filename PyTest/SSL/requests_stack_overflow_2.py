import ssl
import requests.adapters

url = "https://www.tauron-dystrybucja.pl/"


# url = "https://expired.badssl.com/"


class TLSAdapter(requests.adapters.HTTPAdapter):

    def init_poolmanager(self, *args, **kwargs):
        ctx = ssl.create_default_context()
        ctx.set_ciphers("DEFAULT@SECLEVEL=1")
        kwargs["ssl_context"] = ctx
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)


session = requests.session()
session.mount("https://", TLSAdapter())
res = session.get(url)
print(res)
