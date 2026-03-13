from __future__ import annotations

from typing import List, Dict, Tuple, Optional
import pandas as pd


class CSVFile:
    def __init__(
        self,
        file_path: str,
        file_name: str,
        delimiter: str,
        encoding: str,
        has_header: bool
    ) -> None:
        self.file_path: str = file_path
        self.file_name: str = file_name
        self.delimiter: str = delimiter
        self.encoding: str = encoding
        self.has_header: bool = has_header

    def exists(self) -> bool:
        pass

    def get_extension(self) -> str:
        pass

    def validate_format(self) -> bool:
        pass


class DataSet:
    def __init__(
        self,
        data: pd.DataFrame,
        row_count: int,
        column_count: int,
        columns: List[str],
        source_file: Optional[CSVFile]
    ) -> None:
        self.data: pd.DataFrame = data
        self.row_count: int = row_count
        self.column_count: int = column_count
        self.columns: List[str] = columns
        self.source_file: Optional[CSVFile] = source_file

    def get_shape(self) -> Tuple[int, int]:
        pass

    def get_columns(self) -> List[str]:
        pass

    def preview(self, n: int) -> pd.DataFrame:
        pass

    def update_data(self, new_data: pd.DataFrame) -> None:
        pass


class ColumnProfile:
    def __init__(
        self,
        name: str,
        data_type: str,
        null_count: int,
        unique_count: int,
        is_numeric: bool,
        is_categorical: bool
    ) -> None:
        self.name: str = name
        self.data_type: str = data_type
        self.null_count: int = null_count
        self.unique_count: int = unique_count
        self.is_numeric: bool = is_numeric
        self.is_categorical: bool = is_categorical

    def calculate_statistics(self, data: pd.Series) -> Dict:
        pass

    def detect_type(self, data: pd.Series) -> str:
        pass


class DatasetProfiler:
    def __init__(
        self,
        dataset: DataSet,
        column_profiles: Optional[List[ColumnProfile]] = None
    ) -> None:
        self.dataset: DataSet = dataset
        self.column_profiles: List[ColumnProfile] = column_profiles if column_profiles is not None else []

    def analyze(self) -> None:
        pass

    def get_summary(self) -> Dict:
        pass

    def get_numeric_columns(self) -> List[str]:
        pass

    def get_categorical_columns(self) -> List[str]:
        pass

    def get_target_candidates(self) -> List[str]:
        pass


class CSVLoader:
    def __init__(self, csv_file: CSVFile) -> None:
        self.csv_file: CSVFile = csv_file

    def load(self) -> DataSet:
        pass

    def read_sample(self, n: int) -> pd.DataFrame:
        pass