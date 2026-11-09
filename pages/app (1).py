import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="월별 기온 분석",
    page_icon="🌡️",
    layout="wide"
)

st.title("🌡️ 월별 기온분석")
st.write("월을 선택하면 해당 월의 연도별 최고기온과 최저기온을 확인할 수 있습니다.")

# -----------------------------
# 데이터 불러오기
# app.py와 CSV 파일은 같은 폴더에 넣어주세요.
# -----------------------------
DATA_PATH = Path(__file__).parent / "temperature_cleaned.csv"

@st.cache_data
def load_data():
    # UTF-8-SIG를 우선 사용하고, 기존 원본 파일도 읽을 수 있도록 인코딩 대체
    try:
        data = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    except UnicodeDecodeError:
        data = pd.read_csv(DATA_PATH, encoding="euc-kr")

    # 날짜와 기온 데이터 정리
    data["날짜"] = pd.to_datetime(data["날짜"], errors="coerce")
    data = data.dropna(subset=["날짜"]).copy()

    for column in ["최고기온(℃)", "최저기온(℃)"]:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month

    return data

try:
    df = load_data()
except FileNotFoundError:
    st.error(
        "temperature_cleaned.csv 파일을 찾을 수 없습니다. "
        "app.py와 같은 폴더에 CSV 파일을 넣어주세요."
    )
    st.stop()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# -----------------------------
# 월 선택
# -----------------------------
month = st.selectbox(
    "분석할 월을 선택하세요.",
    options=list(range(1, 13)),
    format_func=lambda x: f"{x}월"
)

# 선택한 월의 데이터만 추출
month_df = df[df["월"] == month].copy()

# 같은 연도에 데이터가 여러 개 있을 경우 연도별 최고/최저값으로 정리
yearly_df = (
    month_df.groupby("연도", as_index=False)
    .agg({
        "최고기온(℃)": "max",
        "최저기온(℃)": "min"
    })
    .sort_values("연도")
)

st.subheader(f"{month}월 연도별 기온 데이터")

if yearly_df.empty:
    st.warning(f"{month}월에 해당하는 데이터가 없습니다.")
else:
    # -----------------------------
    # 그래프
    # -----------------------------
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=yearly_df["연도"],
        y=yearly_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="#FF1493", width=2.5),
        marker=dict(color="#FF1493", size=6)
    ))

    fig.add_trace(go.Scatter(
        x=yearly_df["연도"],
        y=yearly_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="#87CEEB", width=2.5),
        marker=dict(color="#87CEEB", size=6)
    ))

    fig.update_layout(
        title="월별 기온분석",
        xaxis_title="연도",
        yaxis_title="온도(℃)",
        legend_title="기온 구분",
        hovermode="x unified",
        template="plotly_white",
        height=600
    )

    fig.update_xaxes(
        tickformat="d",
        showgrid=True
    )
    fig.update_yaxes(
        showgrid=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------
    # 데이터 표
    # -----------------------------
    with st.expander("연도별 기온 데이터 표 보기"):
        display_df = yearly_df.rename(columns={
            "연도": "연도",
            "최고기온(℃)": "최고기온(℃)",
            "최저기온(℃)": "최저기온(℃)"
        })
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.caption(f"총 {len(yearly_df):,}개 연도의 {month}월 데이터가 표시되었습니다.")
