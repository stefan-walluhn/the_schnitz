from msgpack import unpackb
from playsound3 import playsound


class MessagePackCallback:
    def __init__(self, callback):
        self.callback = callback

    def __call__(self, msg):
        self.callback(unpackb(msg))


class AudioCallback:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def play(self):
        playsound(self.audio_file, block=False)

    def __call__(self, _):
        self.play()
