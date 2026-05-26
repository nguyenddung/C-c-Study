"""
Preprocessing pipeline for feature vectors.

Applies StandardScaler normalisation to the raw feature matrix so that
all dimensions contribute equally to cosine similarity regardless of
their natural scale (binary flags vs. continuous GPA).
"""

from __future__ import annotations

import numpy as np
from sklearn.preprocessing import StandardScaler


class FeaturePreprocessor:
    """
    Thin wrapper around sklearn's StandardScaler.

    Usage::

        preprocessor = FeaturePreprocessor()
        X_norm = preprocessor.fit_transform(X_raw)    # during index build
        x_norm = preprocessor.transform(x_query)      # at query time
    """

    def __init__(self) -> None:
        self._scaler = StandardScaler(copy=True)
        self._is_fitted = False

    def fit_transform(self, X: np.ndarray) -> np.ndarray:
        """Fit on *X* and return the normalised matrix."""
        X_scaled = self._scaler.fit_transform(X)
        self._is_fitted = True
        return X_scaled.astype(np.float32)

    def transform(self, X: np.ndarray) -> np.ndarray:
        """
        Normalise *X* using already-fitted parameters.

        Raises RuntimeError if called before fit_transform.
        """
        if not self._is_fitted:
            raise RuntimeError("FeaturePreprocessor must be fitted before transform().")
        return self._scaler.transform(X).astype(np.float32)

    @property
    def is_fitted(self) -> bool:
        return self._is_fitted