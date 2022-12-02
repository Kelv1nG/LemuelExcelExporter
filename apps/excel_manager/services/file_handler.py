import os
from typing import List, Tuple
from pathlib import Path
from pandas import DataFrame

def get_excel_files(*, input_path: Path) -> List[Tuple]:
    """
    Outputs list of paths of the excel files
    [('filename', 'file_path')]
    """
    path_list = []
    for file in os.listdir(input_path):
        if file.endswith('.xlsx') or file.endswith('.xlsm') or file.endswith('.xls'):
            file_name = file.split('.')[0]
            file_path = os.path.join(input_path, file)
            path_list.append((file_name, file_path))
    return path_list


def output_excel_file(*, data: DataFrame, output_path: Path, input_file_name: str) -> None:
    """
    outputs excel files containing the name of each file into
    'file_summary' in the output path

    i.e input: 'file1.xlsx', output: 'file1_summary.xlsx'
    """
    output_file_path = os.path.join(output_path, input_file_name + '_summary.xlsx')
    data.to_excel(output_file_path)
