# -*- coding: utf-8 -*-
import sys
import json
import numpy as np

# Read JSON from stdin
data = json.loads(sys.stdin.read())

# DO something
ldf = np.array(data["levldiff"])

indL=ldf.argmin()

# Return result as JSON
print(json.dumps({"index": indL}))
