from core.validator import validate
from core.router import route
from core.errors import ConfirmationRequired
from platform.state import PlatformState
from core.intent import Intent

state = PlatformState()

def execute(intent: Intent):
    try:
        validate(intent, state)
        route(intent, state)
    except ConfirmationRequired as c:
        print(f"[CONFIRMATION] {c}")
    except Exception as e:
        print(f"[ERROR] {e}")
