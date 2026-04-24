from __future__ import annotations

from typing import List, Optional
import pandas as pd

from data.Dataset import DataSet  # ajusta el import según tu estructura


class MissingValueHandler:
    def __init__(self, strategy: str) -> None:
        self.strategy: str = strategy

    def drop_rows(self, dataset: DataSet) -> DataSet:
        pass

    def fill_mean(self, dataset: DataSet, columns: List[str]) -> DataSet:
        pass

    def fill_mode(self, dataset: DataSet, columns: List[str]) -> DataSet:
        pass


class DataCleaner:
    def __init__(self) -> None:
        pass

    def remove_duplicates(self, dataset: DataSet) -> DataSet:
        pass

    def fix_column_names(self, dataset: DataSet) -> DataSet:
        pass

    def convert_types(self, dataset: DataSet) -> DataSet:
        pass


class DataTransformer:
    def __init__(self) -> None:
        pass

    def normalize(self, dataset: DataSet, columns: List[str]) -> DataSet:
        pass

    def standardize(self, dataset: DataSet, columns: List[str]) -> DataSet:
        pass

    def encode_categorical(self, dataset: DataSet, columns: List[str]) -> DataSet:
        pass


class FeatureSelector:
    def __init__(self) -> None:
        self.selected_features: List[str] = []
        self.target_column: Optional[str] = None

    def select_features(self, columns: List[str]) -> List[str]:
        pass

    def select_target(self, column: str) -> str:
        pass


class ProcessedDataset:
    def __init__(
        self,
        features: pd.DataFrame,
        target: Optional[pd.Series]
    ) -> None:
        self.features: pd.DataFrame = features
        self.target: Optional[pd.Series] = target