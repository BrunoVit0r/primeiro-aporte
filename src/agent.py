from __future__ import annotations

import re
import unicodedata
from typing import Any


EDUCATIONAL_NOTICE = "Esta explicação é educacional e não constitui recomendação de investimento."


def normalize(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def find_topic(question: str, topics: list[dict[str, Any]]) -> dict[str, Any] | None:
    normalized_question = f" {normalize(question)} "
    matches: list[tuple[int, dict[str, Any]]] = []
    for topic in topics:
        aliases = [topic["titulo"], *topic.get("aliases", [])]
        for alias in aliases:
            normalized_alias = normalize(alias)
            if f" {normalized_alias} " in normalized_question:
                matches.append((len(normalized_alias), topic))
                break
    return max(matches, key=lambda item: item[0])[1] if matches else None


def related_topics(question: str, topics: list[dict[str, Any]], limit: int = 4) -> list[str]:
    words = {word for word in normalize(question).split() if len(word) > 3}
    ranked = []
    for topic in topics:
        searchable = normalize(" ".join([topic["titulo"], *topic.get("aliases", []), topic.get("resumo", "")]))
        score = sum(word in searchable for word in words)
        if score:
            ranked.append((score, topic["titulo"]))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    return [title for _, title in ranked[:limit]]


def answer_question(question: str, topics: list[dict[str, Any]]) -> str:
    topic = find_topic(question, topics)
    if topic is None:
        related = related_topics(question, topics)
        suggestions = related or [item["titulo"] for item in topics[:4]]
        options = "\n".join(f"- {title}" for title in suggestions)
        return (
            "Ainda não encontrei esse assunto na minha base local. Você pode reformular a pergunta ou consultar um destes tópicos:\n\n"
            f"{options}\n\n{EDUCATIONAL_NOTICE}"
        )

    points = "\n".join(f"- {item}" for item in topic["pontos_importantes"])
    risks = "\n".join(f"- {item}" for item in topic["riscos_cuidados"])
    return (
        f"### {topic['titulo']}\n\n"
        f"{topic['explicacao']}\n\n"
        f"**Como funciona**\n\n{topic['como_funciona']}\n\n"
        f"**Pontos importantes**\n\n{points}\n\n"
        f"**Riscos e cuidados**\n\n{risks}\n\n"
        f"**Exemplo simples**\n\n{topic['exemplo']}\n\n"
        f"{EDUCATIONAL_NOTICE}"
    )


def explain_another_way(topic: dict[str, Any]) -> str:
    return (
        f"### {topic['titulo']}, em outras palavras\n\n"
        f"**Resumo direto:** {topic['resumo']}\n\n"
        f"Pense assim: {topic['exemplo']}\n\n"
        "Se ainda não ficou claro, você pode escrever qual parte gerou dúvida.\n\n"
        f"{EDUCATIONAL_NOTICE}"
    )


def show_example(topic: dict[str, Any]) -> str:
    return (
        f"### Exemplo de {topic['titulo']}\n\n"
        f"{topic['exemplo']}\n\n"
        "O exemplo é apenas didático: valores, prazos e condições reais podem ser diferentes.\n\n"
        f"{EDUCATIONAL_NOTICE}"
    )


def build_quiz(topic: dict[str, Any], topics: list[dict[str, Any]]) -> dict[str, Any]:
    distractors = [item["resumo"] for item in topics if item["id"] != topic["id"]][:3]
    options = [topic["resumo"], *distractors]
    shift = sum(ord(char) for char in topic["id"]) % len(options)
    options = options[shift:] + options[:shift]
    return {
        "question": f"Qual alternativa descreve melhor: {topic['titulo']}?",
        "options": options,
        "correct": topic["resumo"],
        "explanation": topic["explicacao"],
    }


def get_related_topics(topic: dict[str, Any], topics: list[dict[str, Any]], limit: int = 3) -> list[dict[str, Any]]:
    relation_groups = {
        "conceito-investimento": ["conceito-risco", "conceito-liquidez", "conceito-diversificacao"],
        "produto-cdb": ["conceito-renda-fixa", "produto-lci-lca", "conceito-liquidez"],
        "produto-fii": ["conceito-renda-variavel", "produto-fundos-investimento", "conceito-risco"],
        "produto-tesouro-direto": ["conceito-renda-fixa", "conceito-liquidez", "conceito-risco"],
        "conceito-renda-fixa": ["produto-cdb", "produto-tesouro-direto", "produto-lci-lca"],
        "conceito-renda-variavel": ["produto-acoes", "produto-fii", "produto-etf"],
    }
    ids = relation_groups.get(topic["id"], [])
    by_id = {item["id"]: item for item in topics}
    related = [by_id[item_id] for item_id in ids if item_id in by_id]
    if len(related) < limit:
        related.extend(item for item in topics if item["id"] != topic["id"] and item not in related)
    return related[:limit]
