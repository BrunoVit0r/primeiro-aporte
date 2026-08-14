# Avaliação e Métricas

## Métricas principais

| Métrica | Como medir | Meta do protótipo |
|---|---|---|
| Groundedness local | Respostas compostas somente com a base / total | 100% |
| Precisão de recuperação | Perguntas conhecidas associadas ao tópico correto / total | ≥ 95% |
| Cobertura estrutural | Tópicos com todos os campos obrigatórios / total | 100% |
| Segurança educacional | Respostas sem recomendação ou promessa de retorno / total | 100% |
| Transparência | Respostas desconhecidas que declaram limitação / total | 100% |
| Completude | Respostas com explicação, funcionamento, riscos e exemplo / total | 100% |
| Clareza | Avaliação humana de 1 a 5 | ≥ 4 |
| Disponibilidade local | Consultas previstas respondidas sem rede ou API | 100% |
| Engajamento educacional | Conceitos explorados e ações de reforço por sessão | Tendência crescente |
| Aprendizagem | Respostas corretas nas verificações rápidas / tentativas | ≥ 70% |

## Conjunto de testes
1. Pergunta “O que é investimento?”.
2. Pergunta “O que é CDB?”.
3. Pergunta “O que são fundos imobiliários?”.
4. Uso da sigla “FII”.
5. Pergunta sobre Tesouro Direto.
6. Pergunta sobre juros compostos.
7. Comparação entre renda fixa e renda variável.
8. Consulta sem acentos e em letras maiúsculas.
9. Pergunta sobre assunto ausente.
10. Validação de IDs únicos e campos obrigatórios.
11. Inicialização da interface Streamlit.
12. Ausência de seletor de perfil, métricas e controle de API.
13. Presença das três trilhas e do indicador de progresso.
14. Reformulação e exemplo baseados no tópico local.
15. Quiz com uma única alternativa correta.
16. Conceitos relacionados sem duplicidade.

## Resultado automatizado atual
- 21 testes automatizados, incluindo jornada educacional, progresso, acessibilidade e estrutura visual.
- Base JSON validada.
- Código Python compilado sem erros.
- Interface iniciada por `streamlit.testing.v1.AppTest`.
- Nenhuma importação de OpenAI, `python-dotenv` ou `pandas` no código ativo.

## Rubrica humana
Cada resposta recebe notas de 0 a 2 em:

1. fidelidade à base local;
2. clareza para público iniciante;
3. qualidade do exemplo;
4. apresentação de riscos e cuidados;
5. transparência sobre limitações.

Resultado máximo: 10. Recomenda-se aprovação humana com nota mínima 8.
