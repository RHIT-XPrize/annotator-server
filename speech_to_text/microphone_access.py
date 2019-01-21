#!/usr/bin/env python3
import speech_recognition as sr

class MicrophoneProxy():
    def listen_for_snippet(self):
        raise NotImplemented('MicrophoneProxy must implement `listen_for_snippet` method')

class PyaudioMicrophone(MicrophoneProxy):
    PAUSE_THRESHOLD_SEC = 1
    MAX_ADJUST_SEC = 1

    def __init__(self):
        self.source = sr.Microphone()
        self.speech_recognizer = sr.Recognizer

    def listen_for_snippet(self):
        print("Say something!")
        self.speech_recognizer.pause_threshold = PAUSE_THRESHOLD_SEC
        self.speech_recognizer.adjust_for_ambient_noise(self.source, duration=MAX_ADJUST_SEC) 
        audio = self.speech_recognizer.listen(self.source)
        return audio