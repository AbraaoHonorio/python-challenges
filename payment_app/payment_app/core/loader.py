"""A simple plugin loader."""
import importlib

PLUGIN_FOLDER = 'plugins'


class ModuleInterface:
    """Represents a plugin interface. A plugin has a single register function."""

    @staticmethod
    def register() -> None:
        """Register the necessary items in the payment factory."""


def import_module(name: str) -> ModuleInterface:
    """Imports a module given a name."""
    return importlib.import_module(name)  # type: ignore


def load_plugins(plugins: list[str]) -> None:
    """Loads the plugins defined in the plugins list."""
    for plugin_file in plugins:
        plugin = import_module(f'{PLUGIN_FOLDER}.{plugin_file}')
        if plugin and hasattr(plugin, "register"):
            plugin.register()
