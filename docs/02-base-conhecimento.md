# Base de Conhecimento

## Fontes do protótipo

| Arquivo | Conteúdo | Uso pelo agente |
|---|---|---|
| `base_educacional.json` | Conceitos, produtos, sinônimos, riscos e exemplos | Fonte única para todas as respostas |
| `src/knowledge.py` | Carregamento e validação inicial | Disponibiliza os tópicos para consulta |
| `src/agent.py` | Normalização, busca e template | Localiza o assunto e monta a explicação |
| Estado da sessão | Progresso e último tópico | Personaliza a jornada sem armazenar dados pessoais |

## Estrutura de cada tópico

| Campo | Finalidade |
|---|---|
| `id` | Identificador único e estável |
| `titulo` | Nome exibido ao cliente |
| `aliases` | Sinônimos e formas alternativas de consulta |
| `resumo` | Síntese usada na busca por assuntos relacionados |
| `explicacao` | Definição do conceito em linguagem simples |
| `como_funciona` | Descrição prática do funcionamento |
| `pontos_importantes` | Aspectos essenciais para compreensão |
| `riscos_cuidados` | Alertas e limitações relevantes |
| `exemplo` | Situação didática simplificada |

## Conteúdo disponível

A base reúne 16 tópicos introdutórios:

1. Investimento;
2. CDB;
3. Fundos Imobiliários;
4. Renda fixa;
5. Renda variável;
6. Tesouro Direto;
7. Ações;
8. Fundos de investimento;
9. ETF;
10. LCI e LCA;
11. Diversificação;
12. Liquidez;
13. Risco de investimento;
14. Reserva de emergência;
15. Juros compostos;
16. Diferença entre renda fixa e renda variável.

## Estratégia de grounding
O agente não produz texto a partir de conhecimento externo. A pergunta é normalizada e comparada aos títulos e sinônimos cadastrados. Quando encontra o tópico, a resposta é montada diretamente com os campos do JSON. Quando não encontra, informa a limitação e sugere conteúdos existentes.

## Jornada de aprendizagem
Os mesmos campos locais alimentam quatro experiências: explicação completa, reformulação resumida, exemplo isolado e quiz de reconhecimento. Relações cadastradas no código conectam conceitos próximos. O progresso representa apenas os tópicos explorados na sessão atual e não identifica o usuário.

## Qualidade e governança
- Identificadores únicos para todos os tópicos.
- Estrutura obrigatória validada por testes automatizados.
- Conteúdo sem dados pessoais ou bancários.
- Revisão humana recomendada para inclusão ou alteração de conceitos.
- Informações temporais, taxas e regras vigentes devem ser confirmadas em fontes oficiais.
- Inclusão de riscos e cuidados em todos os assuntos.

## Suitability
O novo escopo não realiza suitability nem recomenda produtos. Como não coleta perfil, objetivo ou capacidade de risco, o agente limita-se a ensinar conceitos. A adequação de qualquer investimento deve ser avaliada separadamente pelo cliente com apoio de canais oficiais ou profissional habilitado.
