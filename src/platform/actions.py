from .state import PlatformState


def load_dataset(state: PlatformState, name: str):
    state.dataset_loaded = True
    state.dataset_name = name
    print(f"[PLATFORM] Dataset '{name}' loaded")


def train_model(state: PlatformState, model_type: str):
    state.model_trained = True
    state.model_type = model_type
    print(f"[PLATFORM] Model '{model_type}' trained")


def evaluate_model(state: PlatformState):
    if not state.model_trained:
        raise RuntimeError("Model not trained")
    print("[PLATFORM] Model evaluated (accuracy=0.91)")
