import pir2.common as common
import pir2.common.IPCPipe as pipe
import pir2.display as display
import pir2.common.Logger as Logger
import json

class DisplayMessage:
    X = 0
    Y = 0
    XL = 124
    YL = 32
    message = ''

    def __init__(self, x=0, y=0, xl=124, yl=32):
        self.X = x
        self.Y = y
        self.XL = xl
        self.YL = yl


CONST_CONFIG_PIPE_NAME = 'display.oled.pipe.name'
CONST_CONFIG_SCRN_X = 'display.oled.screen.X'
CONST_CONFIG_SCRN_Y = 'display.oled.screen.Y'
CONST_CONFIG_SCRN_SX = 'display.oled.screen.size.X'
CONST_CONFIG_SCRN_SY = 'display.oled.screen.size.Y'


class OLEDDisplayDriver:
    pipe = None
    X = 0
    Y = 0
    XL = 124
    YL = 32
    __log = Logger.Logger()

    def __init__(self):
        config = common.get_config(display.CONST_CONFIG_SECTION_NAME_DISPLAY)
        if config:
            self.__log.info('Found RPi Display configuration...')
            v = config.config.get_option(display.CONST_CONFIG_SECTION_NAME_DISPLAY, CONST_CONFIG_PIPE_NAME)
            if not v:
                raise Exception('OLED Display: Pipe name not set...')
            p_name = v
            v = config.config.get_option(display.CONST_CONFIG_SECTION_NAME_DISPLAY, CONST_CONFIG_SCRN_X)
            if v:
                self.X = int(v)
            v = config.config.get_option(display.CONST_CONFIG_SECTION_NAME_DISPLAY, CONST_CONFIG_SCRN_Y)
            if v:
                self.Y = int(v)
            v = config.config.get_option(display.CONST_CONFIG_SECTION_NAME_DISPLAY, CONST_CONFIG_SCRN_SX)
            if v:
                self.XL = int(v)
            v = config.config.get_option(display.CONST_CONFIG_SECTION_NAME_DISPLAY, CONST_CONFIG_SCRN_SY)
            if v:
                self.YL = int(v)

            self.pipe = pipe.Pipe(p_name, mode=pipe.PipeMode.WRITER)
        else:
            raise Exception('OLED Display: Configuration section not found...')

    def write(self, message: str):
        mesg = DisplayMessage(x=self.X, y = self.Y, xl = self.XL, yl = self.XL)
        mesg.message = message

        js = json.dumps(mesg)
        s = self.pipe.write(js)
        self.__log.debug('Sent display message : [' + js + "][size = " + str(s) + ']')

    def dispose(self):
        if self.pipe:
            self.pipe.dispose()
