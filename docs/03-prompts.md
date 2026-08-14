# Prompts do Agente

## System Prompt
Esta versão não utiliza LLM nem envia prompts a serviços externos. Para manter o entregável previsto no desafio, as regras abaixo documentam o comportamento equivalente implementado deterministicamente em `src/agent.py`:

1. responder somente com informações presentes na base local;
2. identificar o tópico pelo título ou por sinônimos cadastrados;
3. explicar o conceito em linguagem simples;
4. apresentar funcionamento, pontos importantes, riscos e exemplo;
5. não recomendar compra ou venda;
6. não inventar taxas, cotações, produtos ou regras atuais;
7. informar claramente quando o assunto não estiver disponível;
8. sugerir tópicos existentes quando não houver correspondência;
9. finalizar com aviso de finalidade educacional.
10. permitir reformulação, exemplo destacado e verificação de aprendizagem sem buscar conteúdo externo;
11. recomendar conceitos relacionados para dar continuidade à trilha.

### Template de resposta local

```text
### {título}

{explicação}

Como funciona
{como_funciona}

Pontos importantes
- {ponto}

Riscos e cuidados
- {risco}

Exemplo simples
{exemplo}

Esta explicação é educacional e não constitui recomendação de investimento.
```

## Exemplos de interação

### Conceito geral
**Entrada:** “O que é investimento?”  
**Saída esperada:** explicar o uso do dinheiro no presente visando preservação ou retorno futuro, destacar risco, prazo e liquidez e apresentar exemplo simples.

### Produto de renda fixa
**Entrada:** “O que é CDB?”  
**Saída esperada:** explicar que é um título emitido por bancos, apresentar formas de remuneração, liquidez, tributação, risco de crédito e referência ao FGC sem tratá-lo como risco zero.

### Renda variável
**Entrada:** “O que são fundos imobiliários?”  
**Saída esperada:** explicar cotas, imóveis ou recebíveis, rendimentos variáveis, negociação em bolsa e riscos como vacância e oscilação.

### Comparação
**Entrada:** “Qual é a diferença entre renda fixa e renda variável?”  
**Saída esperada:** comparar previsibilidade da regra de remuneração, oscilação, horizonte e riscos, sem indicar qual classe o cliente deve escolher.

### Informação ausente
**Entrada:** “Qual é a cotação do dólar agora?”  
**Saída esperada:** informar que o assunto não está na base local e sugerir tópicos cadastrados, sem consultar a internet nem inventar um valor.

### Reforço de aprendizagem
**Ação:** “Explique de outro jeito”  
**Saída esperada:** apresentar o resumo e o exemplo do mesmo tópico com uma formulação mais direta.

### Verificação rápida
**Ação:** “Testar o que aprendi”  
**Saída esperada:** apresentar quatro descrições locais, validar a escolha e explicar o conceito novamente.

## Edge cases
- Variação de maiúsculas e acentos: normalizar antes da busca.
- Siglas como CDB, FII e ETF: mapear pelos aliases.
- Mais de um termo na pergunta: escolher a correspondência específica mais longa.
- Assunto desconhecido: usar fallback com sugestões locais.
- Base vazia ou inválida: interromper o carregamento com erro explícito.
- Pergunta sobre taxas atuais: não fornecer valor sem fonte oficial.
