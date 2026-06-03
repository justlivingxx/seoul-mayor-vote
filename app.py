# app.py
import streamlit as st
import json
import time
from pathlib import Path

st.set_page_config(
    page_title="유지혜를 뽑은 사람들",
    page_icon="🗳️",
    layout="centered"
)

st.markdown("""
    <style>
        body { background-color: #1a0a2e; }
        .stApp { background-color: #1a0a2e; }
        h1, h2, h3, p, div { color: #f0eaff; }

        /* 모바일 여백 제거 */
        .block-container {
            padding-left: 12px !important;
            padding-right: 12px !important;
            padding-top: 20px !important;
            max-width: 100% !important;
        }

        /* 버튼/divider 색상 */
        hr { border-color: #3a2a5e; }
    </style>
""", unsafe_allow_html=True)

def load_data():
    path = Path("data.json")
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

def render_candidate(cand, highlight=False):
    if highlight:
        bg = "#3d1a6e"
        border = "#9b59b6"
        bar_color = "#ce93d8"
        name_prefix = "⭐ "
        name_size = "clamp(22px, 6vw, 38px)"
        party_size = "clamp(13px, 3.5vw, 18px)"
        votes_size = "clamp(26px, 8vw, 48px)"
        rate_size = "clamp(13px, 3.5vw, 18px)"
        padding = "clamp(16px, 4vw, 32px)"
        margin = "16px 0px"
        bar_height = "14px"
        radius = "16px"
    else:
        bg = "#1e1e2e"
        border = "#3a3a5c"
        bar_color = "#5a5a8a"
        name_prefix = ""
        name_size = "clamp(13px, 3.8vw, 17px)"
        party_size = "clamp(11px, 3vw, 14px)"
        votes_size = "clamp(15px, 4.5vw, 20px)"
        rate_size = "clamp(11px, 3vw, 14px)"
        padding = "clamp(10px, 3vw, 18px)"
        margin = "6px 0px"
        bar_height = "7px"
        radius = "12px"

    st.markdown(f"""
        <div style='
            background:{bg};
            border:1.5px solid {border};
            border-radius:{radius};
            padding:{padding};
            margin:{margin};
            box-sizing:border-box;
            width:100%;
        '>
            <div style='
                display:flex;
                justify-content:space-between;
                align-items:center;
                margin-bottom:12px;
                gap:8px;
            '>
                <div style='flex:1; min-width:0;'>
                    <div style='
                        font-size:{name_size};
                        font-weight:bold;
                        color:#f0eaff;
                        word-break:keep-all;
                        line-height:1.3;
                    '>
                        {name_prefix}{cand["name"]}
                    </div>
                    <div style='
                        font-size:{party_size};
                        color:#b39ddb;
                        margin-top:4px;
                        word-break:keep-all;
                    '>
                        {cand["party"]}
                    </div>
                </div>
                <div style='text-align:right; flex-shrink:0;'>
                    <div style='
                        font-size:{votes_size};
                        font-weight:bold;
                        color:#ce93d8;
                        white-space:nowrap;
                    '>
                        {cand["votes"]:,}표
                    </div>
                    <div style='
                        font-size:{rate_size};
                        color:#b39ddb;
                        margin-top:2px;
                    '>
                        {cand["rate"]}%
                    </div>
                </div>
            </div>

            <!-- 프로그레스 바 -->
            <div style='background:#2a2a4a; border-radius:99px; height:{bar_height}; overflow:hidden;'>
                <div style='
                    background:{bar_color};
                    width:{min(cand["rate"], 100)}%;
                    height:{bar_height};
                    border-radius:99px;
                    transition: width 0.5s ease;
                '></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    # 타이틀
    st.markdown("""
        <div style='text-align:center; padding: 8px 0 4px 0;'>
            <div style='font-size:clamp(20px, 6vw, 32px); font-weight:bold; color:#ce93d8; line-height:1.4;'>
                💜 유지혜를 뽑은 사람들 💜
            </div>
        </div>
    """, unsafe_allow_html=True)

    data = load_data()

    if not data:
        st.error("data.json 파일이 없어요!")
        return

    # 업데이트 시간
    st.markdown(f"""
        <div style='
            text-align:center;
            color:#7e57c2;
            font-size:clamp(11px, 3vw, 13px);
            margin: 6px 0 12px 0;
        '>
            🕐 {data['updated_at']} 기준 · 30초마다 자동 갱신
        </div>
    """, unsafe_allow_html=True)

    st.divider()

    candidates = data["candidates"]

    # 여성의당 맨 앞으로
    womens = [c for c in candidates if "여성의당" in c["party"]]
    others = [c for c in candidates if "여성의당" not in c["party"]]
    sorted_candidates = womens + others

    for cand in sorted_candidates:
        is_womens = "여성의당" in cand["party"]
        render_candidate(cand, highlight=is_womens)

    # 하단 여백
    st.markdown("<div style='height:40px'></div>", unsafe_allow_html=True)

    time.sleep(30)
    st.rerun()

main()
