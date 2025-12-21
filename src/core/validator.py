from .intent import Intent
from .errors import ValidationError, ConfirmationRequired
from platform.state import PlatformState

ALLOWED_ACTIONS = {
    "dataset.load",
    "model.train",
    "model.evaluate",
}

def validate(intent: Intent, state: PlatformState) -> None:
    # 1. Action exists
    if intent.action not in ALLOWED_ACTIONS:
        raise ValidationError(f"Unknown action: {intent.action}")

    # 2. Param validation
    if intent.action == "dataset.load":
        if "name" not in intent.params:
            raise ValidationError("Missing param: name")

    if intent.action == "model.train":
        if not state.dataset_loaded:
            raise ValidationError("Cannot train: no dataset loaded")
        if "model_type" not in intent.params:
            raise ValidationError("Missing param: model_type")

    if intent.action == "model.evaluate":
        if not state.model_trained:
            raise ValidationError("Cannot evaluate: model not trained")

    # 3. Confirmation policy (example)
    if intent.action == "dataset.load" and intent.source == "ai":
        raise ConfirmationRequired("Dataset load requires confirmation")
