try:
    import structlog
except ModuleNotFoundError:  # pragma: no cover - depends on local env
    structlog = None


class _FallbackLogger:
    def _emit(self, level, event, **kwargs):
        import logging
        message = str(event)
        if kwargs:
            extras = " ".join(f"{k}={v}" for k, v in kwargs.items())
            message = f"{message} {extras}"
        logging.getLogger("agentcoach").log(level, message)

    def info(self, event, **kwargs):
        import logging
        self._emit(logging.INFO, event, **kwargs)

    def warning(self, event, **kwargs):
        import logging
        self._emit(logging.WARNING, event, **kwargs)

    def error(self, event, **kwargs):
        import logging
        self._emit(logging.ERROR, event, **kwargs)


def get_logger():
    if structlog is None:
        return _FallbackLogger()
    return structlog.get_logger()


def setup_logging(level="INFO"):
    import logging
    if structlog is None:
        logging.basicConfig(level=getattr(logging, level.upper(), logging.INFO))
        return
    structlog.configure(
        processors=[
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, level.upper(), logging.INFO)
        ),
    )
