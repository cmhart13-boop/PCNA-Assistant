import html
from pathlib import Path
import streamlit as st

LOGO_PATH = Path(__file__).with_name("PCNA_Logo_PMS_FINAL_TM_Transparent.png")
st.set_page_config(page_title="PCNA Assistant", page_icon=str(LOGO_PATH), layout="centered", initial_sidebar_state="collapsed")

LOGO_URL = "https://raw.githubusercontent.com/cmhart13-boop/PCNA-Assistant/main/PCNA_Logo_PMS_FINAL_TM_Transparent.png?v=202608161613"
HERO = "https://assets.pcna.com/image/upload/f_auto,q_auto/Mkt_Dept/2026%20Jobs/2026-0810_Web_Messaging/0810_Web_PCNA_Hero_m.gif?v=202608161613"

st.markdown('''
<style>
:root{--navy:#052c64;--blue:#064b97;--ink:#09265a;--paper:#f7f9fc}
*{box-sizing:border-box}.stApp{background:var(--paper);color:var(--ink)}
[data-testid="stHeader"],#MainMenu,footer,[data-testid="stToolbar"],.stDeployButton{display:none!important}
[data-testid="stAppViewContainer"]>.main{padding:0!important}.block-container{padding:0 14px 104px!important;max-width:520px!important}
.top{height:88px;display:grid;grid-template-columns:52px minmax(0,1fr) 52px;align-items:center;padding:10px 8px 0}
.menu,.bell{font-size:30px;color:var(--navy);text-align:center}.brand-logo{display:block;width:min(220px,100%);height:48px;object-fit:contain;margin:auto}
.hero{height:195px;border-radius:16px;overflow:hidden;background:#062e63;position:relative;box-shadow:0 4px 14px #001e4933;margin:0 0 16px}.hero img{display:block;width:100%;height:100%;object-fit:cover}
.section-title{font-size:25px;font-weight:900;letter-spacing:-.7px;margin:0 0 13px 10px}.section-title:after{content:"";display:block;width:32px;border-bottom:3px solid #2ca4dc;padding-top:6px}
[data-testid="stVerticalBlock"]{gap:0!important}[data-testid="stHorizontalBlock"]{gap:12px!important;margin-bottom:12px}
.card{height:188px;background:#fff;border:1px solid #d8e7f5;border-radius:15px;padding:14px 13px;position:relative;overflow:hidden;box-shadow:0 3px 12px #0b5aa52a;cursor:pointer}.badge{height:34px;width:34px;border-radius:50%;display:grid;place-items:center;background:linear-gradient(145deg,#063f87,#001e53);color:white;font-size:21px}.card h3{font-size:18px;line-height:1.05;margin:13px 0 9px;font-weight:900;max-width:108px;letter-spacing:-.5px}.card p{font-size:11px;line-height:1.45;margin:0;max-width:106px}.art{position:absolute;right:-8px;top:23px;width:49%;height:148px;display:grid;place-items:center;font-size:64px;filter:drop-shadow(0 8px 7px #132b4c38)}.go{position:absolute;right:9px;bottom:8px;width:31px;height:31px;border-radius:50%;background:#064993;color:white;display:grid;place-items:center;font-size:23px;font-weight:300}
.bottom{position:fixed;z-index:999;left:50%;transform:translateX(-50%);bottom:max(8px,env(safe-area-inset-bottom));width:min(calc(100% - 28px),492px);height:72px;border-radius:38px;background:linear-gradient(110deg,#073870,#00448b);display:grid;grid-template-columns:repeat(5,1fr);color:#fff;box-shadow:0 7px 18px #001b4544}.nav{display:grid;place-items:center;align-content:center;font-size:10px;gap:4px}.nav b{font-size:23px;line-height:1}.nav.active:after{content:"";width:34px;border-bottom:3px solid white;border-radius:3px}
.mobile-note{display:none}@media(min-width:700px){.mobile-note{display:block;text-align:center;font-size:12px;color:#627087;padding:8px}.block-container{max-width:548px!important}}
button[kind="secondary"]{height:188px;position:absolute;opacity:0;z-index:4}
.workspace-title{font-size:29px;font-weight:900;color:var(--ink);margin:8px 0}.backlink{font-size:13px;color:#215b94}.hint{color:#65758d;font-size:13px;line-height:1.5}.stTextArea textarea{min-height:190px;border-radius:13px}.stButton button{background:#063d7d;color:white;border:0;border-radius:11px;font-weight:800;width:100%}
</style>
''', unsafe_allow_html=True)

if "view" not in st.session_state:
    st.session_state.view = "home"

def go(view):
    st.session_state.view = view

def nav():
    st.markdown('<div class="bottom"><div class="nav active"><b>⌂</b>Home</div><div class="nav"><b>▱</b>Projects</div><div class="nav"><b>◇</b>Products</div><div class="nav"><b>○</b>Messages</div><div class="nav"><b>♙</b>Account</div></div>', unsafe_allow_html=True)

def header():
    st.markdown(f'<div class="top"><div class="menu">☰</div><img class="brand-logo" src="{LOGO_URL}" alt="PCNA"><div class="bell">♧</div></div>', unsafe_allow_html=True)

if st.session_state.view == "home":
    header()
    st.markdown(f'<div class="hero"><img src="{HERO}" alt="PCNA"></div>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">What do you need?</h2>', unsafe_allow_html=True)
    cards = [
        ("✓", "Spec Sample<br>Order", "Tell Nova what you need and build the verified PCNA order.", "🎒", "spec"),
        ("◇", "Virtuals /<br>Designs", "Ask Nova for product, kit or packaging virtuals and keep them in Projects.", "💻", "virtual"),
        ("$", "Quote<br>Request", "Quote a verified PCNA product at the requested quantity.", "📊", "quote"),
        ("□", "Projects", "View and manage your saved projects, orders and virtuals in one place.", "📓", "projects"),
    ]
    cols = st.columns(2, gap="small")
    for i,(badge,title,copy,art,key) in enumerate(cards):
        with cols[i % 2]:
            st.markdown(f'<div class="card"><div class="badge">{badge}</div><h3>{title}</h3><p>{copy}</p><div class="art">{art}</div><div class="go">→</div></div>', unsafe_allow_html=True)
            st.button(title.replace("<br>", " "), key=f"open-{key}", on_click=go, args=(key,))
    nav()
else:
    labels = {"spec":"Spec Sample Order","virtual":"Virtuals / Designs","quote":"Quote Request","projects":"Projects"}
    header()
    st.button("← Back to Home", on_click=go, args=("home",))
    title = labels[st.session_state.view]
    st.markdown(f'<div class="workspace-title">{html.escape(title)}</div>', unsafe_allow_html=True)
    if st.session_state.view == "projects":
        st.info("Your completed requests will be saved here.")
    else:
        st.markdown('<p class="hint">Tell Nova exactly what you need. Include product, color, decoration, quantity and delivery details when applicable.</p>', unsafe_allow_html=True)
        request = st.text_area("Your request", placeholder="Describe the PCNA request…")
        customer = st.text_input("Customer or project name")
        if st.button(f"Create {title}"):
            if request.strip():
                st.success("Request captured. Connect the PCNA data bridge and OpenAI secret in Streamlit to generate the verified file.")
            else:
                st.warning("Describe what you need first.")
    nav()
