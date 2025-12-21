from core.intent import Intent
from platform.state import PlatformState
from platform import actions

def route(intent: Intent, state: PlatformState):
    if intent.action == "dataset.load":
        actions.load_dataset(state, intent.params["name"])

    elif intent.action == "model.train":
        actions.train_model(state, intent.params["model_type"])

    elif intent.action == "model.evaluate":
        actions.evaluate_model(state)

    else:
        # This should never happen if validator is correct
        raise RuntimeError(f"Unhandled action: {intent.action}")
