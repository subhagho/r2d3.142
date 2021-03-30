import picore.common as common
import picore.roaming as roaming
import picore.common.Logger as logger
import RPi.GPIO as gpio
import math
import time


class MovementState:
    set_speed = 0.0
    current_speed = 0.0
    direction = 1

    def copy(self):
        ms = MovementState()
        ms.set_speed = self.set_speed
        ms.current_speed = self.current_speed
        ms.direction = self.direction
        return ms


class RPiMovement:
    CONST_CONFIG_SECTION_NAME = 'picore.movement'
    CONST_CONFIG_WHEEL_DIA = 'wheel.diameter'
    CONST_CONFIG_WHEEL_DIST = 'wheel.distance'
    CONST_CONFIG_MAX_RPM = 'rpm.max'
    CONST_CONFIG_TURN_RPM = 'rpm.turning'

    CONST_GPIO_M1_0 = 17
    CONST_GPIO_M1_1 = 22
    CONST_GPIO_EN_0 = 12
    CONST_GPIO_M2_0 = 23
    CONST_GPIO_M2_1 = 24
    CONST_GPIO_EN_1 = 13

    __log = logger.Logger()

    size_wheel_dia = 65.0
    size_wheel_dist = 170.0
    max_rpm = 50.0
    turn_rpm = 10.0
    max_speed = 10.0
    movement_state = MovementState()

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
            m_rpm = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_MAX_RPM)
            if m_rpm:
                self.max_speed = float(m_rpm)
            t_rpm = config.get_option(self.CONST_CONFIG_SECTION_NAME, self.CONST_CONFIG_TURN_RPM)
            if t_rpm:
                self.turn_rpm = float(t_rpm)
        else:
            self.__log.warn('No RPi configuration defined. Using defaults...')

        self.max_speed = self.size_wheel_dia * math.pi * self.max_rpm
        self.movement_state.set_speed = self.max_speed * 0.25

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
        self.change_speed(0)

    def forward(self, speed=-1, distance=-1):
        t = -1.0
        if speed > 0:
            self.reset_speed(speed)
        if self.movement_state.set_speed <= 0:
            return
        if distance > 0:
            t = distance / self.movement_state.set_speed

        self.movement_state.direction = 1
        gpio.output(self.CONST_GPIO_M1_0, False)
        gpio.output(self.CONST_GPIO_M1_1, True)
        gpio.output(self.CONST_GPIO_M2_0, True)
        gpio.output(self.CONST_GPIO_M2_1, False)
        if t > 0:
            time.sleep(t)
            self.stop()
            self.__log.debug('Stopped after [' + str(t) + ' secs]')

    def reverse(self, speed=-1, distance=-1):
        t = -1.0
        if speed > 0:
            self.reset_speed(speed)
        if self.movement_state.set_speed <= 0:
            return
        if distance > 0:
            t = distance / self.movement_state.set_speed

        self.movement_state.direction = -1
        gpio.output(self.CONST_GPIO_M1_0, True)
        gpio.output(self.CONST_GPIO_M1_1, False)
        gpio.output(self.CONST_GPIO_M2_0, False)
        gpio.output(self.CONST_GPIO_M2_1, True)
        if t > 0:
            time.sleep(t)
            self.stop()
            self.__log.debug('Stopped after [' + str(t) + ' secs]')

    def turn(self, degrees=15):
        ms = self.movement_state.copy()
        self.set_turning_speed()
        t = self.compute_turn_time(degrees)
        if t <= 0:
            return
        if degrees > 0:
            self.right_turn()
        else:
            self.left_turn()

        time.sleep(t)

        self.reset_speed(ms.set_speed)
        if ms.current_speed > 0:
            if ms.direction == 1:
                self.forward()
            elif ms.direction == -1:
                self.reverse()

    def left_turn(self):
        gpio.output(self.CONST_GPIO_M1_0, True)
        gpio.output(self.CONST_GPIO_M1_1, False)
        gpio.output(self.CONST_GPIO_M2_0, True)
        gpio.output(self.CONST_GPIO_M2_1, False)

    def right_turn(self):
        gpio.output(self.CONST_GPIO_M1_0, False)
        gpio.output(self.CONST_GPIO_M1_1, True)
        gpio.output(self.CONST_GPIO_M2_0, False)
        gpio.output(self.CONST_GPIO_M2_1, True)

    def compute_turn_time(self, degrees):
        s = self.turn_rpm * math.pi * self.size_wheel_dia
        w = s * 2 / self.size_wheel_dist
        r = degrees * math.pi / 180
        t = r / w

        return t

    def reset_speed(self, speed):
        delta = speed - self.movement_state.set_speed
        pct = delta / self.movement_state.set_speed * 100
        self.change_speed(pct)

    def change_speed(self, pct):
        delta = self.movement_state.set_speed * pct / 100
        self.movement_state.set_speed += delta
        if self.movement_state.set_speed > self.max_speed:
            self.movement_state.set_speed = self.max_speed
        elif self.movement_state.set_speed <= 0 and self.movement_state.current_speed > 0:
            self.stop()
            return
        if self.movement_state.current_speed > 0:
            rpm = self.movement_state.set_speed / self.max_speed * 100
            self.en_0.ChangeDutyCycle(rpm)
            self.en_1.ChangeDutyCycle(rpm)
            self.movement_state.current_speed = self.movement_state.set_speed
        self.__log.debug(
            'Changed speed to [' + str(self.movement_state.set_speed) + '][current speed=' + str(
                self.movement_state.current_speed) + ']')

    def set_turning_speed(self):
        self.en_0.ChangeDutyCycle(self.turn_rpm)
        self.en_1.ChangeDutyCycle(self.turn_rpm)

    def stop(self):
        self.movement_state.current_speed = 0
        gpio.output(self.CONST_GPIO_M1_0, False)
        gpio.output(self.CONST_GPIO_M1_1, False)
        gpio.output(self.CONST_GPIO_M2_0, False)
        gpio.output(self.CONST_GPIO_M2_1, False)
        gpio.cleanup()
        self.movement_state.direction = 1
        self.__log.debug('Stopped...')
