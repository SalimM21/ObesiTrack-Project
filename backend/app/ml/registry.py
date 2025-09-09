from pathlib import Path
import joblib
from sklearn.base import BaseEstimator
from config import settings

class ModelBundle:
    def __init__(self, preprocessor: BaseEstimator, classifier: BaseEstimator):
        self.preprocessor = preprocessor
        self.classifier = classifier

    def predict_proba(self, X_df):
        X_proc = self.preprocessor.transform(X_df)
        return self.classifier.predict_proba(X_proc)

    def predict(self, X_df):
        X_proc = self.preprocessor.transform(X_df)
        return self.classifier.predict(X_proc)

class ModelRegistry:
    def __init__(self, model_dir: str | Path | None = None):
        self.model_dir = Path(model_dir or settings.MODEL_DIR)
        self.preprocessor_path = self.model_dir / "preprocessor.joblib"
        self.classifier_path = self.model_dir / "classifier.joblib"
        self._bundle: ModelBundle | None = None

    def load(self) -> ModelBundle:
        if self._bundle is None:
            pre = joblib.load(self.preprocessor_path)
            clf = joblib.load(self.classifier_path)
            self._bundle = ModelBundle(pre, clf)
        return self._bundle

registry = ModelRegistry()
