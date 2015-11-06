import os
from board.arietta.pin import PinException


pin_map = {7: {'id': '23', 'name': 'pioA23'},
           8: {'id': '22', 'name': 'pioA22'},
           10: {'id': '21', 'name': 'pioA21'},
           11: {'id': '24', 'name': 'pioA24'},
           12: {'id': '31', 'name': 'pioA31'},
           13: {'id': '25', 'name': 'pioA25'},
           14: {'id': '30', 'name': 'pioA30'},
           15: {'id': '26', 'name': 'pioA26'},
           17: {'id': '27', 'name': 'pioA27'},
           19: {'id': '28', 'name': 'pioA28'},
           21: {'id': '29', 'name': 'pioA29'},
           23: {'id': '0', 'name': 'pioA0'},
           24: {'id': '1', 'name': 'pioA1'},
           25: {'id': '8', 'name': 'pioA8'},
           26: {'id': '7', 'name': 'pioA7'},
           27: {'id': '6', 'name': 'pioA6'},
           28: {'id': '5', 'name': 'pioA5'},
           29: {'id': '92', 'name': 'pioC28'},
           30: {'id': '91', 'name': 'pioC27'},
           31: {'id': '68', 'name': 'pioC4'},
           32: {'id': '95', 'name': 'pioC31'},
           33: {'id': '67', 'name': 'pioC3'},
           34: {'id': '43', 'name': 'pioB11'},
           35: {'id': '66', 'name': 'pioC2'},
           36: {'id': '44', 'name': 'pioB12'},
           37: {'id': '65', 'name': 'pioC1'},
           38: {'id': '45', 'name': 'pioB13'},
           39: {'id': '64', 'name': 'pioC0'},
           40: {'id': '46', 'name': 'pioB14'},
           }


class Digital(object):
    def __init__(self, pin, mode):
        self.pin = pin
        self.id = pin_map[self.pin]['id']
        self.name = pin_map[self.pin]['name']
        self.path = '/sys/class/gpio/%s/value' % self.name
        os.system('echo %s > /sys/class/gpio/export' % self.id)
        if mode in ['in', 'out']:
            os.system('echo %s > /sys/class/gpio/%s/direction' % (mode, self.name))
            self._mode = mode
        else:
            raise PinException()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, mode):
        if not self.mode == mode:
            if mode in ['in', 'out']:
                os.system('echo %s > /sys/class/gpio/%s/direction' % (mode, self.name))
                self._mode = mode
            else:
                raise PinException()

    def read(self):
        with open(self.path, 'r') as f:
            return f.read()

    def write(self, value):
        with open(self.path, 'w+') as f:
            f.write(str(value))
