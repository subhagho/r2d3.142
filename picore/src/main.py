# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from src import picore
import os

__log = Logger.Logger()


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    __log.info(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    wd = os.getcwd()
    print('Working Directory = [' + wd + ']')

    picore.init()
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/