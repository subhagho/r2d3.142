import pir2.common as common
import pir2.roaming as roaming
import pir2.common.Logger as Logger
import RPi.GPIO as gpio
import time


class Stopper:
    CONST_CONFIG_SECTION_NAME = 'pir2.stopper'
    CONST_CONFIG_STOP_DIST = 'distance.stop'
    CONST_CONFIG_TRIG_PORT = 'port.trigger'
    CONST_CONFIG_ECHO_PORT = 'port.echo'

    CONST_PULSE_RATE = 17150

    __log = Logger.Logger()

    stop_dist = 20
    port_trig = 25
    port_echo = 16
    running = False
    callback = None
    name = None

    def __init__(self, name, trig=25, echo=16, callback=None):
        self.port_trig = trig
        self.port_echo = echo
        self.callback = callback
        self.name = name

    def init(self):
        config = common.get_config(roaming.CONST_CONFIG_NAME_ROAMING)
        if config:
            self.__log.info('Found RPi stopper configuration...')
            d_stop = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_STOP_DIST + '.' + self.name)
            if d_stop:
                self.stop_dist = float(d_stop)
            self.__log.info('[' + self.name + '] Using stop distance = ' + str(d_stop))
            p_trig = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_TRIG_PORT + '.' + self.name)
            if p_trig:
                self.port_trig = int(p_trig)
            p_echo = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_ECHO_PORT + '.' + self.name)
            if p_echo:
                self.port_echo = int(p_echo)
            self.__log.info('Using GPIO pins [trigger=' + str(self.port_trig) + ', echo=' + str(self.port_echo) + ']...')
        else:
            self.__log.warn('No RPi configuration defined. Using defaults...')

        gpio.setmode(gpio.BCM)
        gpio.setup(self.port_trig, gpio.OUT)
        gpio.setup(self.port_echo, gpio.IN)
        self.__log.info('Initialized Stopper [name=' + self.name + ']')

    def start(self):
        self.running = True
        while self.running:
            self.fire()

    def stop(self):
        self.running = False

    def fire(self):
        i = 0
        avg_dist = 0
        for i in range(5):
            gpio.output(self.port_trig, False)
            time.sleep(0.1)  # Let the sensors to settle
            gpio.output(self.port_trig, True)
            time.sleep(0.00001)
            gpio.output(self.port_trig, False)
            pulse_start = -1
            pulse_end = 1
            while gpio.input(self.port_echo) == 0:  # Check whether the ECHO is LOW
                pulse_start = time.time()
            while gpio.input(self.port_echo) == 1:  # Check whether the ECHO is HIGH
                pulse_end = time.time()
            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * self.CONST_PULSE_RATE

            distance = round(distance + 1.15, 2)
            avg_dist += distance
        avg_dist = avg_dist / 5

        if avg_dist >= self.stop_dist:
            self.callback(self.name, avg_dist)
            self.__log.info('Sending stop signal [name=' + self.name + '][distance=' + str(avg_dist) + ']')
        else:
            time.sleep(0.2)
