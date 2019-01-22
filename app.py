from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application
from speech_to_text.speech_to_text_annotator import SpeechToTextAnnotator
from speech_to_text.microphone_access import PyaudioMicrophone
from speech_to_text.speech_recognizer_software import GoogleCloudSpeechConverter

define('port', default=3000, help='port to listen on')

def main():
    """Construct and serve the tornado application."""
    audio_source = PyaudioMicrophone()
    speech_converter = GoogleCloudSpeechConverter()

    app = Application(handlers= [
        ('/', SpeechToTextAnnotator, 
            {"audio_source": audio_source, 
             "speech_processor": speech_converter})
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
