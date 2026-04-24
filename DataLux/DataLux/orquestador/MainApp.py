from __future__ import annotations

from typing import Optional

from data.Dataset import CSVFile, DataSet, DatasetProfiler, CSVLoader
from processing.Processing import (
    MissingValueHandler,
    DataCleaner,
    DataTransformer,
    FeatureSelector,
    ProcessedDataset
)
from models.Models import (
    ModelTrainer,
    ModelEvaluator,
    ModelConfig,
    PredictionResult
)
from gui.Visualization import (
    MainWindow,
    FileSelectorPanel,
    DatasetView,
    ProcessingConfigPanel,
    ModelSelectionPanel,
    MetricsView,
    ChartView,
    PredictionResultView,
    ExportPanel
)


class AnalysisApp:
    def __init__(self) -> None:
        self.loader: Optional[CSVLoader] = None
        self.profiler: Optional[DatasetProfiler] = None
        self.missing_handler: Optional[MissingValueHandler] = None
        self.cleaner: Optional[DataCleaner] = None
        self.transformer: Optional[DataTransformer] = None
        self.selector: Optional[FeatureSelector] = None
        self.trainer: Optional[ModelTrainer] = None
        self.evaluator: Optional[ModelEvaluator] = None

        self.main_window: Optional[MainWindow] = None
        self.file_selector: Optional[FileSelectorPanel] = None
        self.dataset_view: Optional[DatasetView] = None
        self.processing_config: Optional[ProcessingConfigPanel] = None
        self.model_selector: Optional[ModelSelectionPanel] = None
        self.metrics_view: Optional[MetricsView] = None
        self.chart_view: Optional[ChartView] = None
        self.result_view: Optional[PredictionResultView] = None
        self.export_panel: Optional[ExportPanel] = None

        self.current_csv_file: Optional[CSVFile] = None
        self.current_dataset: Optional[DataSet] = None
        self.current_processed_dataset: Optional[ProcessedDataset] = None
        self.current_model_config: Optional[ModelConfig] = None
        self.current_prediction_result: Optional[PredictionResult] = None

    def initialize_components(self) -> None:
        pass

    def initialize_gui(self) -> None:
        pass

    def load_dataset(self) -> Optional[DataSet]:
        pass

    def profile_dataset(self, dataset: DataSet) -> None:
        pass

    def process_dataset(self, dataset: DataSet) -> Optional[ProcessedDataset]:
        pass

    def create_model_config(self) -> Optional[ModelConfig]:
        pass

    def train_model(self, processed_dataset: ProcessedDataset) -> Optional[PredictionResult]:
        pass

    def evaluate_model(self, y_true, y_pred) -> dict:
        pass

    def generate_visualizations(self, dataset: DataSet, processed_dataset: ProcessedDataset) -> None:
        pass

    def update_gui_results(self) -> None:
        pass

    def export_results(self) -> None:
        pass

    def run(self) -> None:
        pass