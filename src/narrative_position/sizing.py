from __future__ import annotations
import numpy as np
import pandas as pd

def scenario_statistics(table:pd.DataFrame):
    p=table["probability"].to_numpy(float)
    r=table["return_to_value"].to_numpy(float)
    mean=float(p@r)
    variance=float(p@((r-mean)**2))
    downside=float(p@np.minimum(r,0))
    loss_prob=float(p[r<0].sum())
    return {
        "expected_return":mean,
        "scenario_volatility":float(np.sqrt(variance)),
        "probability_of_loss":loss_prob,
        "expected_downside":downside,
        "worst_case_return":float(r.min()),
        "best_case_return":float(r.max()),
    }

def position_size(
    expected_return,
    scenario_volatility,
    asset_volatility=.25,
    portfolio_volatility=.12,
    correlation_to_portfolio=.55,
    fractional_kelly=.25,
    max_position=.08,
    risk_budget=.015,
):
    """Convert thesis economics into a capped position size.

    Kelly-like sizing uses expected return / variance, then a portfolio marginal-risk
    cap limits the position using asset volatility and correlation.
    """
    variance=max(scenario_volatility**2,1e-8)
    raw_kelly=max(0.0,expected_return/variance)
    kelly_size=fractional_kelly*raw_kelly
    marginal_vol=max(asset_volatility*abs(correlation_to_portfolio),1e-6)
    risk_cap=risk_budget/marginal_vol
    size=min(kelly_size,max_position,risk_cap)
    return {
        "raw_kelly":float(raw_kelly),
        "fractional_kelly_size":float(kelly_size),
        "risk_budget_cap":float(risk_cap),
        "recommended_weight":float(max(0,size)),
    }

def portfolio_impact(weight,asset_volatility=.25,portfolio_volatility=.12,correlation=.55):
    # Approximate new volatility after adding/reallocating weight to the position.
    base=max(1-weight,0)
    variance=(
        (base*portfolio_volatility)**2+
        (weight*asset_volatility)**2+
        2*base*weight*portfolio_volatility*asset_volatility*correlation
    )
    return {
        "approx_portfolio_vol_before":float(portfolio_volatility),
        "approx_portfolio_vol_after":float(np.sqrt(max(variance,0))),
        "standalone_position_vol_contribution":float(weight*asset_volatility),
    }
