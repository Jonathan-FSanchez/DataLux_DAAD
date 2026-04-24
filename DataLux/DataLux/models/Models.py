from __future__ import annotations

from typing import Dict, List, Tuple
import pandas as pd

from processing.Processing import ProcessedDataset


class Model:
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        is_trained: bool = False
    ) -> None:
        self.name: str = name
        self.model_type: str = model_type
        self.parameters: Dict = parameters
        self.is_trained: bool = is_trained

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def get_params(self) -> Dict:
        pass

    def score(self, X: pd.DataFrame, y: pd.Series) -> float:
        pass


class LinearRegressionModel(Model):
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        coefficients: List[float],
        intercept: float,
        is_trained: bool = False
    ) -> None:
        super().__init__(name, model_type, parameters, is_trained)
        self.coefficients: List[float] = coefficients
        self.intercept: float = intercept

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def get_params(self) -> Dict:
        pass


class LogisticRegressionModel(Model):
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        classes: List[str],
        coefficients: List[float],
        intercept: float,
        is_trained: bool = False
    ) -> None:
        super().__init__(name, model_type, parameters, is_trained)
        self.classes: List[str] = classes
        self.coefficients: List[float] = coefficients
        self.intercept: float = intercept

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_params(self) -> Dict:
        pass


class DecisionTreeModel(Model):
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        max_depth: int,
        criterion: str,
        tree_structure: object,
        is_trained: bool = False
    ) -> None:
        super().__init__(name, model_type, parameters, is_trained)
        self.max_depth: int = max_depth
        self.criterion: str = criterion
        self.tree_structure: object = tree_structure

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def get_feature_importance(self) -> Dict:
        pass

    def get_params(self) -> Dict:
        pass


class RandomForestModel(Model):
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        n_estimators: int,
        max_depth: int,
        criterion: str,
        forest_structure: object,
        is_trained: bool = False
    ) -> None:
        super().__init__(name, model_type, parameters, is_trained)
        self.n_estimators: int = n_estimators
        self.max_depth: int = max_depth
        self.criterion: str = criterion
        self.forest_structure: object = forest_structure

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def get_feature_importance(self) -> Dict:
        pass

    def get_params(self) -> Dict:
        pass


class KNNModel(Model):
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        k: int,
        distance_metric: str,
        training_data: pd.DataFrame,
        is_trained: bool = False
    ) -> None:
        super().__init__(name, model_type, parameters, is_trained)
        self.k: int = k
        self.distance_metric: str = distance_metric
        self.training_data: pd.DataFrame = training_data

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def get_neighbors(self, X: pd.DataFrame) -> List:
        pass

    def get_params(self) -> Dict:
        pass


class SVMModel(Model):
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        kernel: str,
        c_value: float,
        support_vectors: object,
        is_trained: bool = False
    ) -> None:
        super().__init__(name, model_type, parameters, is_trained)
        self.kernel: str = kernel
        self.c_value: float = c_value
        self.support_vectors: object = support_vectors

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def decision_function(self, X: pd.DataFrame) -> pd.Series:
        pass

    def get_params(self) -> Dict:
        pass


class NaiveBayesModel(Model):
    def __init__(
        self,
        name: str,
        model_type: str,
        parameters: Dict,
        class_probabilities: Dict,
        feature_probabilities: Dict,
        is_trained: bool = False
    ) -> None:
        super().__init__(name, model_type, parameters, is_trained)
        self.class_probabilities: Dict = class_probabilities
        self.feature_probabilities: Dict = feature_probabilities

    def fit(self, X: pd.DataFrame, y: pd.Series) -> None:
        pass

    def predict(self, X: pd.DataFrame) -> pd.Series:
        pass

    def predict_proba(self, X: pd.DataFrame) -> pd.DataFrame:
        pass

    def get_params(self) -> Dict:
        pass


class ModelConfig:
    def __init__(
        self,
        model_type: str,
        target_column: str,
        feature_columns: List[str],
        parameters: Dict
    ) -> None:
        self.model_type: str = model_type
        self.target_column: str = target_column
        self.feature_columns: List[str] = feature_columns
        self.parameters: Dict = parameters

    def validate(self) -> bool:
        pass


class PredictionResult:
    def __init__(
        self,
        predictions: pd.Series | List,
        metrics: Dict,
        model_name: str
    ) -> None:
        self.predictions: pd.Series | List = predictions
        self.metrics: Dict = metrics
        self.model_name: str = model_name


class ModelTrainer:
    def __init__(
        self,
        config: ModelConfig,
        trained_model: Model
    ) -> None:
        self.config: ModelConfig = config
        self.trained_model: Model = trained_model

    def train(self, processed_dataset: ProcessedDataset) -> None:
        pass

    def predict(self, new_data: pd.DataFrame) -> pd.Series:
        pass

    def split_data(
        self,
        processed_dataset: ProcessedDataset,
        test_size: float
    ) -> Tuple:
        pass

    def select_model(self, model_name: str) -> Model:
        pass


class ModelEvaluator:
    def __init__(self) -> None:
        pass

    def evaluate_regression(self, y_true: pd.Series, y_pred: pd.Series) -> Dict:
        pass

    def evaluate_classification(self, y_true: pd.Series, y_pred: pd.Series) -> Dict:
        pass