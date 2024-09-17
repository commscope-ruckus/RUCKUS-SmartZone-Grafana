# RUCKUS-SmartZone-Grafana
This repository contains the JSON definitions for SmartZone dashboards using different datasources including influxdb, Infinity and CSV.

Dashboard 1 has five visualizations. The first four visualizations use influxdb and a python script to fetch data from SZ using API calls, and then create the points in a bucket in influxdb.
The access point table is created using Infinity to send API calls directly to SmarZone. A variable is used to store the service ticket.
