import machine

from utils import CachedProperty

class PumpConfig:
    pins = {
            2: machine.Pin(2, machine.Pin.OUT),
            4: machine.Pin(4, machine.Pin.OUT),
            16: machine.Pin(16, machine.Pin.OUT),
            17: machine.Pin(17, machine.Pin.OUT),
            5: machine.Pin(5, machine.Pin.OUT),
            18: machine.Pin(18, machine.Pin.OUT),
            19: machine.Pin(19, machine.Pin.OUT),
            21: machine.Pin(21, machine.Pin.OUT)
        }

    @CachedProperty
    def pump_control_topic(self):
        return b"control/pump"

    @CachedProperty
    def pump_pins(self) -> dict[int, machine.Pin]:
        return self.pins


def get_pump(msg: str, pump_config: PumpConfig) -> tuple[machine.Pin, int]:
    """
    Get the pump pin based on the message
    """
    pump_number, pump_time = msg.split(b":")
    pump = pump_config.pump_pins.get(int(pump_number))
    return pump, int(pump_time)
