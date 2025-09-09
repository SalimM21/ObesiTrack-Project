import hashlib, json, joblib
import numpy as np
import pandas as pd
from typing import Dict, Any
from shap import TreeExplainer, KernelExplainer, Explainer
from functools import lru_cache

class ShapExplainerWrapper:
    def __init__(self, model, preprocessor, background_df=None):
        self.model = model
        self.preprocessor = preprocessor
        self.background = background_df
        self._explainer = None
        # create explainer depending on model
        try:
            self._explainer = TreeExplainer(self.model)
        except Exception:
            # fallback
            self._explainer = None

    def explain(self, X_df: pd.DataFrame) -> Dict[str, Any]:
        X_proc = self.preprocessor.transform(X_df)
        if self._explainer is not None:
            shap_values = self._explainer.shap_values(X_proc)
            # for multiclass, shap_values is list of arrays per class
            return {"shap_values": [sv.tolist() for sv in shap_values], "base_values": self._explainer.expected_value}
        else:
            # fallback: use KernelExplainer—expensive: only permit small backgrounds
            if self.background is None:
                raise RuntimeError("No background data for KernelExplainer")
            ke = KernelExplainer(self.model.predict_proba, self.preprocessor.transform(self.background))
            sv = ke.shap_values(X_proc)
            return {"shap_values": [s.tolist() for s in sv]}

# Simple in-memory cache decorator (limited)
@lru_cache(maxsize=256)
def _hash_payload(payload_json: str) -> str:
    return hashlib.sha256(payload_json.encode()).hexdigest()
