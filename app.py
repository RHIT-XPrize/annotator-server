from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.options import define, options
from tornado.web import Application

from speech_to_text.dummy_text_annotator import DummyTextAnnotator
from speech_to_text.speech_to_text_annotator import SpeechToTextAnnotator
from speech_to_text.microphone_access import PyaudioMicrophone
from speech_to_text.speech_recognizer_software import GoogleCloudSpeechConverter
from text_processing.color_annotator import TextProcessingAnnotator
from confidence_aggregation.aggregate_confidence_annotator import AggregateConfidenceAnnotator

define('port', default=3000, help='port to listen on')

def main():
    """Construct and serve the tornado application."""
    audio_source = PyaudioMicrophone()
    speech_converter = GoogleCloudSpeechConverter()

    app = Application(handlers= [
        ('/Speech', SpeechToTextAnnotator,
            {"audio_source": audio_source,
             "speech_processor": speech_converter}),
        ('/TextWithoutSpeech', DummyTextAnnotator),
        ('/TextProcessing', TextProcessingAnnotator),
        ('/AggregateConfidence', AggregateConfidenceAnnotator)
    ])
    http_server = HTTPServer(app)
    http_server.listen(options.port)
    IOLoop.current().start()

if __name__ == '__main__':
    main()
