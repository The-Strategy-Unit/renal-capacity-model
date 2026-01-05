import logging
from pathlib import Path

time_to_event_filenames = [
    "ttgf_cadTx",
    "ttgf_cadTx_initialisation",
    "ttgf_liveTx",
    "ttgf_liveTx_initialisation",
    "ttma_hhd",
    "ttma_hhd_initialisation",
    "ttma_ichd",
    "ttma_ichd_initialisation",
    "ttma_pd",
    "ttma_pd_initialisation",
    "tw_cadTx_England",
    "tw_liveTx_England",
    "ttd_inc_listed",
    "ttd_inc_not_listed",
    "ttd_inc_received_Tx",
    "ttd_prev_listed",
    "ttd_prev_not_listed",
    "ttd_prev_received_Tx",
]


def get_logger(module=None, level: int = logging.INFO) -> logging.Logger:
    """Get logger with appropriate name

    Args:
        module (str, optional): Module name. Defaults to None.
        level (int, optional): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger
    """
    logger_name = module
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s.%(funcName)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(logger_name)


def get_time_to_event_curve_filepaths(
    directory: str = "reference/survival_time_to_event_curves",
) -> list[Path]:
    """Check required time to event curve CSVs are in the specified folder, load the paths to a list

    Args:
        directory (str, optional): Folder where time to event curve CSVs are stored. Defaults to "reference/survival_time_to_event_curves".

    Raises:
        FileNotFoundError: Checks if directory exists
        FileNotFoundError: Checks if required files are all in the specified directory

    Returns:
        list[Path]: List of paths to time to event curve CSVs
    """
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")
    exists = all((path / f"{name}.csv").is_file() for name in time_to_event_filenames)
    if exists:
        time_to_event_filepaths = [
            path / f"{name}.csv" for name in time_to_event_filenames
        ]
        return time_to_event_filepaths
    else:
        missing = [
            name
            for name in time_to_event_filenames
            if not (path / f"{name}.csv").is_file()
        ]
        raise FileNotFoundError(f"File(s) missing: {missing}")
