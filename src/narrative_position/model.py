from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.optimize import brentq

def load_case():
    hist=pd.read_csv("data/visa_historicals.csv").set_index("year")
    bs=pd.read_csv("data/visa_balance_sheet_2025.csv").set_index("item")["value"]
    scenarios=pd.read_csv("data/scenarios.csv")
    return hist,bs,scenarios

def normalized_fcf(hist:pd.DataFrame)->pd.Series:
    return hist["cfo"]-hist["capex"]

def scenario_dcf(hist,bs,row,current_shares=None):
    base_rev=float(hist.loc[2025,"revenue"])
    shares=float(current_shares or hist.loc[2025,"diluted_shares"])
    rev=base_rev; fcfs=[]
    for i in range(1,6):
        rev*=1+float(row[f"revenue_growth_{i}"])
        fcfs.append(rev*float(row[f"fcf_margin_{i}"]))
    wacc=float(row["wacc"]); g=float(row["terminal_growth"])
    years=np.arange(1,6)
    pv_explicit=float(np.sum(np.asarray(fcfs)/(1+wacc)**years))
    terminal=fcfs[-1]*(1+g)/(wacc-g)
    pv_terminal=float(terminal/(1+wacc)**5)
    ev=pv_explicit+pv_terminal
    net_debt=float(bs["debt"]-bs["cash"]-bs["investments"])
    equity=ev-net_debt
    return {
        "enterprise_value":ev,
        "equity_value":equity,
        "value_per_share":equity/shares,
        "pv_explicit":pv_explicit,
        "pv_terminal":pv_terminal,
        "terminal_value_share":pv_terminal/ev,
    }

def scenario_table(hist,bs,scenarios,market_price):
    rows=[]
    for _,s in scenarios.iterrows():
        d=scenario_dcf(hist,bs,s)
        rows.append({
            "scenario":s["scenario"],
            "probability":float(s["probability"]),
            **d,
            "return_to_value":d["value_per_share"]/market_price-1,
        })
    out=pd.DataFrame(rows)
    if not np.isclose(out["probability"].sum(),1):
        raise ValueError("scenario probabilities must sum to one")
    return out

def reverse_dcf_growth(hist,bs,market_price,wacc=.075,terminal_growth=.03,fcf_margin=.51,years=5):
    """Solve constant revenue CAGR required for DCF value to equal market price."""
    revenue=float(hist.loc[2025,"revenue"])
    shares=float(hist.loc[2025,"diluted_shares"])
    net_debt=float(bs["debt"]-bs["cash"]-bs["investments"])
    def value(growth):
        rev=revenue
        fcfs=[]
        for _ in range(years):
            rev*=1+growth
            fcfs.append(rev*fcf_margin)
        n=np.arange(1,years+1)
        ev=float(np.sum(np.asarray(fcfs)/(1+wacc)**n))
        ev+=fcfs[-1]*(1+terminal_growth)/(wacc-terminal_growth)/(1+wacc)**years
        equity=ev-net_debt
        return equity/shares
    target=lambda growth:value(growth)-market_price
    lo,hi=-.15,.40
    if target(lo)*target(hi)>0:
        return np.nan
    return float(brentq(target,lo,hi))

def expectations_gap(base_growth,implied_growth):
    return float(base_growth-implied_growth)
