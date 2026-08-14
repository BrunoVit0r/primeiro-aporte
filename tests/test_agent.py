from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent import EDUCATIONAL_NOTICE, answer_question, build_quiz, explain_another_way, find_topic, get_related_topics, show_example
from knowledge import load_knowledge


@pytest.fixture(scope="module")
def topics():
    return load_knowledge(ROOT / "data")


@pytest.mark.parametrize("question,title,text", [
    ("O que é investimento?", "Investimento", "direcionar uma parte do dinheiro"),
    ("O que é CDB?", "CDB", "Certificado de Depósito Bancário"),
    ("O que são fundos imobiliários?", "Fundos Imobiliários", "reúnem recursos de vários investidores"),
    ("Pode explicar FIIs?", "Fundos Imobiliários", "cotas negociadas em bolsa"),
        ("Como funciona o Tesouro Direto?", "Tesouro Direto", "títulos emitidos pelo governo federal"),
        ("O que são juros sobre juros?", "Juros compostos", "rendimentos anteriores"),
        ("Qual é a diferença entre renda fixa e renda variável?", "Diferença entre renda fixa e renda variável", "regra usada para calcular"),
])
def test_answers_main_questions(topics, question, title, text):
    answer = answer_question(question, topics)
    assert f"### {title}" in answer
    assert text in answer
    assert "**Como funciona**" in answer
    assert "**Riscos e cuidados**" in answer
    assert EDUCATIONAL_NOTICE in answer


def test_matching_ignores_accents_and_case(topics):
    assert find_topic("EXPLIQUE FUNDOS IMOBILIARIOS", topics)["id"] == "produto-fii"


def test_longest_alias_wins(topics):
    assert find_topic("Qual é o risco de investimento?", topics)["id"] == "conceito-risco"


def test_unknown_question_does_not_invent_answer(topics):
    answer = answer_question("Qual é a cotação do dólar agora?", topics)
    assert "Ainda não encontrei esse assunto na minha base local" in answer


def test_base_has_complete_unique_topics(topics):
    required = {"id", "titulo", "aliases", "resumo", "explicacao", "como_funciona", "pontos_importantes", "riscos_cuidados", "exemplo"}
    ids = [topic["id"] for topic in topics]
    assert len(topics) >= 15
    assert len(ids) == len(set(ids))
    assert all(required <= set(topic) for topic in topics)


def test_learning_support_actions_use_local_topic(topics):
    topic = find_topic("O que é CDB?", topics)
    assert topic["resumo"] in explain_another_way(topic)
    assert topic["exemplo"] in show_example(topic)
    assert EDUCATIONAL_NOTICE in explain_another_way(topic)


def test_quiz_has_one_correct_answer(topics):
    topic = find_topic("O que são fundos imobiliários?", topics)
    quiz = build_quiz(topic, topics)
    assert len(quiz["options"]) == 4
    assert quiz["options"].count(quiz["correct"]) == 1
    assert quiz["explanation"] == topic["explicacao"]


def test_related_topics_are_unique_and_exclude_current_topic(topics):
    topic = find_topic("O que é investimento?", topics)
    related = get_related_topics(topic, topics)
    ids = [item["id"] for item in related]
    assert len(ids) == len(set(ids)) == 3
    assert topic["id"] not in ids
