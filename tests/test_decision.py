import numpy as np
from narrative_position.model import load_case,scenario_table,reverse_dcf_growth
from narrative_position.sizing import scenario_statistics,position_size,portfolio_impact

def test_scenario_ordering():
    h,b,s=load_case(); t=scenario_table(h,b,s,350)
    x=t.set_index("scenario")["value_per_share"]
    assert x["bull"]>x["base"]>x["bear"]
    assert np.isclose(t["probability"].sum(),1)

def test_reverse_dcf_reprices_market():
    h,b,_=load_case()
    g=reverse_dcf_growth(h,b,350)
    assert np.isfinite(g)
    assert -.15<g<.40

def test_position_size_respects_caps():
    h,b,s=load_case(); t=scenario_table(h,b,s,350)
    stats=scenario_statistics(t)
    size=position_size(stats["expected_return"],stats["scenario_volatility"],max_position=.08,risk_budget=.015)
    assert 0<=size["recommended_weight"]<=.08

def test_portfolio_impact_finite():
    x=portfolio_impact(.05)
    assert np.isfinite(x["approx_portfolio_vol_after"])
    assert x["approx_portfolio_vol_after"]>0
