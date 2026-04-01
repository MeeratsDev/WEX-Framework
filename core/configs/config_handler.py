from pprint import pprint

import pyjson5

with open("./core/configs/config.json5", "r") as f:
    data = pyjson5.load(f)

pprint(data)
