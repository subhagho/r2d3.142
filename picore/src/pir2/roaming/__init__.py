import pir2.roaming.stopper as stopper
import pir2.roaming.move as move
import pir2.common.Logger as Logger
import pir2.common as common
import time
import threading

CONST_CONFIG_NAME_ROAMING = 'ROAMING'
CONST_CONFIG_ENABLE_MOVE = 'enable.movement'
CONST_CONFIG_ENABLE_DIST_SENSOR = 'enable.sensor.distance'

CONST_FRONT_TRIG = 25
CONST_FRONT_ECHO = 20
CONST_BACK_TRIG = 8
CONST_BACK_ECHO = 21

enable_move = False
enable_dist = False

__log = Logger.Logger()

mover = None
front_stopper = None
back_stopper = None
f_thread = None
b_thread = None


def stop_callback(name: str, distance: float) -> None:
    global mover
    if enable_move and mover:
        mover.stop()

    __log.info('Stop called by [' + name + '][distance=' + str(distance) + ']...')


def __stopper_thread_init(__stopper: stopper.Stopper) -> None:
    __stopper.init()
    time.sleep(2)
    __stopper.start()


def init():
    global f_thread, b_thread, front_stopper, back_stopper, mover, enable_move, enable_dist
    __log.info('Initializing Roaming...')

    config = common.get_config(CONST_CONFIG_NAME_ROAMING)
    if config:
        enable = config.get_option(CONST_CONFIG_NAME_ROAMING, CONST_CONFIG_ENABLE_MOVE)
        if enable:
            enable_move = bool(enable)
            if enable_move:
                __log.info('Enabled movement driver...')
                mover = move.RPiMovement()
                mover.init()
        enable = config.get_option(CONST_CONFIG_NAME_ROAMING, CONST_CONFIG_ENABLE_DIST_SENSOR)
        if enable:
            enable_dist = bool(enable)
            if enable_dist:
                __log.info('Enabled distance sensor driver...')
                front_stopper = stopper.Stopper('front', CONST_FRONT_TRIG, CONST_FRONT_ECHO, stop_callback)
                back_stopper = stopper.Stopper('back', CONST_BACK_TRIG, CONST_BACK_ECHO, stop_callback)

                f_thread = threading.Thread(target=__stopper_thread_init, args=(front_stopper,))
                b_thread = threading.Thread(target=__stopper_thread_init, args=(back_stopper,))

                f_thread.start()
                b_thread.start()


def shutdown():
    global f_thread, b_thread, front_stopper, back_stopper, mover, enable_move, enable_dist
    __log.info('Shutting down Roaming...')

    if enable_move and mover:
        mover.stop()
        mover = None
        __log.info('Stopped movement driver...')

    if enable_dist:
        if front_stopper:
            front_stopper.stop()
            front_stopper = None
        if back_stopper:
            back_stopper.stop()
            back_stopper = None
        __log.info('Stopped distance sensor driver...')
