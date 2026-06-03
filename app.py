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
        bar_color = "#9b59b6"
        name_size = "30px"
        party_size = "20px"
        votes_size = "42px"   # ✅ 득표수 제일 크게
        rate_size = "22px"    # ✅ 비율은 작게
        padding = "36px 40px"
        margin = "20px 0px"
        bar_height = "18px"
        name_prefix = "⭐ "
    else:
        bg = "#1e1e2e"
        border = "#3a3a5c"
        bar_color = "#5a5a8a"
        name_size = "13px"
        party_size = "11px"
        votes_size = "15px"
        rate_size = "11px"
        padding = "10px 16px"
        margin = "4px 0px"
        bar_height = "6px"
        name_prefix = ""

    st.markdown(f"""
        <div style='
            background:{bg};
            border:1.5px solid {border};
            border-radius:12px;
            padding:{padding};
            margin:{margin};
        '>
            <div style='display:flex; justify-content:space-between; align-items:center; margin-bottom:{"16px" if highlight else "8px"};'>
                <div>
                    <div style='font-size:{name_size}; font-weight:bold; color:#f0eaff;'>
                        {name_prefix}{cand["name"]}
                    </div>
                    <div style='font-size:{party_size}; color:#b39ddb; margin-top:4px;'>
                        {cand["party"]}
                    </div>
                </div>
                <div style='text-align:right;'>
                    <div style='font-size:{votes_size}; font-weight:bold; color:#ce93d8;'>
                        {cand["votes"]:,}표
                    </div>
                    <div style='font-size:{rate_size}; color:#b39ddb; margin-top:4px;'>
                        {cand["rate"]}%
                    </div>
                </div>
            </div>
            <div style='background:#2a2a4a; border-radius:6px; height:{bar_height};'>
                <div style='
                    background:{bar_color};
                    width:{min(cand["rate"], 100)}%;
                    height:{bar_height};
                    border-radius:6px;
                '></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

def main():
    st.markdown("<h1 style='text-align:center; color:#ce93d8;'>💜유지혜를 뽑은 사람들💜</h1>", unsafe_allow_html=True)

    data = load_data()

    if not data:
        st.error("data.json 파일이 없어요!")
        return

    st.markdown(f"<p style='text-align:center; color:#7e57c2; font-size:13px;'>🕐 {data['updated_at']} 기준 · 30초마다 자동 갱신</p>", unsafe_allow_html=True)
    st.divider()

    candidates = data["candidates"]

    # 여성의당 맨 앞으로
    womens = [c for c in candidates if "여성의당" in c["party"]]
    others = [c for c in candidates if "여성의당" not in c["party"]]
    sorted_candidates = womens + others

    for cand in sorted_candidates:
        is_womens = "여성의당" in cand["party"]
        render_candidate(cand, highlight=is_womens)

    time.sleep(30)
    st.rerun()

main()
