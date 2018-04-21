"""
Custom PyPlan exceptions.
"""


class PyPlanError(Exception):
    """Parent class for pyplan custom exceptions."""


class PluginError(PyPlanError):
    """Parent class for plugin-related errors."""


class PluginNameClashError(PluginError):
    """To be raised when attempting to register a plugin that shares a name with an already-registered plugin."""


class PluginNotFoundError(PluginError):
    """To be raised when attempting to retrieve a class by name that has not been registered as a plugin."""


class StashError(PyPlanError):
    """Parent class for stash-related errors."""


class StashLoadError(StashError):
    """To be raised when something goes wrong attempting to load data from a stash."""
