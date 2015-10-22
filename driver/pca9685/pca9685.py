class ServoController(object):

    def __init__(self, bus, address, servo_min=700, servo_max=2300, servo_amp=180):

        self._osc_clock = 25000000
        self._update_rate = 60

        self.address = address
        self.servo_min = servo_min
        self.servo_inc = float(servo_max-servo_min)/servo_amp
        self.servo_max = servo_max
        self.servo_zero = float(servo_max+servo_min)/2
        self.bus = bus
        self.servos = {}

        # configuration
        self.setFrequency(self._update_rate)

    def move(self, id, target_position):

        trim = self.servos[id].trim
        target_position = target_position * (-2*self.servos[id].reverse + 1)
        pulse_width = self.servo_zero + (target_position+trim) * self.servo_inc
        register_value = int(pulse_width * self._update_rate * 4095 / 1000000)
        self._write(id, register_value)
        self.servos[id].current_position = target_position

    def getPosition(self, id):

        register_value = self._read(id)
        pulse_width = (register_value*1000000) / (self._update_rate*4095)
        present_position = ((pulse_width-self.servo_zero)/self.servo_inc-self.servos[id].trim) * (-2*self.servos[id].reverse+1)
        
        return present_position

    def setFrequency(self, update_rate):

        self._update_rate = update_rate

        prescale_value = round(self._osc_clock/(4096*self._update_rate)) - 1

        self.bus.write_byte_data(self.address, 0x00, 0x10)
        self.bus.write_byte_data(self.address, 0xfe, int(prescale_value))
        self.bus.write_byte_data(self.address, 0x00, 0x00)

    def _write(self, id, register_value):

        self.bus.write_byte_data(self.address, id*4+6, 0)
        self.bus.write_byte_data(self.address, id*4+7, 0)
        self.bus.write_byte_data(self.address, id*4+8, register_value)
        self.bus.write_byte_data(self.address, id*4+9, register_value >> 8)

    def _read(self, id):
        register_value = self.bus.read_byte_data(self.address, id*4+8)
        register_value += self.bus.read_byte_data(self.address, id*4+9) << 8
        return register_value

    def sleep(self):
        self.bus.write_byte_data(self.address, 0x00, 0x10)
        self.bus.write_byte_data(self.address, 0x00, 0x00)

    def addServo(self, id, trim):
        if id >= 0 and id <= 15:
            self.servos[id] = Servo(id, trim)
        else:
            raise ValueError('Invalid ID')

class Servo(object):

    def __init__(self, id, trim=0):
        self.id = id
        self.trim = trim
        self.current_position = 0
        self.reverse = False
