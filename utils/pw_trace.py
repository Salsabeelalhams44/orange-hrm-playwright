import functools
import inspect
import logging

logger = logging.getLogger(__name__)


def pw_trace(func):
    """Decorator that wraps a page object method with Playwright tracing groups.

    Usage:
        @pw_trace
        def my_method(self, ...):
            ...
    """

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        # Build a readable group name from class and method name
        class_name = self.__class__.__name__
        method_name = func.__name__
        group_name = f"{class_name}.{method_name}"

        logger.info("Tracing group start: %s", group_name)
        self.page.context.tracing.group(group_name)

        try:
            result = func(self, *args, **kwargs)
            return result
        finally:
            self.page.context.tracing.group_end()
            logger.info("Tracing group end: %s", group_name)

    return wrapper


def pw_trace_all(cls):
    """Class decorator that automatically applies pw_trace to all public methods.

    Usage:
        @pw_trace_all
        class AddEmployeePage:
            ...
    """
    for name, method in inspect.getmembers(cls, predicate=inspect.isfunction):
        # Skip private/dunder methods like __init__
        if not name.startswith("_"):
            setattr(cls, name, pw_trace(method))
    return cls
