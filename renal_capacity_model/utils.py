import logging
from pathlib import Path

time_to_event_filenames = [
    "ttd_cadTx",
    "ttd_cadTx_initialisation",
    "ttd_hhd",
    "ttd_hhd_initialisation",
    "ttd_ichd",
    "ttd_ichd_initialisation",
    "ttd_initialisation",
    "ttd_liveTx",
    "ttd_liveTx_initialisation",
    "ttd_pd",
    "ttd_pd_initialisation",
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
]


def get_logger(module=None, level: int = logging.INFO):
    """Get logger with appropriate name."""
    logger_name = module
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s.%(funcName)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
        ],
    )
    return logging.getLogger(logger_name)


def get_time_to_event_curve_filepaths(
    directory="reference/survival_time_to_event_curves",
):
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
