import pandas as pd
from apps.excel_manager.services.file_handler import (
    get_excel_files, output_excel_file
)
from django.core.exceptions import ValidationError
from pandas.io.excel._base import ExcelFile
from typing import List, Dict
import os

def generate_summary(*, excel_file: ExcelFile, targeted_values=List) -> pd.DataFrame:
    excel = pd.ExcelFile(excel_file)
    container = []
    for sheet_name in excel.sheet_names:
        sheet_data = pd.read_excel(excel, sheet_name=sheet_name, header=None)

        # reshape a bit
        sheet_data = sheet_data[[1, 2]]
        sheet_data.set_index(1, inplace=True)
        sheet_data.index.names = ['labels']
        sheet_data.columns = ['values']

        # filter data
        try:
            filtered_data = sheet_data.loc[targeted_values].reset_index()
        except KeyError as e:
            raise ValidationError(e)
        else:
            # change index for alignment later
            filtered_data.index = [0] * len(filtered_data)

            # pivot for usage of concat function where target_values = columns
            pivot_data = filtered_data.pivot(columns=['labels'], values=['values'])

            container.append(pivot_data)

    summary = pd.concat(container, ignore_index=True)
    summary.columns = summary.columns.get_level_values(1)

    return summary[targeted_values]


def export_excel_summary(*, input_path: str, output_path: str, targeted_values: List) -> Dict:
    """

    """
    if not os.path.isdir(input_path):
        raise ValidationError('Input path is not a valid directory please check')

    if not os.path.isdir(output_path):
        raise ValidationError('Output path is not a valid directory please check')

    input_files = get_excel_files(input_path=input_path)
    files_summarized = 0
    for filename, file_path in input_files:
        summary = generate_summary(excel_file=file_path, targeted_values=targeted_values)
        output_excel_file(data=summary, output_path=output_path, input_file_name=filename)
        files_summarized += 1
    return {'files_summarized': files_summarized}
