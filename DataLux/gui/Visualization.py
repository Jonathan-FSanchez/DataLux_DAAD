from __future__ import annotations

from typing import Optional, List
import pandas as pd

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QFileDialog,
    QVBoxLayout,
    QLabel,
    QPushButton
)

from data.Dataset import DataSet
from processing.Processing import ProcessedDataset
from models.Models import PredictionResult


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()

        self.title: str = "DataLux"
        self.width: int = 1200
        self.height: int = 800

        self.current_dataset: Optional[DataSet] = None
        self.current_processed_dataset: Optional[ProcessedDataset] = None
        self.current_prediction_result: Optional[PredictionResult] = None

    def setup_ui(self) -> None:
        pass

    def show_window(self) -> None:
        pass

    def close_window(self) -> None:
        pass


class FileSelectorPanel(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.selected_file_path: str = ""

    def open_file_dialog(self) -> str:
        pass

    def validate_selected_file(self) -> bool:
        pass

    def clear_selection(self) -> None:
        pass


class DatasetView(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.dataset: Optional[DataSet] = None

    def load_dataset(self, dataset: DataSet) -> None:
        pass

    def show_preview(self, n: int) -> pd.DataFrame:
        pass

    def show_columns(self) -> List[str]:
        pass

    def clear_view(self) -> None:
        pass


class MetricsView(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.metrics: dict = {}

    def load_metrics(self, metrics: dict) -> None:
        pass

    def show_metrics(self) -> None:
        pass

    def clear_metrics(self) -> None:
        pass


class ChartView(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.current_data: Optional[pd.DataFrame] = None

    def show_histogram(self, data: pd.DataFrame, column: str) -> None:
        pass

    def show_scatter(self, data: pd.DataFrame, x: str, y: str) -> None:
        pass

    def show_boxplot(self, data: pd.DataFrame, column: str) -> None:
        pass

    def show_correlation_matrix(self, data: pd.DataFrame) -> None:
        pass

    def clear_chart(self) -> None:
        pass


class PredictionResultView(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.result: Optional[PredictionResult] = None

    def load_result(self, result: PredictionResult) -> None:
        pass

    def show_predictions(self) -> None:
        pass

    def show_model_name(self) -> str:
        pass

    def clear_result(self) -> None:
        pass


class ExportPanel(QWidget):

    def __init__(self) -> None:
        super().__init__()

        self.export_path: str = ""

    def export_csv(self, path: str) -> None:
        pass

    def export_pdf(self, path: str) -> None:
        pass

    def set_export_path(self, path: str) -> None:
        pass