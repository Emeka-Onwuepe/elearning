from datetime import datetime
from random import random

year = str(datetime.now().year)
rand_num = str(random())
print(rand_num[-5:])
print(year)

import re

input_data = ' DJDJDJ101010110'
data = re.findall('[A-Z]+', input_data)[0]
print(data)
