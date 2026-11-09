import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

st.set_page_config(page_title="월별 기온분석", page_icon="🌡️", layout="wide")
st.title("🌡️ 월별 기온분석")
st.write("월을 선택하면 해당 월의 연도별 최고기온과 최저기온을 그래프로 확인할 수 있습니다.")

# 이 파일은 pages 폴더 안에 있으므로 CSV는 프로젝트 최상위 폴더에서 찾습니다.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_DIR / "temperature_cleaned.csv"

@st.cache_data
def load_data():
    try:
        data = pd.read_csv(DATA_PATH, encoding="utf-8-sig")
    except UnicodeDecodeError:
        data = pd.read_csv(DATA_PATH, encoding="euc-kr")

    required = ["날짜", "최고기온(℃)", "최저기온(℃)"]
    missing = [col for col in required if col not in data.columns]
    if missing:
        raise ValueError(f"CSV 파일에 필요한 컬럼이 없습니다: {', '.join(missing)}")

    data["날짜"] = pd.to_datetime(data["날짜"], errors="coerce")
    data["최고기온(℃)"] = pd.to_numeric(data["최고기온(℃)"], errors="coerce")
    data["최저기온(℃)"] = pd.to_numeric(data["최저기온(℃)"], errors="coerce")
    data = data.dropna(subset=["날짜"]).copy()
    data["연도"] = data["날짜"].dt.year
    data["월"] = data["날짜"].dt.month
    return data

if not DATA_PATH.exists():
    st.error(
        "temperature_cleaned.csv 파일을 찾을 수 없습니다. "
        "프로젝트 최상위 폴더에 CSV 파일을 업로드했는지 확인해주세요."
    )
    st.stop()

try:
    df = load_data()
except Exception as error:
    st.error(f"데이터를 불러오지 못했습니다: {error}")
    st.stop()

month = st.selectbox(
    "분석할 월을 선택하세요.",
    options=list(range(1, 13)),
    format_func=lambda value: f"{value}월"
)

month_df = df[df["월"] == month]
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
    # 한글 폰트가 없는 클라우드 환경에서도 그래프의 축/범례가 깨지지 않도록
    # 기본 폰트를 사용하고, 그래프 제목과 축은 영문이 아닌 한글로 표시합니다.
    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        yearly_df["연도"],
        yearly_df["최고기온(℃)"],
        color="#FF1493",
        marker="o",
        linewidth=2,
        label="최고기온"
    )
    ax.plot(
        yearly_df["연도"],
        yearly_df["최저기온(℃)"],
        color="#87CEEB",
        marker="o",
        linewidth=2,
        label="최저기온"
    )

    ax.set_title("월별 기온분석", fontsize=16)
    ax.set_xlabel("연도")
    ax.set_ylabel("온도(℃)")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

    with st.expander("연도별 기온 데이터 표 보기"):
        st.dataframe(yearly_df, use_container_width=True, hide_index=True)

    st.caption(f"총 {len(yearly_df):,}개 연도의 {month}월 데이터입니다.")
