#!/usr/bin/env python3

import sys
import os
import json
import datetime
import concurrent.futures
import pandas as pd
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
    
    display_output.append("----------[DEVICE INFO]----------\n")

    # send a GET request with credentials, disable SSL verification, return response in .json format 
    systems = requests.get(
        f"{base_url}/Systems/",
        auth=HTTPBasicAuth(user, password), verify=False).json()
    
    # from the Members array under Systems, extract the first "@odata.id" value (serial number)
    serial_number = systems.get("Members", [])[0]["@odata.id"].split("/")[-1]

    # assign a variable to the extracted string value
    serial_number_resource = requests.get(
        f"{base_url}/Systems/{serial_number}",
        auth=HTTPBasicAuth(user, password), verify=False).json()

    # obtain individual item
    model = serial_number_resource.get("Model")
    sn = serial_number_resource.get("SerialNumber")
    fw = serial_number_resource.get("BiosVersion")
    display_output.append(f"Model: {model}")
    display_output.append(f"Serial Number: {sn}")
    display_output.append(f"CIMC FW Version: {fw}")

    # ---------------------Retrieve info from the /Systems/{serial_number}/Processors/ resource---------------------
    display_output.append("\n----------[CPU INFO]----------")
    cpu1 = requests.get(
        f"{base_url}/Systems/{serial_number}/Processors/CPU1/",
        auth=HTTPBasicAuth(user, password), verify=False).json()
    cpu1_name = cpu1.get("Name", {})
    cpu1_state = cpu1.get("Status", {}).get("State", {})
    cpu1_health = cpu1.get("Status", {}).get("Health", {})
    cpu1_model = cpu1.get("Model", {})
    cpu1_des = cpu1.get("Description", {})
    cpu2 = requests.get(
        f"{base_url}/Systems/{serial_number}/Processors/CPU2/",
        auth=HTTPBasicAuth(user, password), verify=False).json()
    cpu2_name = cpu2.get("Name", {})
    cpu2_state = cpu2.get("Status", {}).get("State", {})
    cpu2_health = cpu1.get("Status", {}).get("Health", {})
    cpu2_model = cpu2.get("Model", {})
    cpu2_des = cpu2.get("Description", {})
    display_output.append(
        f"{cpu1_name}\n\t"
        f"Presence: {cpu1_state}\n\t"
        f"Health: {cpu1_health}\n\t"
        f"Model: {cpu1_model}\n\t"
        f"Description: {cpu1_des}")
    display_output.append(
        f"{cpu2_name}\n\t"
        f"Presence: {cpu2_state}\n\t"
        f"Health: {cpu2_health}\n\t"
        f"Model: {cpu2_model}\n\t"
        f"Description: {cpu2_des}")

    # ---------------------Retrieve info from the /Chassis/1/Power/ resource---------------------
    display_output.append("\n----------[PSU INFO]----------")
    psu = requests.get(
        f"{base_url}/Chassis/1/Power/",
        auth=HTTPBasicAuth(user, password), verify=False).json()
    psu1_name = psu["PowerSupplies"][0]["Name"]
    psu1_state = psu["PowerSupplies"][0]["Status"]["State"]
    psu1_health = psu["PowerSupplies"][0]["Status"]["Health"]
    psu1_model = psu["PowerSupplies"][0]["Model"]
    psu1_sn = psu["PowerSupplies"][0]["SerialNumber"]
    psu2_name = psu["PowerSupplies"][1]["Name"]
    psu2_state = psu["PowerSupplies"][1]["Status"]["State"]
    psu2_health = psu["PowerSupplies"][1]["Status"]["Health"]
    psu2_model = psu["PowerSupplies"][1]["Model"]
    psu2_sn = psu["PowerSupplies"][0]["SerialNumber"]
    display_output.append(
        f"{psu1_name}\n\t"
        f"Presence: {psu1_state}\n\t"
        f"Health: {psu1_health}\n\t"
        f"Model: {psu1_model}\n\t"
        f"Serial Number: {psu1_sn}")
    display_output.append(
        f"{psu2_name}\n\t"
        f"Presence: {psu2_state}\n\t"
        f"Health: {psu2_health}\n\t"
        f"Model: {psu2_model}\n\t"
        f"Serial Number: {psu2_sn}")

    # ---------------------Retrieve info from the /Systems/{serial_number}/Memory/ resource---------------------
    display_output.append("\n----------[MEMORY INFO]----------")
    memory = requests.get(
        f"{base_url}/Systems/{serial_number}/Memory/",
        auth=HTTPBasicAuth(user, password), verify=False).json()

    '''
        create a mapping of vendor ID of the manufacturer from hex to string, source:
        https://www.cisco.com/c/en/us/td/docs/unified_computing/ucs/c/sw/gui/config/guide/2-0/b_Cisco_UCS_C-Series_GUI_Configuration_Guide_for_C3x60_Servers/b_Cisco_UCS_C-Series_GUI_Configuration_Guide_207_chapter_0101.pdf
    '''


    all_dimms = memory.get("Members", [])
    all_dimm_data = []
    for each_dimm in all_dimms:
        dimm_slot = each_dimm["@odata.id"].split("/")[-1]
        retrieve_dim_info = requests.get(
            f"{base_url}/Systems/{serial_number}/Memory/{dimm_slot}/",
            auth=HTTPBasicAuth(user, password), verify=False
        ).json()
        dimm_slot_name = retrieve_dim_info.get("Name", {})
        
        # manufacturer returns a hex string, create a dict to convert it to the normal name
        vendor_id_mapping = {
            "0x2C00" : "Micron Technology, Inc.",
            "0x5105" : "Qimonda AG i. In.",
            "0x802C" : "Micron Technology, Inc.",
            "0x80AD" : "Hynix Semiconductor Inc.",
            "0x80CE" : "Samsung Electronics, Inc.",
            "0x8551" : "Qimonda AG i. In.",
            "0xAD00" : "Hynix Semiconductor Inc.",
            "0xCE00" : "Samsung Electronics, Inc."
        }
        dimm_manu = retrieve_dim_info.get("Manufacturer", "")
        if dimm_manu:
            dimm_manu = vendor_id_mapping.get(dimm_manu, {})
        
        dimm_part_num = retrieve_dim_info.get("PartNumber", "")
        dimm_sn = retrieve_dim_info.get("SerialNumber", "")
        dimm_type = retrieve_dim_info.get("MemoryDeviceType", "")
        dimm_capacity = retrieve_dim_info.get("CapacityMiB", "")
        dimm_speed = retrieve_dim_info.get("OperatingSpeedMhz", "")
        dimm_slot_state = retrieve_dim_info.get("Status", {}).get("State", "")
        dimm_slot_health = retrieve_dim_info.get("Status", {}).get("Health", "")
        each_dimm_data = [
            dimm_slot_name,
            dimm_manu,
            dimm_part_num,
            dimm_sn,
            dimm_type,
            dimm_capacity,
            dimm_speed,
            dimm_slot_state,
            dimm_slot_health
        ]
        all_dimm_data.append(each_dimm_data)

    # store output in a table format
    headers = ["Slot Name", "Manufacturer", "Part Number", "Serial Number", "Type", "Size(MB)", "Speed(MHz)", "Presence", "Health"]
    if all_dimm_data:
        df = pd.DataFrame(all_dimm_data, columns=headers).to_string(index=False, justify="left")
        display_output.append(df)
    else:
        display_output.append("No memory DIMMs found or populated.")

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
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as executor_object:
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
