import machine
from umqtt.simple import MQTTClient

from utils import CachedProperty

# Sensors configuration. Pins: 34, 35, 32, 33, 36, 39
class AdcConfig:
    pins = {
            34: machine.ADC(machine.Pin(34)),
            35: machine.ADC(machine.Pin(35)),
            32: machine.ADC(machine.Pin(32)),
            33: machine.ADC(machine.Pin(33)),
            36: machine.ADC(machine.Pin(36)),
            39: machine.ADC(machine.Pin(39))
        }

    @CachedProperty
    def sensor_values_topic(self):
        return b"sensors/values"

    @CachedProperty
    def adc_pins(self) -> dict[int, machine.ADC]:
        for pin in self.pins.values():
            pin.atten(machine.ADC.ATTN_11DB)        
        return self.pins


def read_sensors(mqtt_client: MQTTClient, adc_config: AdcConfig):
    """
    Function to read and publish sensor values
    """
    for pin, adc in adc_config.adc_pins.items():
        sensor_values = b":".join([str(adc.read()).encode("utf-8"), str(pin).encode("utf-8")])
        print("Publishing sensor value:", sensor_values)
        mqtt_client.publish(adc_config.sensor_values_topic, sensor_values)
