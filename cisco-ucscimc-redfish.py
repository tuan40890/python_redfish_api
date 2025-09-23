#!/usr/bin/env python3

import sys
import os
import json
import datetime
import concurrent.futures
from cryptography.fernet import Fernet
import requests
from requests.auth import HTTPBasicAuth

# disable SSL certificate verification warnings
requests.packages.urllib3.disable_warnings()


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

    # set up base API URL for the target IP
    base_url = f"https://{ip}/redfish/v1"

    # ---------------------Retrieve info from the /Systems/ resource---------------------
    # send a GET request with credentials, disable SSL verification, return response in .json format 
    systems = requests.get(f"{base_url}/Systems/", auth=HTTPBasicAuth(user, password), verify=False).json()
    
    # from the Members array under Systems, extract the first "@odata.id" value (serial number)
    serial_number = systems.get("Members", [])[0]["@odata.id"].split("/")[-1]

    # assign a variable to the extracted string value
    serial_number_resource = requests.get(f"{base_url}/Systems/{serial_number}", auth=HTTPBasicAuth(user, password), verify=False).json()

    # obtain individual item
    model = serial_number_resource.get("Model")
    sn = serial_number_resource.get("SerialNumber")
    fw = serial_number_resource.get("BiosVersion")
    total_memory = serial_number_resource.get("MemorySummary", {}).get("TotalSystemMemoryGiB")
    memory_health = serial_number_resource.get("MemorySummary", {}).get("Status").get("Health")
    effective_memory = serial_number_resource.get("Oem", {}).get("Cisco", {}).get("SystemEffectiveMemory")
    
    display_output.append("----------[DEVICE INFO]----------\n")
    display_output.append(f"Model: {model}")
    display_output.append(f"Serial Number: {sn}")
    display_output.append(f"CIMC FW Version: {fw}")
    display_output.append(f"Total Memory in GB: {total_memory} (Health = {memory_health})")
    display_output.append(f"Effective Memory in GB: {effective_memory}")

    # ---------------------Retrieve info from the /Systems/{serial_number}/Processors/ resource---------------------
    cpu1 = requests.get(f"{base_url}/Systems/{serial_number}/Processors/CPU1/", auth=HTTPBasicAuth(user, password), verify=False).json()
    cpu1_state = cpu1.get("Status", {}).get("State", {})
    cpu1_model = cpu1.get("Model", {})
    cpu1_des = cpu1.get("Description", {})
    cpu2 = requests.get(f"{base_url}/Systems/{serial_number}/Processors/CPU2/", auth=HTTPBasicAuth(user, password), verify=False).json()
    cpu2_state = cpu2.get("Status", {}).get("State", {})
    cpu2_model = cpu2.get("Model", {})
    cpu2_des = cpu2.get("Description", {})
    display_output.append("\n----------[CPU INFO]----------")
    display_output.append(f"CPU1\n\tPresence: {cpu1_state}\n\tModel: {cpu1_model}\n\tDescription: {cpu1_des}")
    display_output.append(f"CPU2\n\tPresence: {cpu2_state}\n\tModel: {cpu2_model}\n\tDescription: {cpu2_des}")

    # ---------------------Retrieve info from the /Chassis/1/Power/ resource---------------------
    psu = requests.get(f"{base_url}/Chassis/1/Power/", auth=HTTPBasicAuth(user, password), verify=False).json()
    psu1_state = psu["PowerSupplies"][0]["Status"]["State"]
    psu1_model = psu["PowerSupplies"][0]["Model"]
    psu2_state = psu["PowerSupplies"][1]["Status"]["State"]
    psu2_model = psu["PowerSupplies"][0]["Model"]
    display_output.append("\n----------[PSU INFO]----------")
    display_output.append(f"PSU1\n\tPresence: {psu1_state}\n\tModel: {psu1_model}")
    display_output.append(f"PSU2\n\tPresence: {psu2_state}\n\tModel: {psu2_model}")

    # join all the output and name the output file
    output_file_name = f"{ip}.txt"
    display_output.append(f"\nOutput is exported to '{output_file_name}'")
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
