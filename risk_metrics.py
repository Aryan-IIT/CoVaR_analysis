import numpy as np
import pandas as pd
from scipy.stats import norm


def _clean_returns(returns):
    """Convert input to a clean 1D numpy array of returns."""
    if isinstance(returns, pd.Series):
        values = returns.to_numpy()
    else:
        values = np.asarray(returns)

    if values.ndim != 1:
        raise ValueError("returns must be a one-dimensional Series or array.")

    # Keep the metric functions focused on already-prepared return data.
    values = values.astype(float)
    values = values[~np.isnan(values)]

    if values.size < 2:
        raise ValueError("At least two non-NaN return observations are required.")

    return values


def _check_alpha(alpha):
    alpha = float(alpha)
    if not 0 < alpha < 1:
        raise ValueError("alpha must be between 0 and 1.")
    return alpha


def historical_var(returns, alpha=0.05):
    """Historical VaR as a positive loss number."""
    alpha = _check_alpha(alpha)
    values = _clean_returns(returns)
    cutoff = np.quantile(values, alpha)
    return float(-cutoff)


def historical_cvar(returns, alpha=0.05):
    """Historical CVaR as the average loss beyond historical VaR."""
    alpha = _check_alpha(alpha)
    values = _clean_returns(returns)
    cutoff = np.quantile(values, alpha)
    tail_returns = values[values <= cutoff]

    if tail_returns.size == 0:
        raise ValueError("No tail observations found for the given alpha.")

    return float(-tail_returns.mean())


def parametric_var(returns, alpha=0.05):
    """Gaussian VaR using sample mean and sample standard deviation."""
    alpha = _check_alpha(alpha)
    values = _clean_returns(returns)
    mean_return = values.mean()
    std_return = values.std(ddof=1)

    if std_return == 0:
        raise ValueError("Sample standard deviation is zero; parametric VaR is not meaningful.")

    z_alpha = norm.ppf(alpha)
    var_return = mean_return + std_return * z_alpha
    return float(-var_return)


def parametric_cvar(returns, alpha=0.05):
    """Gaussian CVaR using the analytical expected shortfall formula."""
    alpha = _check_alpha(alpha)
    values = _clean_returns(returns)
    mean_return = values.mean()
    std_return = values.std(ddof=1)

    if std_return == 0:
        raise ValueError("Sample standard deviation is zero; parametric CVaR is not meaningful.")

    z_alpha = norm.ppf(alpha)
    cvar_return = mean_return - std_return * norm.pdf(z_alpha) / alpha
    return float(-cvar_return)
