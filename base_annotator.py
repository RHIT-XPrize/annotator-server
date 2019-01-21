import json
from tornado.web import RequestHandler

# Template for annotator provided by rhit-xprize team
class Annotator(RequestHandler):
    SUPPORTED_METHODS = ("POST",)

    def __init__(self):
        self.annotation_types = []
        self._annotations = []

    def post(self):
        cas = json.loads(self.request.body)
        self.process(cas)
        resp = json.dumps(self._annotation_to_dict(self._annotations))
        self.send_response(resp)

    def process(self, cas):
        raise NotImplemented('Annotators must implement `process` method')

    def _annotation_to_dict(self, annotations):
        annot_map = {c : [] for c in self.annotation_types}
        for x in annotations:
            class_name = x.name()
            annot_map[class_name].append(dict(x))
        return annot_map

    def set_default_headers(self):
        """Set the default response header to be JSON."""
        self.set_header("Content-Type", 'application/json; charset="utf-8"')

    def send_response(self, data, status=200):
        """Construct and send a JSON response with appropriate status code."""
        self.set_status(status)
        self.write(json.dumps(data))

    def add_annotation(self, annotation):
        self._annotations.append(annotation)

class AnnotationType:
    def __init__(self):
        self.name = "NO NAME PROVIDED"

    def name(self):
        return self.name