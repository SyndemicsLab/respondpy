from __future__ import annotations

__all__: list[str] = ["ExecutionConfig", "LoggingConfig", "RuntimeConfig"]


class ExecutionConfig:
    total_threads: int
    eigen_threads: int
    run_models_concurrently: bool

    def __init__(self) -> None:
        ...


class LoggingConfig:
    logger_name: str
    file_path: str
    use_shared_sink: bool

    def __init__(self) -> None:
        ...


class RuntimeConfig:
    execution: ExecutionConfig
    logging: LoggingConfig

    def __init__(self) -> None:
        ...