import os
import time
import board
import adafruit_dht
from prometheus_client import Gauge, Counter, start_http_server
import logging

logging.basicConfig(format='<%(asctime)s> <%(levelname)s> <%(message)s>', level=logging.INFO)

# Variables
DHT_DATA_PIN = int(os.environ.get('GPIO_PIN_DHT22', 22))
DHT_READ_TIMEOUT = float(os.environ.get('DHT22_SLEEPTIME', 15))
PROMETHEUS_PORT = 9090
PROMETHEUS_LABEL_NAMES = [
  "location",
  "city",
  "country"
]
PROMETHEUS_LABEL_VALUES = [
  str(os.environ.get('PROMETHEUS_LABEL_LOCATION_VALUE', '')),
  str(os.environ.get('PROMETHEUS_LABEL_CITY_VALUE', '')),
  str(os.environ.get('PROMETHEUS_LABEL_COUNTRY_VALUE', ''))
]
logging.info("Set GPIO-Pin to D%s and SleepTime to %.0fsec" % (DHT_DATA_PIN, DHT_READ_TIMEOUT))

# Create a metric to track time spent and requests made.
dht22_temperature_celsius = Gauge(
  'dht22_temperature_celsius',
  'Temperature in celsius provided by dht sensor',
  labelnames=PROMETHEUS_LABEL_NAMES
)
dht22_temperature_fahrenheit = Gauge(
  'dht22_temperature_fahrenheit',
  'Temperature in fahrenheit provided by dht sensor',
  labelnames=PROMETHEUS_LABEL_NAMES
)
dht22_humidity = Gauge(
  'dht22_humidity',
  'Humidity in percents provided by dht sensor',
  labelnames=PROMETHEUS_LABEL_NAMES
)
dht22_read_failures = Counter(
  'dht22_read_failures',
  'Count of the DHT22 sensor read failures',
  labelnames=PROMETHEUS_LABEL_NAMES
)

# GPIO <https://www.raspberrypi.org/documentation/usage/gpio/>
# dictionary idea <https://github.com/adafruit/Adafruit_CircuitPython_DHT/issues/57>
boardspins = {
  'D0': board.D0, 'D1': board.D1, 'D2': board.D2, 'D3': board.D3, 'D4': board.D4,
  'D5': board.D5, 'D6': board.D6, 'D7': board.D7, 'D8': board.D8, 'D9': board.D9,
  'D10': board.D10, 'D11': board.D11, 'D12': board.D12, 'D13': board.D13, 'D14': board.D14,
  'D15': board.D15, 'D16': board.D16, 'D17': board.D17, 'D18': board.D18, 'D19': board.D19,
  'D20': board.D20, 'D21': board.D21, 'D22': board.D22, 'D23': board.D23, 'D24': board.D24,
  'D25': board.D25, 'D26': board.D26, 'D27': board.D27
}

pin = boardspins['D' + str(DHT_DATA_PIN)]

# Initialize the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(pin)
start_http_server(PROMETHEUS_PORT)

logging.info("Starting Prometheus client on port %d" % (PROMETHEUS_PORT))

while True:
  try:
    # Get values and print
    temperature_c = dhtDevice.temperature
    temperature_f = temperature_c * (9 / 5) + 32
    humidity = dhtDevice.humidity

    temperature_c = float(round(temperature_c,1))
    temperature_f = float(round(temperature_f,1))
    humidity = float(round(humidity,1))
    logging.info("Temp: %s F / %s C    Humidity: %s%%" % (temperature_f, temperature_c, humidity))

    dht22_humidity.labels( \
      location=PROMETHEUS_LABEL_VALUES[0], \
      city=PROMETHEUS_LABEL_VALUES[1], \
      country=PROMETHEUS_LABEL_VALUES[2] \
    ) \
    .set('{0:0.1f}'.format(humidity))

    dht22_temperature_fahrenheit.labels( \
      location=PROMETHEUS_LABEL_VALUES[0], \
      city=PROMETHEUS_LABEL_VALUES[1], \
      country=PROMETHEUS_LABEL_VALUES[2] \
    ) \
    .set('{0:0.1f}'.format(temperature_f))

    dht22_temperature_celsius.labels( \
      location=PROMETHEUS_LABEL_VALUES[0], \
      city=PROMETHEUS_LABEL_VALUES[1], \
      country=PROMETHEUS_LABEL_VALUES[2] \
    ) \
    .set('{0:0.1f}'.format(temperature_c))

  except RuntimeError as error:
    # Errors happen fairly often, DHT's are hard to read, just keep going
    logging.error(error.args[0])
    dht22_read_failures.labels( \
      location=PROMETHEUS_LABEL_VALUES[0], \
      city=PROMETHEUS_LABEL_VALUES[1], \
      country=PROMETHEUS_LABEL_VALUES[2] \
    ) \
    .inc(1)

    time.sleep(DHT_READ_TIMEOUT)
    continue
  except Exception as error:
    dhtDevice.exit()
    raise error

  logging.info("Sleeping for %d seconds" % (DHT_READ_TIMEOUT))
  time.sleep(DHT_READ_TIMEOUT)
