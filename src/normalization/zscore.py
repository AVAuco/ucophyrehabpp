# This file performs z-score normalization on input data.
import numpy as np

def zscore_normalization(data, params=None):
    """
    Apply z-score normalization to the input data.

    Parameters:
    data (np.ndarray): Input data to be normalized.

    Returns:
    np.ndarray: Z-score normalized data.
    """
    if params is not None:
        mean = params.get("mean")
        std = params.get("std")
    else:
        mean = np.mean(data, axis=0)
        std = np.std(data, axis=0)

    normalized_data = (data - mean) / std

    norm_params = {"mean": mean, "std": std}

    return normalized_data, norm_params