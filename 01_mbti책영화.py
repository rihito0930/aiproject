

# -----------------------------
# 페이지 설정
# -----------------------------
st.set_page_config(
    page_title="MBTI 취향 추천소 📚",
    page_icon="💗",
    layout="wide"
)

# -----------------------------
# 도서 데이터
# 한국 작가의 작품만 사용
# -----------------------------
books = {
    "아몬드": {
        "author": "손원평",
        "description": "감정과 공감에 대해 생각해 볼 수 있는 특별한 성장 소설이에요.",
        "genre": "성장 소설"
    },
    "불편한 편의점": {
        "author": "김호연",
        "description": "편의점을 배경으로 다양한 사람들의 따뜻한 이야기를 담았어요.",
        "genre": "힐링 소설"
    },
    "완득이": {
        "author": "김려령",
        "description": "유쾌한 일상 속에서 성장과 가족의 의미를 느낄 수 있어요.",
        "genre": "성장 소설"
    },
    "달러구트 꿈 백화점": {
        "author": "이미예",
        "description": "꿈을 사고파는 신비로운 세계를 경험할 수 있는 판타지 소설이에요.",
        "genre": "판타지"
    },
    "페인트": {
        "author": "이희영",
        "description": "부모와 가족의 의미에 대해 새로운 시각으로 생각하게 해줘요.",
        "genre": "청소년 소설"
    },
    "체리새우: 비밀글입니다": {
        "author": "황영미",
        "description": "친구 관계와 학교생활 속에서 진정한 나를 찾아가는 이야기예요.",
        "genre": "청소년 소설"
    },
    "시간을 파는 상점": {
        "author": "김선영",
        "description": "시간과 선택, 책임의 의미를 생각하게 하는 청소년 소설이에요.",
        "genre": "청소년 소설"
    },
    "위저드 베이커리": {
        "author": "구병모",
        "description": "신비로운 빵집에서 벌어지는 흥미진진한 판타지 이야기예요.",
        "genre": "판타지"
    }
}

# -----------------------------
# 영화 데이터
# 2010년 이후 개봉 + 로맨스 장르
# -----------------------------
movies = {
    "건축학개론": {
        "year": 2012,
        "genre": "로맨스",
        "description": "첫사랑의 설렘과 추억을 그린 감성적인 영화예요."
    },
    "오늘의 연애": {
        "year": 2015,
        "genre": "로맨스",
        "description": "친구와 연인 사이에서 벌어지는 현실적인 사랑 이야기예요."
    },
    "뷰티 인사이드": {
        "year": 2015,
        "genre": "로맨스",
        "description": "매일 모습이 달라지는 사람의 특별한 사랑 이야기예요."
    },
    "좋아해줘": {
        "year": 2016,
        "genre": "로맨스",
        "description": "SNS를 통해 시작되는 세 커플의 사랑 이야기예요."
    },
    "너의 결혼식": {
        "year": 2018,
        "genre": "로맨스",
        "description": "첫사랑과 시간의 흐름을 담은 청춘 로맨스예요."
    },
    "가장 보통의 연애": {
        "year": 2019,
        "genre": "로맨스",
        "description": "이별 이후 새로운 사랑을 시작하는 현실적인 이야기예요."
    },
    "새해전야": {
        "year": 2021,
        "genre": "로맨스",
        "description": "새해를 앞둔 여러 사람들의 사랑과 새로운 출발을 담았어요."
    },
    "싱글 인 서울": {
        "year": 2023,
        "genre": "로맨스",
        "description": "혼자가 좋은 사람과 사랑을 꿈꾸는 사람의 이야기예요."
    }
}

# -----------------------------
# MBTI별 추천 정보
# -----------------------------
mbti_data = {
    "ISTJ": {
        "personality": "차분하고 책임감이 강한 현실주의자 📋",
        "books": ["시간을 파는 상점", "불편한 편의점"],
        "movies": ["건축학개론", "싱글 인 서울"]
    },
    "ISFJ": {
        "personality": "따뜻하고 배려심이 많은 수호자 💗",
        "books": ["불편한 편의점", "체리새우: 비밀글입니다"],
        "movies": ["뷰티 인사이드", "좋아해줘"]
    },
    "INFJ": {
        "personality": "깊이 생각하고 의미를 중요하게 생각해요 🌙",
        "books": ["아몬드", "페인트"],
        "movies": ["너의 결혼식", "뷰티 인사이드"]
    },
    "INTJ": {
        "personality": "분석적이고 독립적인 전략가 🧠",
        "books": ["위저드 베이커리", "시간을 파는 상점"],
        "movies": ["싱글 인 서울", "가장 보통의 연애"]
    },
    "ISTP": {
        "personality": "호기심이 많고 독립적인 탐험가 🔍",
        "books": ["위저드 베이커리", "아몬드"],
        "movies": ["건축학개론", "가장 보통의 연애"]
    },
    "ISFP": {
        "personality": "감수성이 풍부하고 자유로운 예술가 🎨",
        "books": ["달러구트 꿈 백화점", "체리새우: 비밀글입니다"],
        "movies": ["뷰티 인사이드", "너의 결혼식"]
    },
    "INFP": {
        "personality": "상상력이 풍부하고 따뜻한 이상주의자 🌷",
        "books": ["달러구트 꿈 백화점", "아몬드"],
        "movies": ["너의 결혼식", "새해전야"]
    },
    "INTP": {
        "personality": "논리적이고 새로운 생각을 좋아하는 탐구자 💡",
        "books": ["위저드 베이커리", "페인트"],
        "movies": ["뷰티 인사이드", "싱글 인 서울"]
    },
    "ESTP": {
        "personality": "활동적이고 도전을 즐기는 모험가 ⚡",
        "books": ["완득이", "위저드 베이커리"],
        "movies": ["오늘의 연애", "가장 보통의 연애"]
    },
    "ESFP": {
        "personality": "밝고 에너지가 넘치는 분위기 메이커 🎉",
        "books": ["완득이", "불편한 편의점"],
        "movies": ["좋아해줘", "새해전야"]
    },
    "ENFP": {
        "personality": "열정적이고 상상력이 풍부한 아이디어 뱅크 🌈",
        "books": ["달러구트 꿈 백화점", "완득이"],
        "movies": ["좋아해줘", "너의 결혼식"]
    },
    "ENTP": {
        "personality": "창의적이고 새로운 도전을 좋아하는 발명가 🚀",
        "books": ["위저드 베이커리", "페인트"],
        "movies": ["오늘의 연애", "싱글 인 서울"]
    },
    "ESTJ": {
        "personality": "체계적이고 추진력이 뛰어난 리더 👑",
        "books": ["시간을 파는 상점", "완득이"],
        "movies": ["가장 보통의 연애", "건축학개론"]
    },
    "ESFJ": {
        "personality": "사교적이고 주변 사람을 잘 챙기는 친선도모자 🤝",
        "books": ["불편한 편의점", "완득이"],
        "movies": ["좋아해줘", "새해전야"]
    },
    "ENFJ": {
        "personality": "공감 능력이 뛰어나고 사람을 이끄는 리더 🌟",
        "books": ["아몬드", "체리새우: 비밀글입니다"],
        "movies": ["뷰티 인사이드", "너의 결혼식"]
    },
    "ENTJ": {
        "personality": "목표 지향적이고 결단력 있는 지도자 🏆",
        "books": ["시간을 파는 상점", "페인트"],
        "movies": ["싱글 인 서울", "오늘의 연애"]
    }
}

# -----------------------------
# 화면 디자인
# -----------------------------
st.title("💗 MBTI 취향 추천소")
st.subheader("나의 MBTI에 맞는 책과 영화를 찾아보자!")
st.write("나의 성격에 어울리는 작품은 무엇일까? ✨")

st.divider()

st.markdown("### 🔎 나의 MBTI를 선택해 주세요!")

mbti_list = list(mbti_data.keys())

selected_mbti = st.selectbox(
    "MBTI 유형 선택",
    mbti_list,
    index=mbti_list.index("ENFP")
)

# -----------------------------
# 추천 결과
# -----------------------------
if st.button("🎁 나에게 맞는 작품 추천받기", use_container_width=True):

    result = mbti_data[selected_mbti]

    st.balloons()

    st.divider()

    st.header(f"🌟 {selected_mbti} 추천 결과")

    st.info(result["personality"])

    # 책 추천
    st.markdown("## 📚 당신을 위한 책 2권")

    col1, col2 = st.columns(2)

    for col, book_name in zip(
        [col1, col2], result["books"]
    ):
        with col:
            book = books[book_name]
            st.markdown(f"### 📖 {book_name}")
            st.write(f"✍️ 작가: {book['author']}")
            st.write(f"🏷️ 장르: {book['genre']}")
            st.write(book["description"])

    st.divider()

    # 영화 추천
    st.markdown("## 🎬 당신을 위한 로맨스 영화 2편")

    col3, col4 = st.columns(2)

    for col, movie_name in zip(
        [col3, col4], result["movies"]
    ):
        with col:
            movie = movies[movie_name]
            st.markdown(f"### 🍿 {movie_name}")
            st.write(f"📅 개봉 연도: {movie['year']}년")
            st.write(f"❤️ 장르: {movie['genre']}")
            st.write(movie["description"])

    st.divider()

    st.success("오늘의 추천이 마음에 들었나요? 💕")
    st.caption(
        "※ MBTI는 성향을 알아보는 참고 자료이며, "
        "추천은 재미와 취향을 위한 콘텐츠입니다."
    )

st.markdown("---")
st.caption("📚 MBTI 취향 추천소 | 나만의 문화생활 찾기 💗")
