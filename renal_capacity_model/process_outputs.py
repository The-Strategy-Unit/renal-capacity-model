# Module for processing results into output suitable for users

import pandas as pd
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
from datetime import datetime
from renal_capacity_model.helpers import get_logger

logging = get_logger(__name__)


def combine_incident_and_prevalent_counts(df: pd.DataFrame) -> pd.DataFrame:
    processed_dfs = []
    for metric in ["prevalence", "mortality", "incidence"]:
        df_filtered = df[df.index.str.contains(metric, case=False, na=False)].copy()
        df_filtered.loc[:, "index"] = df_filtered.index.str.replace(
            r"_?(incident|prevalent)", "", regex=True
        )
        processed_dfs.append(df_filtered.groupby("index").sum())
    return pd.concat(processed_dfs).fillna(0)


def produce_combined_results_for_all_model_runs(results_dfs: list[pd.DataFrame]):
    dfs_processed = [combine_incident_and_prevalent_counts(df) for df in results_dfs]
    combined = pd.concat(
        [df.reset_index().assign(model_run=i + 1) for i, df in enumerate(dfs_processed)]
    )
    return (
        combined.set_index(["index", "model_run"])
        .sort_index(axis=0)
        .sort_index(axis=1)
        .fillna(0)
    )


def write_results_to_excel(path_to_excel_file: str, combined_df: pd.DataFrame):
    today_date = datetime.now().strftime("%Y%m%d-%H%M")
    wb = load_workbook(path_to_excel_file)
    for outcome in combined_df.index.get_level_values(0).drop_duplicates():
        ws = wb.create_sheet(title=outcome)
        for r in dataframe_to_rows(
            combined_df.loc[outcome].reset_index(), index=False, header=True
        ):
            ws.append(r)
    results_filepath = path_to_excel_file.replace(
        ".xlsx", f"_results_{today_date}.xlsx"
    )
    wb.save(results_filepath)
    logging.info(f"Excel format model results written to: ✍️ {results_filepath}")
