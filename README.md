# Sistema multiagente de IA — Demonstração n8n

Projeto de portfólio para demonstrar um **fluxo de cinco agentes de IA em sequência**, validação determinística em JavaScript e geração de relatório com revisão humana.

> **Demonstração, não produto em produção.** Usa registros fictícios da API pública JSONPlaceholder. A versão deste repositório é sanitizada: não contém credenciais, chaves, dados brutos de execução, respostas dos modelos ou tokens de sessão.

## Arquitetura

1. **Entrada:** acionamento manual e consulta de dados fictícios à API JSONPlaceholder.
2. **Validação:** código JavaScript calcula completude, IDs, sintaxe básica de e-mails e duplicações.
3. **Triagem:** identifica finalidade, estrutura e dúvidas.
4. **Qualidade:** analisa consistência e limites da validação dos registros.
5. **Análise:** interpreta indicadores sem inventar métricas.
6. **Relatório:** redige um resumo executivo.
7. **Auditoria:** revisa afirmações e requer aprovação humana.
8. **Saída:** gera um arquivo de relatório `.txt` no armazenamento acessível ao n8n.

Os nós de agentes utilizam um modelo de linguagem configurável no n8n. A amostra original foi executada com `gpt-4o-mini`.

## Arquivos

- `workflows/cinco_agentes_demo_sanitizado.json`: estrutura do workflow para importação no n8n, sem referências a credenciais.
- `docs/metricas_demo_anonimizadas.json`: resultados **agregados** de quatro execuções de demonstração, sem dados pessoais, IDs ou horários.
- `docs/COMO_IMPORTAR.md`: importação, configuração e limitações.
- `SECURITY.md`: escopo da sanitização e recomendações antes da publicação.

## Demonstração e evidências

Na pequena amostra disponibilizada: **4 execuções consultadas**, **3 percorreram os cinco agentes**, **1 não executou nenhum agente**. Não há indicação de falha individual entre as etapas efetivamente executadas na amostra. Isso **não demonstra estabilidade em produção** nem valida a correção do conteúdo gerado.

## Como reproduzir

1. Instale uma instância do n8n com acesso aos nós de IA usados neste exemplo.
2. Importe o JSON sanitizado usando o menu do editor: **Import from File**.
3. Configure **suas próprias credenciais OpenAI** nos cinco nós de modelo. Nenhuma chave é incluída neste projeto.
4. Configure um caminho de saída permitido na instância (consulte `docs/COMO_IMPORTAR.md`).
5. Execute o fluxo manualmente com dados fictícios e revise o relatório antes de usá-lo.

## Limites

- Não inclui aplicações reais de clientes, envio de mensagens nem integração com sistemas empresariais.
- Verificação de sintaxe de e-mail não garante existência ou recebimento.
- O fluxo pode exigir adaptação de nós ou configurações para versões diferentes do n8n.
- A importação não foi testada diretamente nesta sessão; o JSON foi validado estruturalmente.

**Fontes:** [Documentação n8n — exportação e importação](https://docs.n8n.io/workflows/export-import/) · [Documentação n8n — leitura/escrita de arquivos](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.readwritefile/) · [JSONPlaceholder](https://jsonplaceholder.typicode.com/).
