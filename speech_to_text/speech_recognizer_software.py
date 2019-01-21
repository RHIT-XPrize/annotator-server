#!/usr/bin/env python3
import speech_recognition as sr

class SpeechConverter():
    def process_sr_audio(self, audio_snippet):
        raise NotImplemented('SpeechConverters must implement `process_sr_audio` method')

class GoogleCloudSpeechConverter(SpeechConverter):
    SECRETS_PATH = "../auth_secrets/rhit-human-robot-collab-8e5fac3432af.json"

    def __init__(self):
        self.speech_recognizer = sr.Recognizer()

    def process_sr_audio(self, audio_snippet):
        credentials = open(secrets_path).read()
        processed_text = self.speech_recognizer.recognize_google_cloud(audio_snippet, credentials_json=credentials)

        # Log errors to console if they occur
        try:
            print("Google Cloud Speech thinks you said " + processed_text)
            return processed_text
        except sr.UnknownValueError:
            print("Google Cloud Speech could not understand audio")
            raise sr.UnknownValueError
        except sr.RequestError as e:
            print("Could not request results from Google Cloud Speech service; {0}".format(e))
            raise sr.RequestError
        

