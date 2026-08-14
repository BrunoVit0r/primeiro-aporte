from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

SRC_DIR = Path(__file__).resolve().parent
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from agent import answer_question, build_quiz, explain_another_way, find_topic, get_related_topics, show_example
from config import APP_NAME, DATA_DIR, DISCLAIMER, TAGLINE
from knowledge import load_knowledge


st.set_page_config(page_title=APP_NAME, page_icon="📚", layout="centered")
st.markdown("""
<style>
:root { font-size:18px; --red:#cc092f; --red-dark:#990022; --red-soft:#fff1f3; --black:#141414; --gray:#52525b; --line:#e4e4e7; --white:#fff; }
html,body,[data-testid="stAppViewContainer"] { color:var(--black); background:var(--white); }
[data-testid="stHeader"] { background:transparent; }
[data-testid="stDecoration"] { background:var(--red); }
.block-container { max-width:1040px; padding-top:1.3rem; padding-bottom:2.5rem; }
.bank-header { overflow:hidden; margin-bottom:1.7rem; border:1px solid #b8082e; border-radius:20px; color:#fff; background:linear-gradient(120deg,#8f001f 0%,var(--red) 58%,#e10b40 100%); box-shadow:0 14px 34px rgba(153,0,34,.18); }
.bank-header__utility { display:flex; justify-content:space-between; padding:.65rem 1.35rem; color:#f5f5f5; background:rgba(15,15,15,.94); font-size:.82rem; letter-spacing:.02em; }
.bank-header__content { display:flex; align-items:center; gap:1.1rem; padding:1.6rem 1.65rem 1.75rem; }
.brand-mark { display:grid; flex:0 0 3.5rem; width:3.5rem; height:3.5rem; place-items:center; border:2px solid rgba(255,255,255,.8); border-radius:16px; color:var(--red); background:#fff; font-size:1.15rem; font-weight:800; }
.bank-header h1 { margin:0; color:#fff; font-size:2.25rem; line-height:1.1; letter-spacing:-.03em; }
.bank-header p { margin:.55rem 0 0; color:#fff7f8; font-size:1.08rem; line-height:1.5; }
.section-eyebrow { margin:0 0 .3rem; color:var(--red-dark); font-size:.84rem; font-weight:800; letter-spacing:.08em; text-transform:uppercase; }
.journey-eyebrow { margin-top:2rem; }
.section-heading { margin:0; color:var(--black); font-size:1.65rem; line-height:1.25; }
.section-intro { margin:.45rem 0 1.1rem; color:var(--gray); font-size:1rem; line-height:1.6; }
.progress-card { margin-bottom:.8rem; padding:1rem 1.15rem; border:1px solid #efc1cb; border-radius:14px; background:var(--red-soft); }
.progress-card strong { color:var(--red-dark); }
[data-testid="stProgress"],
[data-testid="stProgress"] > div { background:var(--white); }
[data-testid="stProgress"] [role="progressbar"] {
    overflow:hidden;
    box-sizing:border-box;
    border:0;
    border-radius:999px;
    background:var(--red)!important;
}
[data-testid="stProgress"] [role="progressbar"] > div { background:var(--red)!important; }
[data-testid="stProgressBar"] > div {
    background-color:var(--black)!important;
}
[data-testid="stVerticalBlockBorderWrapper"] { border-color:var(--line)!important; border-radius:18px!important; background:#fafafa; box-shadow:0 8px 24px rgba(20,20,20,.06); }
.track-card { min-height:9.5rem; padding:1rem; border-top:4px solid var(--red); border-radius:12px 12px 4px 4px; background:#fff; }
.track-card__icon { font-size:1.45rem; }
.track-card h3 { margin:.5rem 0 .4rem; color:var(--black); font-size:1.1rem; line-height:1.3; }
.track-card p { margin:0; color:var(--gray); font-size:.92rem; line-height:1.55; }
[data-testid="stMarkdownContainer"] p,[data-testid="stMarkdownContainer"] li { font-size:1.04rem; line-height:1.7; }
[data-testid="stChatMessage"] { padding:1rem 1.15rem; margin-bottom:.7rem; border:1px solid var(--line); border-radius:14px; background:#fafafa; }
[data-testid="stChatMessage"] p,[data-testid="stChatMessage"] li { font-size:1.08rem; line-height:1.75; }
[data-testid="stChatMessage"] h3 { color:var(--black); font-size:1.4rem; }
.stButton button { min-height:3.25rem; padding:.7rem .9rem; border:1px solid #c8c8cc; border-radius:10px; color:var(--black); background:#fff; font-size:.96rem; font-weight:700; line-height:1.3; white-space:normal; }
.stButton button:hover { border-color:var(--red); color:var(--red-dark); background:var(--red-soft); }
.stButton button[kind="primary"],[data-testid="stFormSubmitButton"] button { border-color:var(--red); color:#fff; background:var(--red); }
.stButton button[kind="primary"]:hover,[data-testid="stFormSubmitButton"] button:hover { border-color:var(--red-dark); color:#fff; background:var(--red-dark); }
.stButton button[kind="tertiary"] { min-height:2.5rem; padding:.3rem; border:0; color:var(--gray); background:transparent; font-size:.9rem; font-weight:600; text-decoration:underline; text-decoration-color:#d1d5db; text-underline-offset:4px; }
.stButton button:focus-visible,input:focus-visible { outline:3px solid var(--black); outline-offset:3px; }
[data-testid="stForm"] { margin-top:1rem; padding:1rem; border:2px solid var(--black); border-radius:16px; background:#fff; box-shadow:0 8px 22px rgba(20,20,20,.08); }
[data-testid="stTextInput"] input { min-height:3.4rem; padding:.8rem .9rem; border:1px solid #9ca3af; border-radius:10px; color:var(--black); font-size:1.05rem; }
.consult-label { margin:1.5rem 0 .45rem; color:#71717a; font-size:.82rem; font-weight:700; letter-spacing:.05em; text-transform:uppercase; }
.footer-note { margin-top:1.5rem; padding-top:1rem; border-top:1px solid var(--line); color:#71717a; font-size:.84rem; line-height:1.5; text-align:center; }
@media(max-width:760px) { :root{font-size:17px}.block-container{padding:.8rem .85rem 2rem}.bank-header__utility{align-items:flex-start;gap:.3rem;flex-direction:column}.bank-header__content{align-items:flex-start;padding:1.3rem}.bank-header h1{font-size:1.85rem}.track-card{min-height:auto}[data-testid="stHorizontalBlock"]{flex-direction:column;gap:.55rem}[data-testid="column"]{width:100%!important;flex:1 1 100%!important} }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def get_topics():
    return load_knowledge(DATA_DIR)


topics = get_topics()
topics_by_id = {topic["id"]: topic for topic in topics}
if "learned_topics" not in st.session_state:
    st.session_state.learned_topics = []
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant","content":"Olá! Sou seu guia de aprendizagem. Escolha uma trilha ou escreva o que deseja entender sobre investimentos."}]

st.markdown(f"""
<header class="bank-header">
  <div class="bank-header__utility"><span>Educação financeira para começar com segurança</span><span>Projeto educacional • não oficial</span></div>
  <div class="bank-header__content"><div class="brand-mark" aria-hidden="true">PA</div><div><h1>{APP_NAME}</h1><p><strong>{TAGLINE}</strong> Conhecimento claro para decisões mais conscientes.</p></div></div>
</header>
""", unsafe_allow_html=True)

learned_count = len(st.session_state.learned_topics)
st.markdown(f'<div class="progress-card"><strong>Seu progresso:</strong> {learned_count} de {len(topics)} conceitos explorados</div>', unsafe_allow_html=True)
st.progress(learned_count / len(topics))

tracks = [
    ("🌱","Primeiros passos","Investimento, risco, liquidez e reserva de emergência.","O que é investimento?"),
    ("🏦","Entenda a renda fixa","Entenda sobre CDB, Tesouro Direto, LCI e LCA.","O que é CDB?"),
    ("📈","Conheça a renda variável","Ações, fundos imobiliários e ETFs.","O que são fundos imobiliários?"),
]
st.markdown('<p class="section-eyebrow journey-eyebrow">Jornada de conhecimento</p><h2 class="section-heading">Trilhas de aprendizagem</h2><p class="section-intro">Escolha um caminho e avance no seu ritmo. Cada trilha começa com um conceito essencial.</p>', unsafe_allow_html=True)
with st.container(border=True):
    track_columns = st.columns(3, gap="medium")
    for column,(icon,name,description,question) in zip(track_columns,tracks):
        with column:
            st.markdown(f'<div class="track-card"><span class="track-card__icon">{icon}</span><h3>{name}</h3><p>{description}</p></div>', unsafe_allow_html=True)
            if st.button(f"{name}", key=f"track-{name}", type="primary", width="stretch"):
                st.session_state["pending_question"] = question

st.markdown('<p class="consult-label">Consultas rápidas</p>', unsafe_allow_html=True)
quick_questions = {"Investimento":"O que é investimento?","CDB":"O que é CDB?","Fundos imobiliários":"O que são fundos imobiliários?","Tesouro Direto":"O que é Tesouro Direto?"}
quick_columns = st.columns(4)
for column,(label,question) in zip(quick_columns,quick_questions.items()):
    if column.button(label,key=f"quick-{label}",type="tertiary",width="stretch"):
        st.session_state["pending_question"] = question

st.markdown('<p class="section-eyebrow" style="margin-top:1.8rem">Espaço de consulta</p><h2 class="section-heading">Converse e aprenda</h2><p class="section-intro">Veja as explicações e continue a conversa sem sair desta página.</p>', unsafe_allow_html=True)
latest_question_index = max(
    (index for index,message in enumerate(st.session_state.messages) if message["role"] == "user"),
    default=-1,
)
latest_response_index = len(st.session_state.messages) - 1
for message_index,message in enumerate(st.session_state.messages):
    if message_index == latest_question_index:
        st.markdown('<div id="latest-question"></div>', unsafe_allow_html=True)
    if message_index == latest_response_index and message["role"] == "assistant":
        st.markdown('<div id="latest-response"></div>', unsafe_allow_html=True)
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

last_topic = topics_by_id.get(st.session_state.get("last_topic_id", ""))
if last_topic:
    st.markdown("**Próximos conceitos sugeridos**")
    related_columns = st.columns(3)
    for column,related in zip(related_columns,get_related_topics(last_topic,topics)):
        if column.button(related["titulo"],key=f"related-{related['id']}",width="stretch"):
            st.session_state["pending_question"] = f"O que é {related['titulo']}?"
    action_columns = st.columns(3)
    if action_columns[0].button("💬 Explique de outro jeito",width="stretch"):
        st.session_state.messages.append({"role":"assistant","content":explain_another_way(last_topic)}); st.session_state["scroll_target"] = "latest-response"; st.rerun()
    if action_columns[1].button("🔎 Ver um exemplo",width="stretch"):
        st.session_state.messages.append({"role":"assistant","content":show_example(last_topic)}); st.session_state["scroll_target"] = "latest-response"; st.rerun()
    if action_columns[2].button("✅ Testar o que aprendi",width="stretch"):
        st.session_state["quiz_topic_id"] = last_topic["id"]
        st.session_state["scroll_target"] = "learning-quiz"

quiz_topic = topics_by_id.get(st.session_state.get("quiz_topic_id", ""))
if quiz_topic:
    quiz = build_quiz(quiz_topic, topics)
    st.markdown('<div id="learning-quiz"></div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### Verificação rápida")
        choice = st.radio(quiz["question"],quiz["options"],index=None,key=f"quiz-choice-{quiz_topic['id']}")
        if st.button("Conferir resposta",type="primary"):
            if choice is None: st.warning("Escolha uma alternativa antes de conferir.")
            elif choice == quiz["correct"]: st.success("Muito bem! Você identificou o conceito corretamente.")
            else: st.error("Ainda não. Leia a explicação e tente novamente.")
            if choice is not None: st.info(quiz["explanation"])

scroll_target = st.session_state.pop("scroll_target",None)
if scroll_target:
    components.html(f"""
    <script>
    window.setTimeout(() => {{
        const target = window.parent.document.getElementById("{scroll_target}");
        if (target) target.scrollIntoView({{ behavior: "smooth", block: "start" }});
    }}, 180);
    </script>
    """, height=0)

with st.form("question-form",clear_on_submit=True,border=True):
    st.markdown("**O que você quer aprender agora?**")
    typed_question = st.text_input("Pergunta sobre investimentos",placeholder="Ex.: O que é renda fixa?",label_visibility="collapsed")
    submitted = st.form_submit_button("Enviar pergunta",type="primary",width="stretch")

question = typed_question.strip() if submitted else ""
if st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")
if question:
    matched_topic = find_topic(question,topics)
    st.session_state.messages.extend([{"role":"user","content":question},{"role":"assistant","content":answer_question(question,topics)}])
    if matched_topic:
        learned = list(st.session_state.learned_topics)
        if matched_topic["id"] not in learned: learned.append(matched_topic["id"])
        st.session_state.learned_topics = learned
        st.session_state["last_topic_id"] = matched_topic["id"]
        st.session_state.pop("quiz_topic_id",None)
    st.session_state["scroll_target"] = "latest-question"
    st.rerun()

st.markdown(f'<footer class="footer-note">Base de conhecimento local • {DISCLAIMER}</footer>', unsafe_allow_html=True)
