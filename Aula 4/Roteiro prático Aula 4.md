# Aula 4 - Roteiro pratico
## Do agente funcional para workflow operacional (API + Docker)

## Objetivo da atividade
Nesta atividade, cada grupo vai evoluir o que iniciou na Aula 3 (um dos temas escolhidos) para uma versao mais operacional:

- organizar o agente em um workflow explicito;
- expor o fluxo por API;
- preparar execucao padronizada (Docker) (opcional);
- opcionalmente, conectar um frontend simples para demonstracao.

A ideia e sair de um prototipo executado no notebook e chegar em algo que rode de forma reproduzivel.

---

## Contexto da continuidade (Aula 3 -> Aula 4)
Partimos do que ja existe da Aula 3:

- contrato de saida testavel;
- regra de fallback e revisao humana;
- cenarios de validacao (normal, ambiguo e falha);
- uma fonte externa (API) ou base local.

Na Aula 4, isso vira um fluxo mais "de produto":

1. fluxo modelado (workflow);
2. endpoint de servico (API);
3. empacotamento para execucao consistente (Docker).

---

## Entregaveis minimos
Ao final, cada grupo deve apresentar:

1. workflow do agente em codigo (ou diagrama + implementacao);
2. API rodando localmente com:
   - GET /health
   - POST endpoint principal do agente;
3. README com como executar;
4. demonstracao ponta a ponta.

Entregavel opcional (bonus):

- frontend Streamlit em modo chat consumindo a API.

---

## Guia pratico (passo a passo)

### Passo 1 - Fixar contrato
Checklist:

- resposta final em campo claro (answer);
- confiança (0 a 1);
- evidencias/fontes;
- flags de fallback e revisao humana;
- resumo de rastreabilidade (trace).

### Passo 2 - Organizar workflow
Sugestão de passos:

1. interpretar entrada;
2. coletar dados;
3. tratar erro e retry;
4. compor resposta;
5. validar contrato;
6. retornar saída.

### Passo 3 - Expor API
Mínimo recomendado:

- GET /health: status da aplicacao;
- POST endpoint principal: recebe input e retorna contrato.

### Passo 4 - Containerizar (opcional)
Mínimo recomendado:

- Dockerfile com dependencia e comando de start;
- porta exposta;
- execucao com docker run ou compose.

### Passo 5 - Interface (opcional)
Se houver tempo:

- Streamlit consumindo endpoint principal;
- modo chat simples com historico local da sessao;
- botao de limpar conversa.

---

## Rubrica rápida de avaliacao

### 1) Funcionalidade (40%)
- fluxo executa do inicio ao fim;
- API responde de forma consistente.

### 2) Robustez (25%)
- fallback/retry/revisao humana presentes;
- tratamento de erro claro.

### 3) Operabilidade (20%)
- execucao documentada;
- ambiente reproduzivel (Docker).

### 4) Comunicacao tecnica (15%)
- demo objetiva;
- justificativas de design e limites conhecidos.

---

## Checklist de pronto para demo

- [ ] endpoint de health responde
- [ ] endpoint principal responde com contrato esperado
- [ ] pelo menos 1 caso de erro demonstrado
- [ ] instrucoes de execucao no README
- [ ] (bonus) frontend consumindo API

---

## Avalie

1. O que mudou ao sair do notebook para API?
2. Qual parte do fluxo foi mais fragil?
3. O que o Docker resolveu no contexto de reprodução?
4. Onde entraria observabilidade em uma próxima iteração?
