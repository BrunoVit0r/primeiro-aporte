from pathlib import Path

from streamlit.testing.v1 import AppTest


ROOT = Path(__file__).resolve().parents[1]


def load_app():
    return AppTest.from_file(str(ROOT / "src" / "app.py"), default_timeout=10).run()


def test_app_starts_as_simple_local_consultation():
    app = load_app()
    assert not app.exception
    assert len(app.chat_input) == 0
    assert len(app.text_input) == 1
    assert len(app.get("form")) == 1
    assert len(app.button) == 8
    assert len(app.selectbox) == 0
    assert len(app.metric) == 0
    content = "\n".join(item.value for item in app.markdown)
    assert "Primeiro Aporte" in content
    assert "Aprenda antes de investir" in content
    assert "Seu progresso:" in content
    assert "st.progress(" in (ROOT / "src" / "app.py").read_text(encoding="utf-8")
    assert "bank-header" in content


def test_app_has_no_external_integration_controls():
    app = load_app()
    assert not app.exception
    assert len(app.toggle) == 0
    assert "OpenAI" not in "\n".join(item.value for item in app.markdown)


def test_accessible_typography_and_focus_styles_are_present():
    source = (ROOT / "src" / "app.py").read_text(encoding="utf-8")
    assert ':root { font-size:18px;' in source
    assert 'min-height:3.25rem;' in source
    assert 'font-size:1.08rem;' in source
    assert ':focus-visible' in source
    assert '@media(max-width:760px)' in source


def test_learning_tracks_are_available():
    app = load_app()
    assert len([button for button in app.button if button.key and button.key.startswith("track-")]) == 3
    content = "\n".join(item.value for item in app.markdown)
    assert "Primeiros passos" in content
    assert "Entenda a renda fixa" in content
    assert "Conheça a renda variável" in content


def test_consultation_updates_progress_and_shows_learning_actions():
    app = load_app()
    next(button for button in app.button if button.label == "CDB").click().run()
    assert not app.exception
    content = "\n".join(item.value for item in app.markdown)
    labels = [button.label for button in app.button]
    assert "### CDB" in content
    assert app.session_state["learned_topics"] == ["produto-cdb"]
    assert "💬 Explique de outro jeito" in labels
    assert "🔎 Ver um exemplo" in labels
    assert "✅ Testar o que aprendi" in labels


def test_question_form_is_after_conversation_and_before_footer():
    source = (ROOT / "src" / "app.py").read_text(encoding="utf-8")
    messages_position = source.index("for message_index,message in enumerate(st.session_state.messages)")
    form_position = source.index('with st.form("question-form"')
    footer_position = source.index('<footer class="footer-note">')
    assert messages_position < form_position < footer_position


def test_visual_identity_uses_red_white_and_black_with_aligned_track_cards():
    source = (ROOT / "src" / "app.py").read_text(encoding="utf-8")
    assert "--red:#cc092f" in source
    assert "--black:#141414" in source
    assert "--white:#fff" in source
    assert ".track-card { min-height:9.5rem;" in source
    assert 'type="primary"' in source


def test_progress_uses_red_outline_and_progressive_fill():
    source = (ROOT / "src" / "app.py").read_text(encoding="utf-8")
    assert '[data-testid="stProgress"] > div { background:var(--white); }' in source
    assert '[data-testid="stProgress"] [role="progressbar"] {' in source
    assert 'background:var(--red)!important;' in source
    assert '[data-testid="stProgress"] [role="progressbar"] > div { background:var(--red)!important; }' in source
    assert '[data-testid="stProgressBar"] > div {' in source
    assert 'background-color:var(--black)!important;' in source
    assert 'Continue aprendendo no seu ritmo' not in source
    assert '.journey-eyebrow { margin-top:2rem; }' in source


def test_scroll_targets_match_each_user_action():
    source = (ROOT / "src" / "app.py").read_text(encoding="utf-8")
    assert 'id="latest-question"' in source
    assert 'id="latest-response"' in source
    assert 'id="learning-quiz"' in source
    assert 'message["role"] == "user"' in source
    assert 'st.session_state["scroll_target"] = "latest-question"' in source
    assert source.count('st.session_state["scroll_target"] = "latest-response"') == 2
    assert 'st.session_state["scroll_target"] = "learning-quiz"' in source
    assert 'document.getElementById("{scroll_target}")' in source
    assert 'scrollIntoView({{ behavior: "smooth", block: "start" }})' in source
