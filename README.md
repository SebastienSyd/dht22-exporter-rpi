# DHT22 prometheus exporter

This repository creates a Prometheus exporter container so that metrics can be collected by a Prometheus agent and displayed in any kind of dashboard such as Grafana.

## Run the container

- Copy the [.env.example](./.env.example) file into a `.env` file and fill the values from your own
- Run this command to build and start the container:
```
> docker-compose up -d
...
Starting dht22_exporter_rpi ... done
```
- Verify that the sensor is correctly collecting data with:
```
> docker logs dht22_exporter_rpi
<2022-08-19 12:53:20,747> <INFO> <Set GPIO-Pin to D22 and SleepTime to 15sec>
<2022-08-19 12:53:20,754> <INFO> <Starting Prometheus client on port 9090>
<2022-08-19 12:53:21,106> <INFO> <Temp: 82.9 F / 28.3 C    Humidity: 58.1%>
<2022-08-19 12:53:21,107> <INFO> <Sleeping for 15 seconds>
<2022-08-19 12:53:36,465> <INFO> <Temp: 82.9 F / 28.3 C    Humidity: 59.4%>
<2022-08-19 12:53:36,465> <INFO> <Sleeping for 15 seconds>
<2022-08-19 12:53:51,832> <ERROR> <Checksum did not validate. Try again.>
<2022-08-19 12:54:07,195> <INFO> <Temp: 82.9 F / 28.3 C    Humidity: 58.4%>
<2022-08-19 12:54:07,195> <INFO> <Sleeping for 15 seconds>
<2022-08-19 12:54:22,563> <ERROR> <Checksum did not validate. Try again.>
<2022-08-19 12:54:37,930> <ERROR> <Checksum did not validate. Try again.>
<2022-08-19 12:54:53,298> <INFO> <Temp: 82.9 F / 28.3 C    Humidity: 58.2%>
```
- Verify that the `/metrics` is showing the metrics details with:
```
> curl localhost:9090/metrics
# HELP python_gc_objects_collected_total Objects collected during gc
# TYPE python_gc_objects_collected_total counter
python_gc_objects_collected_total{generation="0"} 100.0
python_gc_objects_collected_total{generation="1"} 273.0
python_gc_objects_collected_total{generation="2"} 0.0
# HELP python_gc_objects_uncollectable_total Uncollectable object found during GC
# TYPE python_gc_objects_uncollectable_total counter
python_gc_objects_uncollectable_total{generation="0"} 0.0
python_gc_objects_uncollectable_total{generation="1"} 0.0
python_gc_objects_uncollectable_total{generation="2"} 0.0
# HELP python_gc_collections_total Number of times this generation was collected
# TYPE python_gc_collections_total counter
python_gc_collections_total{generation="0"} 42.0
python_gc_collections_total{generation="1"} 3.0
python_gc_collections_total{generation="2"} 0.0
# HELP python_info Python platform information
# TYPE python_info gauge
python_info{implementation="CPython",major="3",minor="9",patchlevel="5",version="3.9.5"} 1.0
# HELP process_virtual_memory_bytes Virtual memory size in bytes.
# TYPE process_virtual_memory_bytes gauge
process_virtual_memory_bytes 1.8038784e+07
# HELP process_resident_memory_bytes Resident memory size in bytes.
# TYPE process_resident_memory_bytes gauge
process_resident_memory_bytes 1.1784192e+07
# HELP process_start_time_seconds Start time of the process since unix epoch in seconds.
# TYPE process_start_time_seconds gauge
process_start_time_seconds 1.66091359955e+09
# HELP process_cpu_seconds_total Total user and system CPU time spent in seconds.
# TYPE process_cpu_seconds_total counter
process_cpu_seconds_total 0.97
# HELP process_open_fds Number of open file descriptors.
# TYPE process_open_fds gauge
process_open_fds 7.0
# HELP process_max_fds Maximum number of open file descriptors.
# TYPE process_max_fds gauge
process_max_fds 1.048576e+06
# HELP dht22_temperature_celsius Temperature in celsius provided by dht sensor
# TYPE dht22_temperature_celsius gauge
dht22_temperature_celsius{city="mycity",country="mycountry",location="livingroom"} 28.3
# HELP dht22_temperature_fahrenheit Temperature in fahrenheit provided by dht sensor
# TYPE dht22_temperature_fahrenheit gauge
dht22_temperature_fahrenheit{city="mycity",country="mycountry",location="livingroom"} 82.9
# HELP dht22_humidity Humidity in percents provided by dht sensor
# TYPE dht22_humidity gauge
dht22_humidity{city="mycity",country="mycountry",location="livingroom"} 59.4
# HELP dht22_read_failures_total Count of the DHT22 sensor read failures
# TYPE dht22_read_failures_total counter
dht22_read_failures_total{city="mycity",country="mycountry",location="livingroom"} 20.0
# HELP dht22_read_failures_created Count of the DHT22 sensor read failures
# TYPE dht22_read_failures_created gauge
dht22_read_failures_created{city="mycity",country="mycountry",location="livingroom"} 1.660913631833311e+09
```

## 

## Known issues

The collection of the data from the sensor is not 100% available all the time. Sometimes the sensor fails to collect it and the error `Checksum did not validate. Try again.` is thrown into the logs.

When this happens, this increments the counter `dht22_read_failures`

## Test

Tested on Raspberry 4 model B on Raspbian GNU/Linux 10 (buster)

## Reference

The code in this repository has been inspired by:
- https://github.com/Tob1as/rpi-sensors
- https://github.com/clintjedwards/dht22_exporter