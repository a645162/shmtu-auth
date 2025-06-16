import urllib3

urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import requests

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def request_set_ciphers():
    urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"
    requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS = "ALL:@SECLEVEL=1"


def request_disable_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
