# RUCKUS-SmartZone-Grafana
This repository contains the JSON definitions for SmartZone dashboards using different datasources including influxdb, Infinity and CSV. The dashboards were created using the following versions:
grafana v11.2.0
influxDB 2.7.10
Infinity 2.9.6
CSV 0.6.19

**SmartZone Dashboard 1** has five visualizations. The first four visualizations use influxdb and a python script to fetch data from SZ using API calls, and then create the points in a bucket in influxdb.
The access point table is created using Infinity to send API calls directly to SmarZone. A variable is used to store the service ticket.

**sz_grafana.py** is the python script used to make API call to SmartZone, and to create a time-series by sending points to a influxdb bucket. It is used by SmartZone Dashboard 1 and SmartZone Dashboard 2.
