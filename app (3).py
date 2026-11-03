import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

# --------------------------------------------------
# 기본 설정
# --------------------------------------------------
st.set_page_config(
    page_title="World MBTI Explorer",
    page_icon="🌎",
    layout="wide",
)

# --------------------------------------------------
# 파일 경로
# 현재 구조:
# 프로젝트 폴더/
# ├── countriesMBTI_16types.csv
# ├── requirements.txt
# └── pages/
#     └── app.py
#
# app.py가 pages 폴더 안에 있으므로,
# 부모 폴더에서 CSV 파일을 찾습니다.
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "countriesMBTI_16types.csv"


@st.cache_data
def load_data(file_path):
    data = pd.read_csv(file_path)

    if "Country" not in data.columns:
        raise ValueError("CSV 파일에 'Country' 열이 없습니다.")

    mbti_columns = [column for column in data.columns if column != "Country"]

    if len(mbti_columns) != 16:
        raise ValueError(
            f"MBTI 열은 16개여야 합니다. 현재 {len(mbti_columns)}개입니다."
        )

    data["Country"] = data["Country"].astype(str).str.strip()

    for column in mbti_columns:
        data[column] = pd.to_numeric(data[column], errors="coerce")

    data = data.dropna(subset=["Country"])
    data = data.dropna(subset=mbti_columns, how="all")

    return data, mbti_columns


def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip("#")
    return tuple(
        int(hex_color[i:i + 2], 16)
        for i in (0, 2, 4)
    )


def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)


def make_gradient_colors(count):
    """첫 번째 막대는 빨간색, 나머지는 파란색 계열 그라데이션."""
    if count <= 0:
        return []

    colors = ["#E53935"]

    if count == 1:
        return colors

    blue_start = hex_to_rgb("#2563EB")
    blue_end = hex_to_rgb("#DBEAFE")

    for index in range(count - 1):
        ratio = index / max(count - 2, 1)

        rgb = tuple(
            round(
                blue_start[channel]
                + (blue_end[channel] - blue_start[channel]) * ratio
            )
            for channel in range(3)
        )

        colors.append(rgb_to_hex(rgb))

    return colors


def convert_to_percent(values):
    """데이터가 0~1 범위의 비율이면 100을 곱해 퍼센트로 변환."""
    values = pd.to_numeric(values, errors="coerce")

    if values.dropna().empty:
        return values

    if values.max() <= 1:
        return values * 100

    return values


# --------------------------------------------------
# 제목 및 데이터 확인
# --------------------------------------------------
st.title("🌎 World MBTI Explorer")
st.write(
    "국가별 MBTI 비율을 확인하고, MBTI 유형별로 비율이 높은 국가 순위를 살펴보세요!"
)

if not DATA_FILE.exists():
    st.error("CSV 파일을 찾을 수 없습니다.")
    st.info(
        "countriesMBTI_16types.csv 파일이 프로젝트 최상위 폴더에 있는지 확인하세요."
    )
    st.code(
        "프로젝트 폴더/\n"
        "├── countriesMBTI_16types.csv\n"
        "├── requirements.txt\n"
        "└── pages/\n"
        "    └── app.py"
    )
    st.stop()

try:
    df, mbti_columns = load_data(DATA_FILE)
except Exception as error:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {error}")
    st.stop()

countries = sorted(df["Country"].dropna().unique().tolist())


# --------------------------------------------------
# 탭 구성
# --------------------------------------------------
tab_country, tab_mbti = st.tabs(
    ["🌍 국가별 MBTI 분석", "🏆 MBTI별 국가 순위"]
)


# ==================================================
# TAB 1. 국가를 선택하면 16개 MBTI 비율 표시
# ==================================================
with tab_country:
    st.subheader("🌍 국가별 MBTI 비율")

    default_country_index = (
        countries.index("South Korea")
        if "South Korea" in countries
        else 0
    )

    selected_country = st.selectbox(
        "국가를 선택하세요.",
        options=countries,
        index=default_country_index,
        key="country_select",
    )

    country_row = df.loc[
        df["Country"] == selected_country,
        mbti_columns
    ].iloc[0]

    country_chart = pd.DataFrame(
        {
            "MBTI": mbti_columns,
            "비율": [country_row[mbti] for mbti in mbti_columns],
        }
    )

    country_chart["비율(%)"] = convert_to_percent(country_chart["비율"])
    country_chart = (
        country_chart
        .dropna(subset=["비율(%)"])
        .sort_values("비율(%)", ascending=False)
        .reset_index(drop=True)
    )

    if not country_chart.empty:
        top_mbti = country_chart.iloc[0]["MBTI"]
        top_rate = country_chart.iloc[0]["비율(%)"]

        metric1, metric2, metric3 = st.columns(3)
        metric1.metric("선택 국가", selected_country)
        metric2.metric("가장 높은 MBTI", top_mbti)
        metric3.metric("1위 비율", f"{top_rate:.2f}%")

        colors = make_gradient_colors(len(country_chart))

        fig_country = go.Figure(
            go.Bar(
                x=country_chart["MBTI"],
                y=country_chart["비율(%)"],
                marker_color=colors,
                text=[
                    f"{value:.2f}%"
                    for value in country_chart["비율(%)"]
                ],
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "MBTI: %{x}<br>"
                    "비율: %{y:.2f}%"
                    "<extra></extra>"
                ),
            )
        )

        fig_country.update_layout(
            title=f"{selected_country}의 MBTI 16가지 유형",
            xaxis_title="MBTI 유형",
            yaxis_title="비율(%)",
            yaxis=dict(
                rangemode="tozero",
                ticksuffix="%",
            ),
            template="plotly_white",
            height=560,
            margin=dict(l=25, r=25, t=65, b=40),
            showlegend=False,
        )

        st.plotly_chart(
            fig_country,
            use_container_width=True,
        )

        st.caption(
            "🔴 1위는 빨간색이며, 나머지는 비율이 높은 순서대로 "
            "진한 파란색에서 연한 파란색으로 표시됩니다."
        )

        with st.expander("📋 선택한 국가의 전체 비율 보기"):
            display_country = country_chart[["MBTI", "비율(%)"]].copy()
            display_country.insert(
                0,
                "순위",
                range(1, len(display_country) + 1),
            )
            display_country["비율(%)"] = display_country["비율(%)"].map(
                lambda value: f"{value:.2f}%"
            )
            st.dataframe(
                display_country,
                use_container_width=True,
                hide_index=True,
            )


# ==================================================
# TAB 2. MBTI를 선택하면 국가별 순위 표시
# ==================================================
with tab_mbti:
    st.subheader("🏆 MBTI별 국가 순위")
    st.write(
        "MBTI 유형을 선택하면 해당 유형의 비율이 높은 국가부터 1위 순서로 보여줍니다."
    )

    selected_mbti = st.selectbox(
        "MBTI 유형을 선택하세요.",
        options=mbti_columns,
        index=mbti_columns.index("ENFP") if "ENFP" in mbti_columns else 0,
        key="mbti_select",
    )

    ranking = df[["Country", selected_mbti]].copy()
    ranking[selected_mbti] = convert_to_percent(ranking[selected_mbti])

    ranking = (
        ranking
        .dropna(subset=[selected_mbti])
        .sort_values(
            by=selected_mbti,
            ascending=False,
        )
        .reset_index(drop=True)
    )

    ranking.insert(0, "순위", range(1, len(ranking) + 1))

    if not ranking.empty:
        first_country = ranking.iloc[0]["Country"]
        first_rate = ranking.iloc[0][selected_mbti]

        rank_col1, rank_col2, rank_col3 = st.columns(3)
        rank_col1.metric("선택 MBTI", selected_mbti)
        rank_col2.metric("1위 국가", first_country)
        rank_col3.metric("1위 비율", f"{first_rate:.2f}%")

        st.markdown(f"### 🥇 {selected_mbti} 비율이 높은 국가 TOP 10")

        top10 = ranking.head(10).copy()
        top10_colors = make_gradient_colors(len(top10))

        fig_ranking = go.Figure(
            go.Bar(
                x=top10[selected_mbti],
                y=top10["Country"],
                orientation="h",
                marker_color=top10_colors,
                text=[
                    f"{value:.2f}%"
                    for value in top10[selected_mbti]
                ],
                textposition="outside",
                cliponaxis=False,
                hovertemplate=(
                    "국가: %{y}<br>"
                    "비율: %{x:.2f}%"
                    "<extra></extra>"
                ),
            )
        )

        # 가로 막대그래프에서 1위가 맨 위에 오도록 설정
        fig_ranking.update_layout(
            xaxis_title="비율(%)",
            yaxis_title="국가",
            xaxis=dict(
                rangemode="tozero",
                ticksuffix="%",
            ),
            yaxis=dict(
                autorange="reversed",
            ),
            template="plotly_white",
            height=480,
            margin=dict(l=25, r=55, t=25, b=40),
            showlegend=False,
        )

        st.plotly_chart(
            fig_ranking,
            use_container_width=True,
        )

        st.markdown(f"### 📋 {selected_mbti} 전체 국가 순위")

        display_ranking = ranking.copy()
        display_ranking.columns = ["순위", "국가", "비율(%)"]
        display_ranking["비율(%)"] = display_ranking["비율(%)"].map(
            lambda value: f"{value:.2f}%"
        )

        st.dataframe(
            display_ranking,
            use_container_width=True,
            hide_index=True,
            height=500,
        )


# --------------------------------------------------
# 하단 안내
# --------------------------------------------------
st.divider()
st.caption(
    f"총 {len(countries)}개 국가 · MBTI 16개 유형 | "
    "제공된 CSV 데이터를 기반으로 한 참고용 통계입니다. "
    "국가 전체 인구의 실제 MBTI 분포를 확정하는 자료는 아닙니다."
)
