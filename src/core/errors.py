# TODO: IMPLEMENT LATER

class IntentError(Exception):
    pass

class ValidationError(IntentError):
    pass

class ConfirmationRequired(IntentError):
    pass
