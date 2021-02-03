import shutil
import os
import sys

date = sys.argv[1][:10]

input_file = "/data/order_details.csv"

output = "/data/csv/{0}/data.csv".format(date)

os.makedirs(os.path.dirname(output), exist_ok = True)

shutil.copy(input_file,output)