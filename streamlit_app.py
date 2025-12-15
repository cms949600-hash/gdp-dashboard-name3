import streamlit as st
import pandas as pd
import math
from pathlib import Path

# Set the title and favicon that appear in the Browser's tab bar.
st.set_page_config(
    page_title='GDP dashboard',
    page_icon=':earth_americas:', # This is an emoji shortcode. Could be a URL too.
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_gdp_data():
    """Grab GDP data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/gdp_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    MIN_YEAR = 1960
    MAX_YEAR = 2022

    # The data above has columns like:
    # - Country Name
    # - Country Code
    # - [Stuff I don't care about]
    # - GDP for 1960
    # - GDP for 1961
    import streamlit as st
    import random
    from typing import List

    # Page configuration
    st.set_page_config(page_title='✨ 제목학원 - 브랜딩 도우미', page_icon='✨', layout='centered')

    # ----------------------
    # CSS: 인스타 느낌의 파스텔 UI
    css = '''
    <style>
    body {background: linear-gradient(135deg, #fff0f6 0%, #fffaf0 100%);} 
    .main {font-family: -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial;}
    .stApp {background: transparent}
    .card {background: linear-gradient(180deg, rgba(255,255,255,0.8), rgba(255,250,240,0.8));
           border-radius:16px; padding:20px; box-shadow: 0 8px 30px rgba(0,0,0,0.08);}
    .title {font-weight:700; font-size:28px; color:#333333}
    .subtitle {color:#6b6b6b; margin-top:6px}
    .result {font-size:28px; font-weight:800; color:#b34d76}
    .muted {color:#8b8787}
    .big-emoji {font-size:42px}
    .small-pill {background:#fff0f6; padding:6px 10px; border-radius:999px; color:#b34d76; font-weight:600}
    </style>
    '''

    st.markdown(css, unsafe_allow_html=True)

    # Header
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="display:flex; align-items:center; gap:12px">'
                    f'<div class="big-emoji">✨</div>'
                    f'<div><div class="title">✨ 제목학원 - 브랜딩 도우미</div>'
                    f'<div class="subtitle">유머와 센스가 묻어나는 나만의 이름 만들기</div></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Input card
    st.markdown('<br/>', unsafe_allow_html=True)
    with st.form(key='branding_form'):
        st.markdown('<div class="card">', unsafe_allow_html=True)
        key_word = st.text_input('나를 한 단어로 표현한다면?', placeholder='예: 열정, 차분함, 창의')
        likes_input = st.text_input('내가 좋아하는 것 2가지 (콤마로 구분)', placeholder='예: 초코, 고양이, 꽃')

        submitted = st.form_submit_button('별명 생성하기 😎')
        st.markdown('</div>', unsafe_allow_html=True)

    def parse_likes(likes_raw: str) -> List[str]:
        items = [x.strip() for x in likes_raw.split(',') if x.strip()]
        return items[:5]

    def sanitize_word(w: str) -> str:
        return w.strip()

    def generate_nicknames(key_word: str, likes: List[str], n: int = 6) -> List[str]:
        kw = sanitize_word(key_word) if key_word else ''
        likes = [sanitize_word(l) for l in likes]

        candidates = []

        # Basic combos
        for like in likes:
            if kw:
                candidates.append(f'{like} 덕후 {kw} 😜')
                candidates.append(f'{kw} of {like} 🌟')
                candidates.append(f'{like}랑 {kw} 사이')
            else:
                candidates.append(f'{like} 덕후')

        # Korean-flavored playful templates
        if kw:
            candidates += [
                f'{kw}요정 🧚',
                f'작은{kw} (Large Mood) 🎉',
                f'{kw}짱! 😎',
                f'{kw}님✦',
                f'{kw}♡{likes[0] if likes else "취향"}',
            ]

        # Alliteration & shorten
        if kw and likes:
            first_like = likes[0]
            # make short mash
            mash = (first_like[:3] + kw[:3]).strip()
            candidates.append(f'{mash}★')

        # Funny roles
        candidates += [
            '행복배달부 🎁',
            '센스충 ⚡',
            '별빛수집가 ✨',
        ]

        # Deduplicate while keeping order
        seen = set()
        out = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                out.append(c)

        # Shuffle a bit but keep deterministic-ish order
        random.shuffle(out)
        return out[:n]

    # Display results
    if submitted:
        key_word = key_word.strip()
        likes = parse_likes(likes_input)

        # Store variables (as requested)
        st.session_state['key_word'] = key_word
        st.session_state['likes'] = likes

        # Generate
        nicknames = generate_nicknames(key_word, likes, n=8)

        # Result card
        st.markdown('<br/>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown(f'<div style="display:flex; justify-content:space-between; align-items:center">'
                    f'<div><div class="muted">추천 별명</div>'
                    f'<div class="result">{nicknames[0] if nicknames else "아직 아무것도..."}</div></div>'
                    f'<div><span class="small-pill">{" • ".join(likes) if likes else "취향 미입력"}</span></div></div>', unsafe_allow_html=True)

        # Show variations
        st.markdown('<hr/>', unsafe_allow_html=True)
        cols = st.columns(2)
        for i, nick in enumerate(nicknames):
            with cols[i % 2]:
                st.markdown(f'<div style="padding:8px; border-radius:12px; background:#fff7fb; margin-bottom:8px; font-weight:700; color:#7a2b4b">{nick}</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Advanced: 더 많은 템플릿 제시
        more = st.expander('템플릿 더 보기 (유머/센스)')
        with more:
            extra_templates = [
                '취향 저격러 💘',
                '감성 제조기 🎨',
                '오늘도 센스충 🌈',
                '작은 기적 담당자 ✨',
                '비밀의 취향수집가 🗝️',
                '무드 메이커 🎶',
            ]
            for t in extra_templates:
                st.write('•', t)

        st.markdown('<div style="margin-top:10px; color:#6b6b6b">원하시면 별명 조합 규칙을 더 늘리거나, 랜덤성/언어 스타일을 조절해드릴게요.</div>', unsafe_allow_html=True)

    else:
        # Show a friendly prompt card
        st.markdown('<br/>', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="font-weight:700; font-size:18px;">시작하기 전에</div>', unsafe_allow_html=True)
        st.markdown('<div class="muted">간단한 키워드와 좋아하는 것을 입력하면 유머러스한 별명과 감성 문구를 추천해드립니다. 두 가지를 콤마로 구분해서 입력하세요.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Footer small note
    st.markdown('<div style="text-align:center; margin-top:14px; color:#9a9a9a">Made with ❤️ by 제목학원</div>', unsafe_allow_html=True)
