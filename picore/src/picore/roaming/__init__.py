import src.picore.roaming.stopper as stopper
import src.picore.roaming.move as move
import time
import threading

CONST_CONFIG_NAME_ROAMING = 'ROAMING'
CONST_FRONT_TRIG = 25
CONST_FRONT_ECHO = 20
CONST_BACK_TRIG = 8
CONST_BACK_ECHO = 21

__log = Logger.Logger()
mover = move.RPiMovement()


def stop_callback(name, distance):
    global mover
    mover.stop()
    __log.info('Stop called by [' + name + '][distance=' + str(distance) + ']...')


front_stopper = stopper.Stopper('front', CONST_FRONT_TRIG, CONST_FRONT_ECHO, stop_callback)
back_stopper = stopper.Stopper('back', CONST_BACK_TRIG, CONST_BACK_ECHO, stop_callback)
f_thread = None
b_thread = None


def stopper_thread_init(__stopper):
    __stopper.init()
    time.sleep(2)
    __stopper.start()


def init():
    global f_thread, b_thread, front_stopper, back_stopper, mover

    __log.info('Initializing Roaming...')
    mover.init()

    f_thread = threading.Thread(target=stopper_thread_init, args=(front_stopper,))
    b_thread = threading.Thread(target=stopper_thread_init, args=(back_stopper,))

    f_thread.start()
    b_thread.start()
