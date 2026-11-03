import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# -----------------------------
# 페이지 기본 설정
# -----------------------------
st.set_page_config(
    page_title="World MBTI Explorer",
    page_icon="🌎",
    layout="wide",
)

# -----------------------------
# 데이터 불러오기
# app.py와 CSV 파일을 같은 폴더에 둡니다.
# -----------------------------
DATA_FILE = Path(__file__).parent / "countriesMBTI_16types.csv"

@st.cache_data
def load_data(file_path: str) -> pd.DataFrame:
    data = pd.read_csv(file_path)
    if "Country" not in data.columns:
        raise ValueError("CSV 파일에 'Country' 열이 없습니다.")

    mbti_columns = [column for column in data.columns if column != "Country"]
    if len(mbti_columns) != 16:
        raise ValueError(f"MBTI 열은 16개여야 합니다. 현재 {len(mbti_columns)}개입니다.")

    data["Country"] = data["Country"].astype(str).str.strip()
    for column in mbti_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(subset=["Country"])
    data = data.dropna(subset=mbti_columns, how="all")
    return data, mbti_columns

st.title("🌎 World MBTI Explorer")
st.caption("국가를 선택하면 해당 국가의 MBTI 16가지 유형별 비율을 확인할 수 있어요.")

if not DATA_FILE.exists():
    st.error(
        "CSV 파일을 찾을 수 없습니다. "
        "countriesMBTI_16types.csv 파일을 app.py와 같은 폴더에 넣어주세요."
    )
    st.stop()

try:
    df, mbti_columns = load_data(str(DATA_FILE))
except Exception as error:
    st.error(f"데이터를 불러오는 중 문제가 발생했습니다: {error}")
    st.stop()

# 국가 선택
countries = sorted(df["Country"].dropna().unique().tolist())
selected_country = st.selectbox(
    "🗺️ 국가 선택",
    options=countries,
    index=countries.index("South Korea") if "South Korea" in countries else 0,
)

country_data = df.loc[df["Country"] == selected_country, mbti_columns].iloc[0]
chart_data = (
    pd.DataFrame({
        "MBTI": mbti_columns,
        "비율": [float(country_data[mbti]) for mbti in mbti_columns],
    })
    .dropna()
    .sort_values("비율", ascending=False)
    .reset_index(drop=True)
)

# 데이터가 0~1 사이의 비율이면 퍼센트로 변환
if not chart_data.empty and chart_data["비율"].max() <= 1:
    chart_data["비율(%)"] = chart_data["비율"] * 100
else:
    chart_data["비율(%)"] = chart_data["비율"]

# 1위는 빨간색, 나머지는 진한 파랑에서 연한 파랑으로 그라데이션
def hex_to_rgb(hex_color: str):
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def blend(start, end, ratio):
    return tuple(
        round(start[i] + (end[i] - start[i]) * ratio)
        for i in range(3)
    )

red = "#E53935"
blue_start = hex_to_rgb("#2563EB")
blue_end = hex_to_rgb("#DBEAFE")

colors = [red]
remaining_count = max(len(chart_data) - 1, 1)
for index in range(len(chart_data) - 1):
    ratio = index / max(remaining_count - 1, 1)
    colors.append(rgb_to_hex(blend(blue_start, blue_end, ratio)))

# 상단 요약
if not chart_data.empty:
    top_mbti = chart_data.iloc[0]["MBTI"]
    top_rate = chart_data.iloc[0]["비율(%)"]

    col1, col2, col3 = st.columns(3)
    col1.metric("선택 국가", selected_country)
    col2.metric("가장 높은 MBTI", top_mbti)
    col3.metric("1위 비율", f"{top_rate:.2f}%")

    st.subheader(f"📊 {selected_country}의 MBTI 비율")

    fig = go.Figure(
        data=[
            go.Bar(
                x=chart_data["MBTI"],
                y=chart_data["비율(%)"],
                marker=dict(color=colors),
                text=[f"{value:.2f}%" for value in chart_data["비율(%)"]],
                textposition="outside",
                cliponaxis=False,
                hovertemplate="%{x}<br>비율: %{y:.2f}%<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        xaxis_title="MBTI 유형",
        yaxis_title="비율(%)",
        yaxis=dict(rangemode="tozero", ticksuffix="%"),
        template="plotly_white",
        height=560,
        margin=dict(l=25, r=25, t=35, b=35),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption("🔴 1위 MBTI  |  🔵 나머지 MBTI는 높은 비율부터 낮은 비율 순으로 파란색이 점점 연해집니다.")

    with st.expander("📋 비율 데이터 표 보기"):
        display_data = chart_data[["MBTI", "비율(%)"]].copy()
        display_data["비율(%)"] = display_data["비율(%)"].map(lambda value: f"{value:.2f}%")
        st.dataframe(display_data, use_container_width=True, hide_index=True)

st.divider()
st.caption(
    f"총 {len(countries)}개 국가 · MBTI 16개 유형 | "
    "이 데이터는 제공된 CSV 파일을 기반으로 하며, 실제 전체 인구의 성격 유형을 확정하는 자료는 아닙니다."
)
