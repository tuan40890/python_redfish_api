# Display Server Info
- This python script interacts with the Redfish API to obtain and display data from the Cisco UCS Rack Servers
- It also uses the cryptography library to encrypt the password that the user enters
- First, run `key_gen.py` to enter credentials to generate the encrypted files `key.key` and `creds.enc`
- These two encrypted files are required for the script `cisco-ucscimc-redfish.py` to run
- Below is the output example for all servers on the terminal, and it includes the starting and ending time
- In additiona, output for each server is generated into separate .txt files
# Output Example:
```
test-user@test-vm:~/python_redfish_api$ uv run cisco-ucscimc-redfish.py 

Script started at 16:18:05 on 09-22-2025

Retrieving data for 2 devices...

------------------------------------------
[DEVICE INFO]
Model: UCSC-C220-M6S
Serial Number: 123456788
CIMC FW Version: C220M6.4.3.2e.0.1130231848
CPU Model: 2 x Intel(R) Xeon(R) Gold 5318N CPU @ 2.10GHz
Total Memory in GB: 128 (Health = OK)
Effective Memory in GB: 128
Output is exported to '192.168.1.10.txt'
------------------------------------------
[DEVICE INFO]
Model: UCSC-C220-M6S
Serial Number: 123456789
CIMC FW Version: C220M6.4.3.2e.0.1130231848
CPU Model: 2 x Intel(R) Xeon(R) Gold 5318N CPU @ 2.10GHz
Total Memory in GB: 128 (Health = OK)
Effective Memory in GB: 128
Output is exported to '192.168.1.11.txt'
------------------------------------------

Completed.

Script ended at 16:18:08 on 09-22-2025
Total script runtime: 00:00:03
```
