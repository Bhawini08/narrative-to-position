import sys
from pathlib import Path
import streamlit as st
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/"src"))
from narrative_position.model import load_case,scenario_table,reverse_dcf_growth
from narrative_position.sizing import scenario_statistics,position_size,portfolio_impact

st.set_page_config(page_title="From Narrative to Position",layout="wide")
st.title("From Narrative to Position")
st.caption("Fundamentals → embedded expectations → scenarios → sizing → portfolio impact")

price=st.sidebar.number_input("Market price",min_value=1.0,value=350.0,step=1.0)
asset_vol=st.sidebar.slider("Asset volatility",.10,.60,.25,.01)
portfolio_vol=st.sidebar.slider("Portfolio volatility",.05,.30,.12,.01)
corr=st.sidebar.slider("Correlation to portfolio",-1.0,1.0,.55,.05)

h,b,s=load_case(); table=scenario_table(h,b,s,price)
stats=scenario_statistics(table); implied=reverse_dcf_growth(h,b,price)
size=position_size(stats["expected_return"],stats["scenario_volatility"],asset_vol,portfolio_vol,corr)
impact=portfolio_impact(size["recommended_weight"],asset_vol,portfolio_vol,corr)

c1,c2,c3,c4=st.columns(4)
c1.metric("Expected return",f"{stats['expected_return']:.1%}")
c2.metric("Loss probability",f"{stats['probability_of_loss']:.0%}")
c3.metric("Implied revenue CAGR",f"{implied:.1%}" if implied==implied else "n/a")
c4.metric("Position size",f"{size['recommended_weight']:.1%}")

st.subheader("Scenario valuation")
st.dataframe(table,use_container_width=True)
st.bar_chart(table.set_index("scenario")["value_per_share"])

st.subheader("Portfolio impact")
st.json(impact)

st.subheader("Thesis monitoring")
st.dataframe(__import__("pandas").read_csv(ROOT/"data/thesis_monitor.csv"),use_container_width=True)
