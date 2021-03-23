import pickle
import base64


def encode_and_save_session(request, class_object, name):
    serialized = pickle.dumps(class_object)
    encoded = base64.b64encode(serialized).decode("ascii")
    request.session[name] = encoded


def get_session_object(request, name):
    encoded=request.session[name]
    serialized=base64.b64decode(encoded)
    obj = pickle.loads(serialized)
    return obj
