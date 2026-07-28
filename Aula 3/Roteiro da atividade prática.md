# Roteiro prático da Aula 3 - Sistema agêntico com validação de performance

## Objetivo da atividade

Nesta atividade, você e seu grupo vão desenvolver um sistema agêntico simples ou multiagente para uma temática definida em sala, usando os notebooks da Aula 3 como referência de padrão, não como solução pronta.

O objetivo é sair de "fazer o agente responder" e chegar em "fazer o sistema funcionar de forma confiável".

Ao final, seu grupo deve conseguir:
- estruturar um fluxo de agente ou multiagentes com uma tool externa ou uma fonte de dados controlada;
- definir um contrato de saída estruturado para permitir teste;
- implementar fallback, retry e revisão humana quando necessário;
- medir performance e confiabilidade com critérios observáveis;
- justificar, com dados, se o sistema está pronto para uso ou precisa de ajuste.

---

## Como fazer a atividade

### Organização
- trabalhe em grupos de 3 a 5 pessoas;
- escolha uma temática entre as opções abaixo;
- entregue um sistema próprio, usando a mesma estrutura mínima de avaliação.

### Como usar os notebooks da Aula 3
Use os notebooks 3A, 3B e 3C como referência de padrão:
- 3A inspira engenharia de contexto, acesso controlado e rastreabilidade;
- 3B inspira avaliação por propriedades e contratos;
- 3C inspira fallback, regressão, retry e revisão humana.

---

## Temáticas sugeridas

Escolha uma temática por grupo. O ideal é que cada tema tenha uma fonte externa simples, para reduzir o tempo gasto com preparação de dados.

1. Previsão do tempo por cidade
- tool externa: API pública de clima;
- ferramentas abertas: Open-Meteo, OpenWeatherMap e Nominatim para geocodificação da cidade;
- tarefa: informar previsão e recomendar uma ação prática.

2. Conversão cambial
- tool externa: API pública de câmbio;
- ferramentas abertas: Frankfurter, exchangerate.host ou outra API pública com cotação diária;
- tarefa: converter valores e explicar o resultado.

3. Consulta de política interna
- fonte: arquivos locais de política ou base documental;
- ferramentas abertas: pesquisa em documentos locais, indexação simples em JSON/CSV ou base de conhecimento interna;
- tarefa: responder se uma ação é permitida, restrita ou depende de revisão.

4. Resumo de ticket ou incidente
- fonte: JSON ou CSV com tickets simulados;
- ferramentas abertas: leitura de arquivos locais, busca textual simples e parsing estruturado de JSON/CSV;
- tarefa: resumir, classificar e priorizar o ticket.

5. Agente de roteiro de viagens
- ferramenta principal: API de busca na web para coletar contexto atual sobre destinos, atrações e recomendações;
- ferramentas complementares: geocodificação e pontos de interesse;
- ferramentas abertas: OpenStreetMap / Nominatim, OpenTripMap, Wikivoyage e APIs públicas de clima;
- tarefa: sugerir um roteiro simples por cidade, período e preferências do usuário.

6. Agente de compra e venda de ações
- ferramenta externa: API pública ou com plano gratuito de dados de mercado;
- ferramentas abertas: Alpha Vantage, Finnhub, Twelve Data ou Stooq, conforme disponibilidade e limite de uso;
- tarefa: analisar um ativo com base em preço, variação recente e sinais básicos, e sugerir uma ação com cautela.

---

## Estrutura mínima do sistema

Você pode seguir uma destas abordagens:

### Opção A - Agente único
Fluxo recomendado:
1. receber a entrada do usuário;
2. extrair intenção e parâmetros principais;
3. chamar a tool ou consultar a fonte de dados;
4. gerar uma resposta estruturada;
5. aplicar validação e decidir entre aceitar, tentar novamente ou escalar.

### Opção B - Multiagentes
Fluxo recomendado:
1. agente investigador coleta dados;
2. agente sintetizador organiza a resposta;
3. agente revisor verifica contrato, evidências e risco;
4. orquestrador decide a saída final.

### Regras mínimas
- o sistema precisa ter uma saída estruturada e testável;
- o sistema precisa registrar evidências ou eventos de execução;
- o sistema precisa ter uma regra explícita de fallback;
- o sistema precisa indicar quando há necessidade de revisão humana.

---

## Contrato de saída mínimo

Defina um schema de saída com campos como estes:

- `answer`: resposta final ao usuário;
- `confidence`: nota de confiança entre 0 e 1;
- `evidence_ids`: lista de evidências, IDs, fontes ou URLs;
- `fallback_acionado`: booleano;
- `needs_human_review`: booleano;
- `review_reason`: motivo da revisão humana, quando houver;
- `trace_summary`: resumo curto do que foi consultado ou executado.

O contrato pode ter campos adicionais, desde que permaneça simples e validável.

---

## Validação de performance e confiabilidade

Valide o sistema com pelo menos 3 cenários:

1. Cenário normal
- a entrada está completa;
- a tool responde corretamente;
- a saída deve ser aceita.

2. Cenário ambíguo
- a entrada tem pouca informação ou mais de uma interpretação;
- o sistema deve demonstrar robustez, pedir mais contexto ou reduzir confiança.

3. Cenário de falha
- a tool falha, a fonte não existe ou a informação é insuficiente;
- o sistema deve acionar fallback ou revisão humana.

### Métricas obrigatórias
Registre, no mínimo:
- taxa de aprovação dos casos;
- taxa de escalonamento para revisão humana;
- número médio de tentativas por caso;
- tempo médio de execução por caso;
- custo aproximado em tokens, quando disponível;
- observações sobre falhas recorrentes.

### Critérios de qualidade
O sistema será melhor quando:
- responde com consistência ao mesmo tipo de entrada;
- não inventa evidências ou dados ausentes;
- sinaliza corretamente situações de baixa confiança;
- reduz retrabalho com retry bem direcionado;
- evita loops infinitos e excesso de custo.

---

## Passo a passo

### 1. Defina a temática e o escopo
Escolha um problema simples e delimitado. Evite ampliar demais o escopo.

Exemplo de escopo bom:
- cidade única;
- horizonte curto;
- uma tool principal;
- contrato de saída fixo.

### 2. Especifique a saída esperada
Antes de codar, defina o schema final e os critérios de aprovação.

### 3. Implemente o fluxo principal
Construa a versão mínima que já funcione de ponta a ponta.

### 4. Adicione validação
Implemente checagem do contrato, evidências, confiança e regras de revisão.

### 5. Adicione fallback e retry
Se houver falha, o sistema deve tentar novamente com feedback verificável ou escalar.

### 6. Rode os cenários de teste
Execute os 3 cenários obrigatórios e registre os resultados.

### 7. Compare resultados
Monte uma tabela com métricas e conclusões.

---

## Rubrica de avaliação

Cada item pode ser avaliado em escala de 0 a 2.

### 1. Estrutura do sistema
- 0: fluxo incompleto ou confuso;
- 1: fluxo funcional, mas com pouca clareza;
- 2: fluxo simples, claro e bem organizado.

### 2. Contrato de saída
- 0: saída livre, difícil de testar;
- 1: saída parcialmente estruturada;
- 2: saída estruturada e validável.

### 3. Tratamento de falhas
- 0: falhas não tratadas;
- 1: existe fallback, mas sem consistência;
- 2: fallback e revisão humana funcionam de forma explícita.

### 4. Avaliação por propriedades
- 0: avaliação apenas textual;
- 1: avaliação parcial;
- 2: avaliação baseada em critérios objetivos e repetíveis.

### 5. Observabilidade
- 0: não há rastreio;
- 1: há rastreio parcial;
- 2: o sistema registra decisões, tool calls e sinais úteis para diagnóstico.

### 6. Conclusão técnica
- 0: não há análise final;
- 1: há análise, mas sem dados;
- 2: há recomendação sustentada por métricas.

---

## Entrega esperada

Ao final, seu grupo deve entregar:
- um notebook ou código funcional do sistema;
- um resumo curto da arquitetura;
- uma tabela com os cenários testados e métricas;
- uma conclusão sobre confiabilidade e custo;
- uma recomendação final: aceitar, ajustar ou escalar para revisão humana.

---

## Fechamento

O objetivo desta prática não é apenas construir um agente que responda. O objetivo é discutirmos como um sistema agêntico passa a ser útil quando também é possível controlá-lo, medir seu comportamento e decidir, com base em evidências, quando ele pode operar sozinho e quando deve escalar para revisão humana.