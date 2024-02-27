import pandas as pd
import requests
import json



url = "https://api-optimistic.etherscan.io/api?" \
      "module=account" \
      "&action=tokentx" \
      "&contractaddress=0x86f1e0420c26a858fc203A3645dD1A36868F18e5"\
      "&address=0xC64f9436f8Ca50CDCC096105C62DaD52FAEb1f2e"\
      "&startblock=0" \
      "&endblock=999999" \
      "&page=1" \
      "&offset=10000" \
      "&sort=asc" \
      "&apikey=WPSDUCKXQUHG4Q6M2P6XW9655RZ5GBUM1D"


headers = {

    "Accept": "application/json"

}


response = requests.get(url, headers=headers)


data=response.text
data_dict=json.loads(data)