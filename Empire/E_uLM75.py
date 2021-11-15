from math import floor
import time
import machine

class E_uLM75(object):
    _address = 0x4f
    _error = "None"
    _last_results = (0,0)
    _last_read = 0
    _currentTemp = 0
    _tempValues = []

    def __init__(self, i2cInput, address=0x4f):
        self.i2c = i2cInput
        self._address = address
        
        self._tempTimer = machine.Timer(2)
        self._tempTimer.init(period=1000, mode=machine.Timer.PERIODIC, callback=self._updateTemp) 

    def _get_output(self):
        """Return raw output from the LM75 sensor."""
        output = self.i2c.readfrom(self._address, 2)
        return output[0], output[1]

    def _get_temp(self):
        """Return a tuple of (temp_c, point)."""
        try:
            temp = self._get_output()
            self._last_results = (int(temp[0]), floor(int(temp[1]) / 23))
            return self._last_results[0]*10+self._last_results[1]
        except(E):
            self._error = E
            return 0.0
        
    def _updateTemp(self,caller):
        if len(self._tempValues) < 7:
            self._tempValues.append(self._get_temp())
        else:
            self._currentTemp = self._tempValues[3]
            self._tempValues = []
            
    def read(self):
        return self._currentTemp
            
        
