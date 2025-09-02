from evidently.report import Report
from evidently.metric_preset import DataDriftPreset
from evidently import ColumnMapping
import pandas as pd
import json

def build_drift_report(baseline_df: pd.DataFrame, production_df: pd.DataFrame, column_mapping: ColumnMapping | None = None):
    report = Report(metrics=[DataDriftPreset()])
    report.run(reference_data=baseline_df, current_data=production_df, column_mapping=column_mapping)
    return report

# to export to json:
# report_json = report.as_dict()
