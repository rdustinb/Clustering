try:
    import psutil
    import time
    import json
    from gpiozero import CPUTemperature
    from datetime import datetime
except:
    print("There are libraries missing, please install psutil, time, and json.")

data_file = "data.json"
max_data_samples = 240 # Store 1 hour of samples

########################################
# Read in the JSON Data, or create a new dictionary to store...
try:
    with open(data_file, "r") as json_data:
         data = json.load(json_data)
except FileNotFoundError:
    # Create an empty data dictionary
    data = {"update_time": 0, "cpu_temp": 0, "cpu_count": psutil.cpu_count(), "mem_total": psutil.virtual_memory().total, "cpu_samples": list(), "mem_samples": list()}

time.sleep(1)

########################################
# Store the current time to track the current data samples
data["update_time"] = datetime.now().isoformat()

########################################
# This kicks off every minute, and there are samples take in this script every 15 seconds
for thisSample in range(4):
    # Fetch and append a Sample...
    data["cpu_samples"].append(psutil.cpu_percent())
    data["mem_samples"].append(psutil.virtual_memory().used)
    # Wait 15s, but not on the last sample
    if thisSample != 3: time.sleep(15)

########################################
# Get the current CPU Temperature
try:
    cpu_temp = CPUTemperature()
    data["cpu_temp"] = cpu_temp.temperature
except:
    # If this is running elsewhere or doesn't have the proper packages installed, just log a really high number
    data["cpu_temp"] = 99.999

########################################
# Get length of data arrays
cpu_sample_length = len(data["cpu_samples"])
mem_sample_length = len(data["mem_samples"])

# Trim the CPU data if necessary...
if cpu_sample_length > max_data_samples:
    thisTrim = cpu_sample_length - max_data_samples
    # Remove the oldest samples...
    del data["cpu_samples"][:thisTrim]
    cpu_sample_length = len(data["cpu_samples"])

# Trim the Memory data if necessary...
if mem_sample_length > max_data_samples:
    thisTrim = mem_sample_length - max_data_samples
    # Remove the oldest samples...
    del data["mem_samples"][:thisTrim]
    mem_sample_length = len(data["mem_samples"])

########################################
# Store the data
with open(data_file, 'w+', encoding="utf-8") as fh:
    json.dump(data, fh, ensure_ascii=False, indent=2)
