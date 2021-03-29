import picore.common as common
import picore.common.Config as cfg
import picore.roaming as roaming
import picore.common.Logger as logger
import RPi.GPIO as gpio
import NumPy as numpy

class RPiMovement:
    CONST_CONFIG_SECTION_NAME = 'picore.movement'
    CONST_CONFIG_WHEEL_DIA = 'wheel.diameter'
    CONST_CONFIG_WHEEL_DIST = 'wheel.distance'
    CONST_CONFIG_MAX_SPEED = 'speed.max'

    CONST_GPIO_M1_0 = 17
    CONST_GPIO_M1_1 = 22
    CONST_GPIO_EN_0 = 12
    CONST_GPIO_M2_0 = 23
    CONST_GPIO_M2_1 = 24
    CONST_GPIO_EN_1 = 13

    __log = logger.Logger()

    size_wheel_dia = 65
    size_wheel_dist = 170
    max_speed = 10

    en_0 = None
    en_1 = None

    def init(self):
        config = common.get_config(roaming.CONST_CONFIG_NAME_ROAMING)
        if config:
            self.__log.info('Found RPi movement configuration...')
            w_dia = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_WHEEL_DIA)
            if w_dia:
                self.size_wheel_dia = float(w_dia)
            w_dist = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_WHEEL_DIST)
            if w_dist:
                self.size_wheel_dist = float(w_dist)
            m_speed = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_MAX_SPEED)
            if m_speed:
                self.max_speed = float(m_speed)
        else:
            self.__log.warn('No RPi configuration defined. Using defaults...')

        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)
        gpio.setup(self.CONST_GPIO_M1_0, gpio.OUT)
        gpio.setup(self.CONST_GPIO_M1_1, gpio.OUT)
        gpio.setup(self.CONST_GPIO_EN_0, gpio.OUT)
        gpio.setup(self.CONST_GPIO_M2_0, gpio.OUT)
        gpio.setup(self.CONST_GPIO_M2_1, gpio.OUT)
        gpio.setup(self.CONST_GPIO_EN_1, gpio.OUT)

        self.en_0 = gpio.PWM(self.CONST_GPIO_EN_0, 100)
        self.en_1 = gpio.PWM(self.CONST_GPIO_EN_1, 100)

    def forward(self, speed=-1, distance=-1):
        gpio.output(self.CONST_GPIO_M1_0, False)
        gpio.output(self.CONST_GPIO_M1_1, True)
        gpio.output(self.CONST_GPIO_M2_0, True)
        gpio.output(self.CONST_GPIO_M2_1, False)

    def reverse(self, speed=-1, distance=-1):
        gpio.output(self.CONST_GPIO_M1_0, True)
        gpio.output(self.CONST_GPIO_M1_1, False)
        gpio.output(self.CONST_GPIO_M2_0, False)
        gpio.output(self.CONST_GPIO_M2_1, True)

    def left_turn(self, degrees=15):
        gpio.output(self.CONST_GPIO_M1_0, True)
        gpio.output(self.CONST_GPIO_M1_1, False)
        gpio.output(self.CONST_GPIO_M2_0, True)
        gpio.output(self.CONST_GPIO_M2_1, False)

    def right_turn(self, degrees=15):
        gpio.output(self.CONST_GPIO_M1_0, False)
        gpio.output(self.CONST_GPIO_M1_1, True)
        gpio.output(self.CONST_GPIO_M2_0, False)
        gpio.output(self.CONST_GPIO_M2_1, True)

    def stop(self):
        gpio.output(self.CONST_GPIO_M1_0, False)
        gpio.output(self.CONST_GPIO_M1_1, False)
        gpio.output(self.CONST_GPIO_M2_0, False)
        gpio.output(self.CONST_GPIO_M2_1, False)
        gpio.cleanup()
