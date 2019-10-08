"""Embedding of multivariate time-series."""
# License: Apache 2.0

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from ..utils import validate_params
from sklearn.utils.validation import check_is_fitted, check_array, column_or_1d


class PearsonCorrelation(BaseEstimator, TransformerMixin):
    """Transformer performing an argsort of each row in each array in a collection.
    Based on ideas in `arXiv:1904.07403 <https://arxiv.org/abs/1904.07403>`_.

    Parameters
    ----------
    positive_definite : bool, default: True
        Whether the correlation should be output as a positive definite matrix.
    """
    _hyperparameters = {'positive_definite': [bool, (0, 1)]}

    def __init__(self, positive_definite=True):
        self.positive_definite = positive_definite

    def fit(self, X, y=None):
        """Do nothing and return the estimator unchanged.
        This method is just there to implement the usual API and hence
        work in pipelines.

        Parameters
        ----------
        X : ndarray, shape (n_samples, n_points, d)
            Input data.

        y : None
            There is no need of a target in a transformer, yet the pipeline API
            requires this parameter.

        Returns
        -------
        self : object
            Returns self.

        """
        validate_params(self.get_params(), self._hyperparameters)
        check_array(X)

        self._is_fitted = True
        return self

    def transform(self, X, y=None):
        """For each array in X, argsort each row in ascending order.

        Parameters
        ----------
        X : ndarray, shape (n_samples, n_points, d)
            Input data.

        y : None
            There is no need of a target in a transformer, yet the pipeline API
            requires this parameter.

        Returns
        -------
        Xt : ndarray of int, shape (n_samples, n_points, d)
            The transformed array.

        """
        # Check if fit had been called
        check_is_fitted(self, ['_is_fitted'])
        X = check_array(X)

        n_features = X.shape[1]

        Xt = np.corrcoef(X.T)
        if self.positive_definite:
            Xt = np.ones((n_features, n_features)) - np.abs(Xt)

        return Xt