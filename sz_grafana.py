#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 18:15:55 2024

@author: marcelomolinari
"""

import random, time
import influxdb_client
import warnings, csv
warnings.filterwarnings("ignore", message="Unverified HTTPS request")
from influxdb_client.client.write_api import SYNCHRONOUS
from vSZ_calls_Q322 import vSZ_calls

bucket = "SmartZone"
org = "RUCKUS"
influxToken = "your api token"
url= "http://localhost:8086"

host = 'your SZ FQDN'
username = 'your SZ username'
password = 'your SZ password'

SmartZone = vSZ_calls()

token = SmartZone.getToken(host, username, password)
domain = SmartZone.getDomainByName(host, 'Administration Domain', token)
domainId = domain['list'][0]['id']

client = influxdb_client.InfluxDBClient(
    url = url,
    token = influxToken,
    org = org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    temperature = float(random.randrange(25, 28, 1))
    p = influxdb_client.Point("my_measurement").tag("location", "Sunnyvale").field("temperature", 24 + (1.5 * (temperature / 10))).field("humidity", 26)
    write_api.write(bucket=bucket, org=org, record=p)
    
    apTotal = len(SmartZone.queryAPs(host, 'DOMAIN', domainId, 200, token))
    q = influxdb_client.Point("my_measurement").tag("Number of APs", "All domains").field("number", apTotal)
    write_api.write(bucket=bucket, org=org, record=q)
    
    apOnline = len(SmartZone.queryOnlineAPs(host, 'DOMAIN', domainId, 200, token))
    r = influxdb_client.Point("my_measurement").tag("Number of Online APs", "All domains").field("online", apOnline)
    write_api.write(bucket=bucket, org=org, record=r)

    clients = len(SmartZone.getClients(host, 'DOMAIN', domainId, 200, token))
    s = influxdb_client.Point("my_measurement").tag("Number of Clients", "All domains").field("clients", clients)
    write_api.write(bucket=bucket, org=org, record=s)
    
    totalTraffic = SmartZone.getTotalTraffic(host, 'DOMAIN', domainId, 200, token)
    t = influxdb_client.Point("my_measurement").tag("Total Traffic", "All domains").field("traffic", totalTraffic)
    write_api.write(bucket=bucket, org=org, record=t)
    
    csv_file_1 = open('szAPs.csv', mode='w', encoding='UTF8') 
    writer = csv.writer(csv_file_1)
    writer.writerow(['Access Point Name', 'IP Address', 'Status', 'Model', 
                  'Serial Number', 'MAC Address', 'Zone', 'Number of Clients'])
    apModelsDict = {}
    apList = SmartZone.queryAPs(host, 'DOMAIN', domainId, 200, token)
    for ap in apList:
        zone = (SmartZone.getZoneName(host, ap['zoneId'], token))
        writer.writerow([ap['deviceName'], ap['ip'], ap['status'], 
                          ap['model'], ap['serial'], ap['apMac'], zone,
                          ap['numClients']])
        if not ap['model'] in apModelsDict:
            apModelsDict[ap['model']] = 1
        else:
            apModelsDict[ap['model']] += 1
            
    csv_file_2 = open('szAPmodels.csv', mode='w', encoding='UTF8') 
    writer = csv.writer(csv_file_2)
    writer.writerow(['Model', 'Number'])
    for key,value in apModelsDict.items():
        writer.writerow([key, value])
        
    time.sleep(15)

