import picore.common as common
import picore.roaming as roaming
import picore.common.Logger as logger
import RPi.GPIO as gpio
import math
import time


class Stopper:
    CONST_CONFIG_SECTION_NAME = 'picore.stopper'
    CONST_CONFIG_STOP_DIST_FRONT = 'distance.front'
    CONST_CONFIG_STOP_DIST_BACK = 'distance.back'

    CONST_PULSE_RATE = 17150

    __log = logger.Logger()

    stop_dist_front = 20
    stop_dist_back = 40
    port_trig = 25
    port_echo = 16
    running = False

    def __init__(self, trig=25, echo=16):
        self.port_trig = trig
        self.port_echo = echo

    def init(self):
        config = common.get_config(roaming.CONST_CONFIG_NAME_ROAMING)
        if config:
            self.__log.info('Found RPi stopper configuration...')
            d_front = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_STOP_DIST_FRONT)
            if d_front:
                self.stop_dist_front = float(d_front)
            d_back = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_STOP_DIST_BACK)
            if d_back:
                self.stop_dist_back = float(d_back)
        else:
            self.__log.warn('No RPi configuration defined. Using defaults...')

        gpio.setmode(gpio.BCM)
        gpio.setup(self.port_trig, gpio.OUT)
        gpio.setup(self.port_echo, gpio.IN)

    def start(self):
        self.running = True
        while self.running:
            self.fire()

    def stop(self):
        self.running = False
        
    def fire(self):
        gpio.output(self.port_trig, False)
        time.sleep(2)  # Let the sensors to settle
        gpio.output(self.port_trig, True)
        time.sleep(0.00001)
        gpio.output(self.port_trig, False)
