import datetime as dt

import requests
import streamlit as st

st.set_page_config(page_title="Date Quest", page_icon="💜", layout="centered")

# ---------- น้องมังกรพิกเซล (ออกแบบใหม่) ----------
DRAGON = [
    "....y.....y.....",
    "...oyo...oyo....",
    "..oppoooooppo...",
    ".oppppppppppo...",
    ".ophepppphepo...",
    ".opeeppppeepo...",
    ".ocppppppppco...",
    "..opppoopppo....",
    "ww.oppppppo.ww..",
    "wwwobbbbbbowww..",
    ".wwobbbbbbowwpp.",
    "..opbbbbbbpo.pp.",
    "..oppppppppopo..",
    "..opo.oo.opo....",
    "..ooo....ooo....",
]
COLORS = {
    "o": "#3b2a4d", "p": "#b8a4e3", "b": "#fde8c8", "w": "#f7a8c4",
    "e": "#3b2a4d", "h": "#ffffff", "c": "#ff8fab", "y": "#ffd166",
}


def dragon_svg(px: int = 10, flip: bool = False) -> str:
    rects = []
    w = len(DRAGON[0])
    for y, row in enumerate(DRAGON):
        for x, ch in enumerate(row):
            if ch in COLORS:
                xx = (w - 1 - x) if flip else x
                rects.append(
                    f'<rect x="{xx*px}" y="{y*px}" width="{px}" height="{px}" fill="{COLORS[ch]}"/>'
                )
    return (
        f'<svg class="dragon" width="{w*px}" height="{len(DRAGON)*px}" '
        f'shape-rendering="crispEdges" xmlns="http://www.w3.org/2000/svg">{"".join(rects)}</svg>'
    )


# ---------- สไตล์ ----------
st.markdown(
    """
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Mali:wght@500;700&display=swap" rel="stylesheet">
<style>
.stApp { background: #1e1633;
  background-image: radial-gradient(#ffffff22 1px, transparent 1px);
  background-size: 18px 18px; }
html, body, [class*="css"], .stMarkdown, label, p { font-family: 'Mali', sans-serif !important; color: #f5ecff; }
h1, h2, h3, .pixel { font-family: 'Press Start 2P', monospace !important; color: #ffd166 !important;
  text-shadow: 3px 3px 0 #3b2a4d; line-height: 1.6; }
.box { background: #2d2250; border: 4px solid #b8a4e3; box-shadow: 6px 6px 0 #0d0918;
  padding: 18px; margin: 12px 0; image-rendering: pixelated; }
.center { text-align: center; }
.dragon { animation: bob 1.2s steps(2) infinite; }
@keyframes bob { 50% { transform: translateY(-6px); } }
.stButton > button { font-family: 'Press Start 2P', monospace !important; font-size: 12px;
  border: 4px solid #3b2a4d !important; border-radius: 0 !important; box-shadow: 4px 4px 0 #0d0918;
  background: #f7a8c4 !important; color: #3b2a4d !important; }
.stButton button p, .stFormSubmitButton button p { color: #3b2a4d !important; font-family: 'Mali', sans-serif !important; font-weight: 700; }
.stFormSubmitButton > button { border: 4px solid #3b2a4d !important; border-radius: 0 !important;
  box-shadow: 4px 4px 0 #0d0918; background: #ffd166 !important; }
[data-testid="stForm"] { background: #2d2250; border: 4px solid #b8a4e3 !important; border-radius: 0; box-shadow: 6px 6px 0 #0d0918; }
.stButton > button:active { transform: translate(4px,4px); box-shadow: none; }
.st-key-no_btn button { background: #8a7fa8 !important; }
.hearts { font-size: 28px; letter-spacing: 6px; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- state ----------
ss = st.session_state
ss.setdefault("step", "ask")
ss.setdefault("no_count", 0)

NO_TEXTS = [
    "ไม่ไปอะ", "แน่ใจหรอ?", "คิดดีๆ นะ", "น้องมังกรร้องไห้แล้ว 🥺",
    "ขอร้องงง", "กดไม่ได้หรอก~", "ไปเถอะนะ 💜",
]

st.markdown("<h1 class='center'>DATE QUEST</h1>", unsafe_allow_html=True)

# ---------- ขั้นที่ 1: ชวน ----------
if ss.step == "ask":
    sad = ss.no_count > 0
    st.markdown(
        f"<div class='center'>{dragon_svg(12, flip=sad)}</div>"
        f"<div class='box center'><p class='pixel' style='font-size:14px'>"
        f"{'ไปเดทกับเค้านะ...' if sad else 'ไปเดทกันไหม?'}</p>"
        f"<p>{'🥺' * min(ss.no_count, 5)}</p></div>",
        unsafe_allow_html=True,
    )
    yes_size = 12 + ss.no_count * 5
    st.markdown(
        f"<style>.st-key-yes_btn button {{ font-size:{yes_size}px !important; "
        f"padding:{8 + ss.no_count*4}px 20px !important; background:#ffd166 !important; }}</style>",
        unsafe_allow_html=True,
    )
    c1, c2 = st.columns(2)
    with c1:
        if st.button("ไปสิ! 💜", key="yes_btn", use_container_width=True):
            ss.step = "form"
            st.rerun()
    with c2:
        if ss.no_count < len(NO_TEXTS):
            if st.button(NO_TEXTS[ss.no_count], key="no_btn", use_container_width=True):
                ss.no_count += 1
                st.rerun()

# ---------- ขั้นที่ 2: เลือกวันเดท ----------
elif ss.step == "form":
    st.markdown(
        f"<div class='center'>{dragon_svg(8)}</div>"
        "<div class='box center'><p class='pixel' style='font-size:12px'>เย้! เลือกวันเดทเลย</p>"
        "<p class='hearts'>💜💗💜</p></div>",
        unsafe_allow_html=True,
    )
    with st.form("date_form"):
        name = st.text_input("ชื่อของเธอ")
        today = dt.date.today()
        date = st.date_input("วันไหนดี?", value=today + dt.timedelta(days=1), min_value=today)
        time = st.time_input("กี่โมง?", value=dt.time(18, 0), step=1800)
        activities = st.multiselect(
            "อยากทำอะไรบ้าง?",
            ["🍜 กินข้าว", "🍰 คาเฟ่ของหวาน", "🎬 ดูหนัง", "🎮 เล่นเกม",
             "🌅 เดินเล่นดูพระอาทิตย์ตก", "🛍️ เดินห้าง", "🎤 ร้องคาราโอเกะ"],
            default=["🍜 กินข้าว"],
        )
        mood = st.select_slider("ตื่นเต้นแค่ไหน?", ["นิดนึง", "พอประมาณ", "มาก", "มากกกก", "ใจจะวาย 💥"], value="มาก")
        note = st.text_area("ฝากอะไรถึงเค้าไหม?", max_chars=300)
        submitted = st.form_submit_button("ยืนยันการจอง ✨", use_container_width=True)

    if submitted:
        if not name.strip():
            st.warning("ใส่ชื่อก่อนน้า")
        elif not activities:
            st.warning("เลือกกิจกรรมอย่างน้อย 1 อย่างนะ")
        else:
            ss.booking = dict(name=name.strip(), date=date, time=time,
                              activities=activities, mood=mood, note=note.strip())
            ss.step = "send"
            st.rerun()

# ---------- ขั้นที่ 3: ส่งเข้า Discord ----------
elif ss.step == "send":
    b = ss.booking
    when = f"{b['date'].strftime('%d/%m/%Y')} เวลา {b['time'].strftime('%H:%M')} น."
    try:
        webhook = st.secrets.get("DISCORD_WEBHOOK_URL", "")
        user_id = st.secrets.get("DISCORD_USER_ID", "")
    except Exception:
        webhook, user_id = "", ""

    if not ss.get("sent"):
        if not webhook:
            st.error("ยังไม่ได้ตั้งค่า DISCORD_WEBHOOK_URL ใน Secrets")
        else:
            payload = {
                "content": (f"<@{user_id}> " if user_id else "") + "💌 มีคนจองเดทแล้ว!",
                "embeds": [{
                    "title": f"💜 {b['name']} ตอบตกลงไปเดท!",
                    "color": 0xB8A4E3,
                    "fields": [
                        {"name": "📅 วันเวลา", "value": when, "inline": False},
                        {"name": "🎯 กิจกรรม", "value": "\n".join(b["activities"]), "inline": True},
                        {"name": "💓 ความตื่นเต้น", "value": b["mood"], "inline": True},
                        {"name": "🙅 กดปฏิเสธไปก่อน", "value": f"{ss.no_count} ครั้ง", "inline": True},
                    ] + ([{"name": "💬 ข้อความ", "value": b["note"], "inline": False}] if b["note"] else []),
                    "footer": {"text": "Date Quest"},
                }],
            }
            try:
                r = requests.post(webhook, json=payload, timeout=10)
                r.raise_for_status()
                ss.sent = True
                st.balloons()
            except Exception as e:
                st.error(f"ส่งแจ้งเตือนไม่สำเร็จ: {e}")

    if ss.get("sent"):
        acts = " · ".join(b["activities"])
        st.markdown(
            f"<div class='center'>{dragon_svg(12)}</div>"
            f"<div class='box center'><p class='pixel' style='font-size:14px'>จองสำเร็จ!</p>"
            f"<p>เจอกัน <b>{when}</b></p><p>{acts}</p>"
            f"<p class='hearts'>💜💗💜💗💜</p><p>ส่งข่าวให้เค้าแล้ว รอเจอกันน้า~</p></div>",
            unsafe_allow_html=True,
        )
    if st.button("↺ เริ่มใหม่"):
        for k in ["step", "no_count", "booking", "sent"]:
            ss.pop(k, None)
        st.rerun()
