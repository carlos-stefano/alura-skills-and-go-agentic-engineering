# Política — Limites de automação para agentes de desenvolvimento

O sistema agêntico pode sugerir alterações em código, plano de testes e rascunho de pull request.

O sistema não deve aplicar alterações diretamente em branch principal, executar deploy, alterar segredos, modificar permissões ou abrir PR automaticamente sem aprovação humana.

Mudanças em código devem ser acompanhadas de:

- evidências utilizadas;
- arquivos afetados;
- justificativa técnica;
- plano mínimo de testes;
- avaliação de risco;
- indicação clara de revisão humana obrigatória.
