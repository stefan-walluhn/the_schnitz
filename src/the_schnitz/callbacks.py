from playsound3 import playsound


class AudioCallback:
    def __init__(self, audio_file):
        self.audio_file = audio_file

    def play(self):
        playsound(self.audio_file, block=False)

    def __call__(self, event):
        if event.get('type') == 'LocationFoundEvent':
            self.play()
