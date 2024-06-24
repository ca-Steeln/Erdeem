
import importlib

from django.db.models import Model
from django.apps import apps


def get_model(model_identifier):
    """
    Retrieve a Django model class based on the model identifier.

    Args:
        model_identifier (str or type): The model identifier, which can be:
            - A string in the format 'app_label.ModelName'
            - A string with the full import path 'myapp.models.MyModel'
            - The model class itself

    Returns:
        Model: The Django model class.

    Raises:
        ValueError: If the model cannot be found or the identifier is invalid.
    """
    if isinstance(model_identifier, str):
        # Check if the string is in the format 'app_label.ModelName'
        if '.' in model_identifier and model_identifier.count('.') == 1:
            app_label, model_name = model_identifier.split('.')
            try:
                model = apps.get_model(app_label, model_name)
                if model is None:
                    raise ValueError(f"Model '{model_identifier}' not found.")
                return model
            except LookupError:
                raise ValueError(f"Model '{model_identifier}' not found in app '{app_label}'.")

        # Check if the string is a full import path
        try:
            module_path, class_name = model_identifier.rsplit('.', 1)
            module = importlib.import_module(module_path)
            model = getattr(module, class_name)
            if not issubclass(model, Model):
                raise ValueError(f"'{model_identifier}' is not a valid Django model.")
            return model
        except (ImportError, AttributeError, ValueError):
            raise ValueError(f"Model '{model_identifier}' not found or invalid path.")

    # If the identifier is already a model class
    elif issubclass(model_identifier, Model):
        return model_identifier

    else:
        raise ValueError("Model identifier must be a string or a Django model class.")

