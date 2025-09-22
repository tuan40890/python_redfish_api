#!/usr/bin/env python3

import sys
import os
import json
import datetime
import concurrent.futures
from cryptography.fernet import Fernet
import requests
from requests.auth import HTTPBasicAuth


def load_creds():
    '''
    Load the credentials from .key and .enc files
    '''

    try:

        # use the .key file to unlock the encrypted .enc file and decrypt it
        KEY_FILE = "key.key"
        CREDS_FILE = "creds.enc"
        key = open(KEY_FILE, "rb").read()
        data = Fernet(key).decrypt(open(CREDS_FILE, "rb").read())

        # after decryption, data is still a byte string, decode it into normal strings
        str_creds = json.loads(data.decode())

        # extract the decoded normal strings to return the values
        return str_creds["username"], str_creds["password"]
    except Exception as e:
        print(f"Credential error: {e}")
        sys.exit(1)


def info_retrieval(ip, user, password):
    '''
    Retrieve device info and export it to a .txt file
    '''

    # set an empty list to append sectional outputs after
    display_output = []

    # disable SSL certificate verification warnings
    requests.packages.urllib3.disable_warnings()

    # set up base API URL for the target IP
    base_url = f"https://{ip}/redfish/v1"

    # send a GET request with credentials, disable SSL verification, return response in .json format 
    systems = requests.get(f"{base_url}/Systems", auth=HTTPBasicAuth(user, password), verify=False).json()
    
    # from the response above, extract the list of system members
    members = systems.get("Members", [])

    # extract the first member's '@odata.id' URI (serial number)
    serial_number = members[0]["@odata.id"].split("/")[-1]

    # send a GET request again with the serial number
    each_system = requests.get(f"{base_url}/Systems/{serial_number}", auth=HTTPBasicAuth(user, password), verify=False).json()
    
    # start obtaining info
    model = each_system.get("Model")
    sn = each_system.get("SerialNumber")
    fw = each_system.get("BiosVersion")
    cpu = each_system.get("ProcessorSummary", {})
    total_memory = each_system.get("MemorySummary", {}).get("TotalSystemMemoryGiB")
    memory_health = each_system.get("MemorySummary", {}).get("Status").get("Health")
    effective_memory = each_system.get("Oem", {}).get("Cisco", {}).get("SystemEffectiveMemory")
    
    display_output.append("[DEVICE INFO]")
    display_output.append(f"Model: {model}")
    display_output.append(f"Serial Number: {sn}")
    display_output.append(f"CIMC FW Version: {fw}")
    display_output.append("CPU Model: " + str(cpu.get("Count")) + " x " + cpu.get("Model"))
    display_output.append(f"Total Memory in GB: {total_memory} (Health = {memory_health})")
    display_output.append(f"Effective Memory in GB: {effective_memory}")

    output_file_name = f"{ip}.txt"
    display_output.append(f"Output is exported to '{output_file_name}'")
    display_output.append(f"------------------------------------------\n")
    joining_output = "\n".join(display_output)

    try:

    # export the output
        with open(output_file_name, "w") as file:
            file.write(joining_output)
    except Exception as e:
        joining_output += f"\nCRITICAL: cannot write {output_file_name}: {e}\n"
    return joining_output
    

if __name__ == "__main__":

    '''all the print statements here provide terminal outputs, they're not exported to a file'''

    # start timer to display starting time
    script_starting_time = datetime.datetime.now()
    print(f"\nScript started at {script_starting_time:%H:%M:%S} on {script_starting_time:%m-%d-%Y}\n")

    # load the credentials (to be used for concurrency later)
    user, password = load_creds()

    # create a variable to access the file
    IP_ADDRESSES = "ip.txt"

    # check if host file is present
    if not os.path.exists(IP_ADDRESSES):
        print(f"Missing '{IP_ADDRESSES}'")
        sys.exit(1)

    # use list comprehension to include only the stripped IP addresses
    ip_addresses = [each_line.strip() for each_line in open(IP_ADDRESSES) if each_line.strip()]

    # check if IP is found in the host file
    if not ip_addresses:
        print("No IPs found. Exiting.")
        sys.exit(0)

    print(f"Retrieving data for {len(ip_addresses)} devices...\n")
    print(f"------------------------------------------")

    # assign the number of works to work on concurrency
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor_object:
        for future_object in concurrent.futures.as_completed(
            executor_object.submit(info_retrieval, ip, user, password) for ip in ip_addresses):

            # print result, display all output
            print(future_object.result(), end="")

    # calculate script runtime duration
    script_ending_time = datetime.datetime.now()
    duration = int((script_ending_time - script_starting_time).total_seconds())
    hour, remainder = divmod(duration, 3600)
    minute, second = divmod(remainder, 60)

    print("\nCompleted.")
    print(f"\nScript ended at {script_ending_time:%H:%M:%S} on {script_ending_time:%m-%d-%Y}")
    print(f"Total script runtime: {hour:02}:{minute:02}:{second:02}")
