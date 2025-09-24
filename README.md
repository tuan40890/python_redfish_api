# Display Server Info from CIMC
- This python script interacts with the Redfish API to obtain and display data from the Cisco UCS Rack Servers
- It also uses the cryptography library to encrypt the password that the user enters
- First, run `key_gen.py` to enter credentials to generate the encrypted files `key.key` and `creds.enc`
- These two encrypted files are required for the script `cisco-ucscimc-redfish.py` to run
- Below is the output example for all servers on the terminal, and it includes the starting and ending time
- In additiona, output for each server is generated into separate .txt files
# Output Example:
```
test-user@test-vm:~/python_redfish_api$ uv run cisco-ucscimc-redfish.py 

Script started at 21:38:32 on 09-23-2025

Retrieving data for 2 devices...

------------------------------------------
----------[DEVICE INFO]----------

Model: UCSC-C240-M7SX
Serial Number: 15134236326232632623
CIMC FW Version: C240M7.4.3.2a.0.0710230213

----------[CPU INFO]----------
CPU1
        Presence: Enabled
        Model: Intel(R) Xeon(R) Bronze 3408U
        Description: Intel(R) Xeon(R) Bronze 1S 3408U CPU @ 1.8GHz 125W 8C 22.5MB Cache DDR5 4000MT/s
Computer Processor
        Presence: Absent
        Model: {}
        Description: Computer Processor

----------[PSU INFO]----------
PSU1
        Presence: Enabled
        Model: PS-2122-9S
        Serial Number: LKH272222AP
PSU2
        Presence: Enabled
        Model: PS-2122-9S
        Serial Number: LKH272222AP

----------[DRIVE INFO]----------
Slot # Manufacturer Model           Name                                        Serial #     Type  Capacity(GB) Presence
  1    TOSHIBA      UCS-HD12TB10KJ4 AL15SEB120N - 1.2TB 12G SAS 10K RPM SFF HDD 142352212323 HDD  1118          Enabled 
  2    TOSHIBA      UCS-HD12TB10KJ4 AL15SEB120N - 1.2TB 12G SAS 10K RPM SFF HDD 142352212313 HDD  1118          Enabled 
  3                                                                           3                   1118           Absent 
  4                                                                           4                   1118           Absent 
  5                                                                           5                   1118           Absent 
  6                                                                           6                   1118           Absent 
  7                                                                           7                   1118           Absent 
  8                                                                           8                   1118           Absent 
  9                                                                           9                   1118           Absent 
 10                                                                          10                   1118           Absent 
 11                                                                          11                   1118           Absent 
 12                                                                          12                   1118           Absent 
 13                                                                          13                   1118           Absent 
 14                                                                          14                   1118           Absent 
 15                                                                          15                   1118           Absent 
 16                                                                          16                   1118           Absent 
 17                                                                          17                   1118           Absent 
 18                                                                          18                   1118           Absent 
 19                                                                          19                   1118           Absent 
 20                                                                          20                   1118           Absent 
 21                                                                          21                   1118           Absent 
 22                                                                          22                   1118           Absent 
 23                                                                          23                   1118           Absent 
 24                                                                          24                   1118           Absent 
101                                                                         101                   1118           Absent 
102                                                                         102                   1118           Absent 
103                                                                         103                   1118           Absent 
104                                                                         104                   1118           Absent 

----------[MEMORY INFO]----------
Slot Name  Manufacturer              Part #             Serial #           Type Size(MB) Speed(MHz) Presence
DIMM_P1_A1 Samsung Electronics, Inc. M321R2GA3BB6-CQKET 845643638456347684 DDR5 16384    4800       Enabled 
DIMM_P1_A2                                                                                           Absent 
DIMM_P1_B1                                                                                           Absent 
DIMM_P1_B2                                                                                           Absent 
DIMM_P1_C1                                                                                           Absent 
DIMM_P1_C2                                                                                           Absent 
DIMM_P1_D1                                                                                           Absent 
DIMM_P1_D2                                                                                           Absent 
DIMM_P1_E1                                                                                           Absent 
DIMM_P1_E2                                                                                           Absent 
DIMM_P1_F1                                                                                           Absent 
DIMM_P1_F2                                                                                           Absent 
DIMM_P1_G1 Samsung Electronics, Inc. M321R2GA3BB6-CQKET 845643638456347685 DDR5 16384    4800       Enabled 
DIMM_P1_G2                                                                                           Absent 
DIMM_P1_H1                                                                                           Absent 
DIMM_P1_H2                                                                                           Absent 
DIMM_P2_A1                                                                                           Absent 
DIMM_P2_A2                                                                                           Absent 
DIMM_P2_B1                                                                                           Absent 
DIMM_P2_B2                                                                                           Absent 
DIMM_P2_C1                                                                                           Absent 
DIMM_P2_C2                                                                                           Absent 
DIMM_P2_D1                                                                                           Absent 
DIMM_P2_D2                                                                                           Absent 
DIMM_P2_E1                                                                                           Absent 
DIMM_P2_E2                                                                                           Absent 
DIMM_P2_F1                                                                                           Absent 
DIMM_P2_F2                                                                                           Absent 
DIMM_P2_G1                                                                                           Absent 
DIMM_P2_G2                                                                                           Absent 
DIMM_P2_H1                                                                                           Absent 
DIMM_P2_H2                                                                                           Absent 

Output is exported to '192.168.1.10.txt'
------------------------------------------
----------[DEVICE INFO]----------

Model: UCSC-C220-M6S
Serial Number: 15134236326232632622
CIMC FW Version: C220M6.4.3.2d.0.0825231000

----------[CPU INFO]----------
CPU1
        Presence: Enabled
        Model: Intel(R) Xeon(R) Gold 5318N CPU @ 2.10GHz
        Description: Intel(R) Xeon(R) Gold 5318N 2.10 GHz 150W 24C 36.0MB Cache DDR4 2667MHz 6TB
CPU2
        Presence: Enabled
        Model: Intel(R) Xeon(R) Gold 5318N CPU @ 2.10GHz
        Description: Intel(R) Xeon(R) Gold 5318N 2.10 GHz 150W 24C 36.0MB Cache DDR4 2667MHz 6TB

----------[PSU INFO]----------
PSU1
        Presence: Enabled
        Model: PS-2112-9S-LF
        Serial Number: LIT2748AAA6
PSU2
        Presence: Enabled
        Model: PS-2112-9S-LF
        Serial Number: LIT2748AAA6

----------[DRIVE INFO]----------
No drives found or populated.

----------[MEMORY INFO]----------
Slot Name  Manufacturer              Part #           Serial #           Type Size(MB) Speed(MHz) Presence
DIMM_P1_A1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565341 DDR4 32768    3200       Enabled 
DIMM_P1_A2                                                                                         Absent 
DIMM_P1_B1                                                                                         Absent 
DIMM_P1_B2                                                                                         Absent 
DIMM_P1_C1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565341 DDR4 32768    3200       Enabled 
DIMM_P1_C2                                                                                         Absent 
DIMM_P1_D1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565343 DDR4 32768    3200       Enabled 
DIMM_P1_D2                                                                                         Absent 
DIMM_P1_E1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565344 DDR4 32768    3200       Enabled 
DIMM_P1_E2                                                                                         Absent 
DIMM_P1_F1                                                                                         Absent 
DIMM_P1_F2                                                                                         Absent 
DIMM_P1_G1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565345 DDR4 32768    3200       Enabled 
DIMM_P1_G2                                                                                         Absent 
DIMM_P1_H1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565346 DDR4 32768    3200       Enabled 
DIMM_P1_H2                                                                                         Absent 
DIMM_P2_A1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565347 DDR4 32768    3200       Enabled 
DIMM_P2_A2                                                                                         Absent 
DIMM_P2_B1                                                                                         Absent 
DIMM_P2_B2                                                                                         Absent 
DIMM_P2_C1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565348 DDR4 32768    3200       Enabled 
DIMM_P2_C2                                                                                         Absent 
DIMM_P2_D1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565349 DDR4 32768    3200       Enabled 
DIMM_P2_D2                                                                                         Absent 
DIMM_P2_E1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565311 DDR4 32768    3200       Enabled 
DIMM_P2_E2                                                                                         Absent 
DIMM_P2_F1                                                                                         Absent 
DIMM_P2_F2                                                                                         Absent 
DIMM_P2_G1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565312 DDR4 32768    3200       Enabled 
DIMM_P2_G2                                                                                         Absent 
DIMM_P2_H1 Samsung Electronics, Inc. M393A4K40EB3-CWE 687345234264565313 DDR4 32768    3200       Enabled 
DIMM_P2_H2                                                                                         Absent 

Output is exported to '192.168.1.11.txt'
------------------------------------------

Completed.

Script ended at 21:39:45 on 09-23-2025
Total script runtime: 00:01:13
```
