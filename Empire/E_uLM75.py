from math import floor
import time

class E_uLM75(object):
    _address = 0x4f
    _error = "None"
    _last_results = (0,0)
    _last_read = 0

    def __init__(self, i2cInput, address=0x4f):
        self.i2c = i2cInput
        self._address = address

    def _get_output(self):
        """Return raw output from the LM75 sensor."""
        output = self.i2c.readfrom(self._address, 2)
        return output[0], output[1]

    def get_temp(self):
        """Return a tuple of (temp_c, point)."""
        if time.ticks_add(self._last_read, 500)<time.ticks_ms():
            try:
                temp = self._get_output()
                self._last_results = (int(temp[0]), floor(int(temp[1]) / 23))
                return self._last_results[0], self._last_results[1]
            except(E):
                self._error = E
                return 0,0
        else:
            self._error = "To fast read, sensor can be read 2x a sec"
            return self._last_read
            
        
