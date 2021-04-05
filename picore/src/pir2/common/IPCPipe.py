import struct
import os
import select
from enum import Enum


def encode_msg_size(size: int) -> bytes:
    return struct.pack("<I", size)


def decode_msg_size(size_bytes: bytes) -> int:
    return struct.unpack("<I", size_bytes)[0]


class PipeMode(Enum):
    READER = 1
    WRITER = 2


class BasicMessage:
    data = None
    length = 0

    def set(self, mesg: str):
        if not mesg or len(mesg) <= 0:
            raise Exception('NULL/Empty string passed...')
        self.data = bytes(mesg, 'utf-8')
        self.length = len(self.data)

    def set_data(self, content: bytes, size: int):
        self.data = content
        self.length = size

    def get(self):
        if self.data:
            return str(self.data, 'utf-8')
        return None

    def create_mesg(self) -> bytes:
        if not self.data or self.length <= 0:
            raise Exception('Message data is NULL/Empty')
        return encode_msg_size(self.length) + self.data

    def to_string(self) -> str:
        if self.data and self.length > 0:
            return str(self.data, 'utf-8')
        return ''


class Pipe:
    name = ''
    fifo = None
    poll = None
    mode = PipeMode.READER

    def __init__(self, name: str, mode=PipeMode.READER, create=False):
        if not name or len(name) <= 0:
            raise Exception('Invalid Pipe name...')
        self.name = name
        self.mode = mode
        if create:
            os.mkfifo(name)
        flags = os.O_WRONLY
        if self.mode == PipeMode.READER:
            flags = os.O_RDONLY | os.O_NONBLOCK
        self.fifo = os.open(name, flags)
        if mode == PipeMode.READER:
            self.poll = select.poll()
            self.poll.register(self.fifo, select.POLLIN)

    def write(self, message: str) -> int:
        if not self.mode == PipeMode.WRITER:
            raise Exception('Pipe not initialized for write...')
        mesg = BasicMessage()
        mesg.set(message)
        data = mesg.create_mesg()
        if data:
            os.write(self.fifo, data)
            return mesg.length
        return -1

    def get_message(self) -> BasicMessage:
        """Get a message from the named pipe."""
        msg_size_bytes = os.read(self.fifo, 4)
        msg_size = decode_msg_size(msg_size_bytes)
        msg_content = os.read(self.fifo, msg_size)

        mesg = BasicMessage()
        mesg.set_data(msg_content, msg_size)

        return mesg

    def read(self, timeout=2000) -> str:
        if not self.mode == PipeMode.READER:
            raise Exception('Pipe not initialized for read...')
        if (self.fifo, select.POLLIN) in self.poll.poll(timeout):
            mesg = self.get_message()
            if mesg and mesg.length > 0:
                return mesg.to_string()
        return ''

    def dispose(self, delete=False):
        if self.mode == PipeMode.READER:
            if self.poll:
                self.poll.unregister(self.fifo)
        if self.fifo:
            os.close(self.fifo)
        if delete:
            os.remove(self.name)