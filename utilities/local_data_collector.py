import psutil
import time
import json

SampleSeconds = 55

data_dict = {"cpu_count": psutil.cpu_count(), "mem_total": psutil.virtual_memory().total, "cpu_samples": list(), "mem_samples": list()}

# Fetch the Samples...
for thisSample in range(SampleSeconds):
    data_dict["cpu_samples"].append(psutil.cpu_percent())
    data_dict["mem_samples"].append(psutil.virtual_memory().available)
    time.sleep(1)

with open("data.json", 'w+', encoding="utf-8") as fh:
    json.dump(data_dict, fh, ensure_ascii=False, indent=2)
