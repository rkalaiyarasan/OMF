
'''
This program will collect the data from Linux and Windows machines and send the collected data over OMF to PI using PI Connector Relay.

Versions Used:

    PI Connector relay 1.1.166.2514
    OMF : 1.0
    Operating Systems Tested for Data Collection:
        1. CentOS Linux release 7.2.1511 (Core)
        2. Windows 7 Enterprise SP1

***PythonDemo program provided as a part of the Connector Relay is used as a sample and the code is also being reused here***

'''


# Importing the required packages

import sys, json, random, time, platform, requests, socket, datetime, random

# Importing the package responsible for collecting Machine Performance Data

import LinuxPerfData


relay_url = "http://Ram-PIINT2:8118/ingress/messages"
producer_token = "Windows"

# ************************************************************************

#Collect Linux Performance Data

global PerfData, PerfData_Keys, PerfData_Values

PerfData = LinuxPerfData.collectStats()
PerfData_Keys = list(PerfData.keys())
PerfData_Values = list(PerfData.values())


# ************************************************************************
# Define the stream values which are being sent to PI via Connector Relay

def create_data_values_stream_message(target_stream_id):
    data_values_JSON = ''
    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'
    data_values_JSON = [
        {
            "containerid": target_stream_id,
            "values": [
                {
                    "Time": timestamp,
                    PerfData_Keys[0]: PerfData_Values[0],
                    PerfData_Keys[1]: PerfData_Values[1],
                    PerfData_Keys[2]: PerfData_Values[2],
                    PerfData_Keys[3]: PerfData_Values[3],
                    PerfData_Keys[4]: PerfData_Values[4],
                    PerfData_Keys[5]: PerfData_Values[5],
                    PerfData_Keys[6]: PerfData_Values[6],
                    PerfData_Keys[7]: PerfData_Values[7]
                }
            ]
        }
    ]
    print(data_values_JSON)
    return data_values_JSON

# ************************************************************************
# POST the data to PI via Connector relay using OMF 1.0 protocol

def sendOMFMessageToEndPoint(message_type, OMF_data):
        try: 
                msg_header = {'producertoken': producer_token, 'messagetype': message_type, 'action': 'create', 'messageformat': 'JSON', 'omfversion': '1.0'}   
                #msg_header = {'producertoken': producer_token, 'messagetype': message_type, 'action': 'update', 'messageformat': 'JSON', 'omfversion': '1.0'}   
                response = requests.post(relay_url, headers=msg_header, data=json.dumps(OMF_data), verify=False, timeout=30)
                print('Response from relay from the initial "{0}" message: {1} {2}'.format(message_type, response.status_code, response.text))
        except Exception as e:
                print(str(datetime.datetime.now()) + " An error ocurred during web request: " + str(e))		

# ************************************************************************
# Define the Asset Hierarchy, Assets and related attributes

types = [
    {
        "id": "type_Machine",
        "type": "object",
        "classification": "static",
        "properties": {
                "Name": {
                        "type": "string",
                        "isindex": True
                },
                "Location": {
                        "type": "string"
                }
        }
	},
	{
        "id": "type_measurement",
        "type": "object",
        "classification": "dynamic",
        "properties": {
                "Time": {
                        "format": "date-time",
                        "type": "string",
                        "isindex": True
                },
                PerfData_Keys[0]: {
                        "type": "number"
                },
                PerfData_Keys[1]: {
                        "type": "number"
                },
                PerfData_Keys[2]: {
                    "type": "number"
                },
                PerfData_Keys[3]: {
                    "type": "number"
                },
                PerfData_Keys[4]: {
                    "type": "number"
                },
                PerfData_Keys[5]: {
                    "type": "number"
                },
                PerfData_Keys[6]: {
                    "type": "number"
                },
                PerfData_Keys[7]: {
                    "type": "number"
                }
        }
    }
]

containers = [{
        "id": "measurement",
        "typeid": "type_measurement"
}]

staticData = [{
        "typeid": "type_Machine",
        "values": [{
                "Name": "Machine1",
                "Location": "Singapore"
                },
                   {
                "Name": "Machine2",
                "Location": "America"
                },
                   {
                "Name": "Machine3",
                "Location": "India"
                },
                   {
                "Name": "Machine4",
                "Location": "Canada"
                }]
}]

linkData = [{
        "typeid": "__Link",
        "values": [{
                "source": {
                        "typeid": "type_Machine",
                        "index": "_ROOT"
                },
                "target": {
                        "typeid": "type_Machine",
                        "index": "Machine1"
                }
                },
                {
                "source": {
                        "typeid": "type_Machine",
                        "index": "_ROOT"
                },
                "target": {
                        "typeid": "type_Machine",
                        "index": "Machine2"
                }
                },
                {
                "source": {
                        "typeid": "type_Machine",
                        "index": "_ROOT"
                },
                "target": {
                        "typeid": "type_Machine",
                        "index": "Machine3"
                }
                },
                {
                "source": {
                        "typeid": "type_Machine",
                        "index": "_ROOT"
                },
                "target": {
                        "typeid": "type_Machine",
                        "index": "Machine4"
                }
                },
                {
                "source": {
                        "typeid": "type_Machine",
                        "index": "Machine1"
                },
                "target": {
                        "containerid": "measurement"
                }
                },
                {
                 "source": {
                        "typeid": "type_Machine",
                        "index": "Machine2"
                },
                "target": {
                        "containerid": "measurement"
                }
                },
                {
                 "source": {
                        "typeid": "type_Machine",
                        "index": "Machine3"
                },
                "target": {
                        "containerid": "measurement"
                }
                },
                {
                 "source": {
                        "typeid": "type_Machine",
                        "index": "Machine4"
                },
                "target": {
                        "containerid": "measurement"
                }
                }]
        }]


requests.packages.urllib3.disable_warnings()

    
sendOMFMessageToEndPoint("Type", types)
#time.sleep(1)
sendOMFMessageToEndPoint("Container", containers)
# time.sleep(1)
sendOMFMessageToEndPoint("Data", staticData)
# time.sleep(1)
sendOMFMessageToEndPoint("Data", linkData)
# time.sleep(1)

# ************************************************************************
# POST the events continuously

i = True

while i:
    values = create_data_values_stream_message("measurement")
    sendOMFMessageToEndPoint("Data", values)
    time.sleep(1)
    #i += 1
