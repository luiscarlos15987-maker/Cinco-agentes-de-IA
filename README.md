# Sistema multiagente de IA — Demonstração n8n

[![Verificação automática](https://github.com/luiscarlos15987-maker/Cinco-agentes-de-IA/actions/workflows/ci.yml/badge.svg)](https://github.com/luiscarlos15987-maker/Cinco-agentes-de-IA/actions/workflows/ci.yml)

Projeto de portfólio para demonstrar um **fluxo de cinco agentes de IA em sequência**, validação determinística em JavaScript e geração de relatório com revisão humana.

> **Demonstração, não produto em produção.** Usa registros fictícios da API pública JSONPlaceholder. A versão deste repositório é sanitizada: não contém credenciais, chaves, dados brutos de execução, respostas dos modelos ou tokens de sessão.

**Versão demonstrativa 1.0:** teste manual local concluído. [Notas da versão](docs/VERSAO_1_0.md).

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

## Qualidade automatizada

A verificação `GitHub Actions` roda a cada alteração, em pull requests, manualmente e uma vez por semana. Não precisa de chave OpenAI e não consome créditos de IA.

- **Estrutura e segurança:** checa JSON, conexões, cinco agentes + cinco modelos e ferramentas, IDs, `active: false`, ausência de credenciais embutidas e padrões comuns de segredo.
- **Testes JavaScript reais, sem rede:** executa os nós Code de preparação, validação e construção do relatório com três registros fictícios e saídas de agentes simuladas.
- **Revisão humana e limites:** os testes conferem a presença de auditoria/relatório, mas **não comprovam a qualidade das respostas do modelo**.

Para reproduzir no VS Code com Python 3.12 e Node.js 22:

```powershell
python scripts/quality_gate.py --mode portfolio
node scripts/test_agents.mjs workflows/cinco_agentes_demo_sanitizado.json
```

[Consultar histórico dos testes automáticos](https://github.com/luiscarlos15987-maker/Cinco-agentes-de-IA/actions) · [Escopo e pendências](docs/VALIDACAO.md)

## Demonstração e evidências

Na pequena amostra disponibilizada: **4 execuções consultadas**, **3 percorreram os cinco agentes**, **1 não executou nenhum agente**. Não há indicação de falha individual entre as etapas efetivamente executadas na amostra. Isso **não demonstra estabilidade em produção** nem valida a correção do conteúdo gerado.

### Teste local da cópia de portfólio

Em 27/11/2026, o autor apresentou evidência visual de execução manual ponta a ponta da demonstração no n8n: consulta de dados fictícios, validação JavaScript, cinco agentes com GPT-4o-mini, conversão e gravação de relatório TXT. O workflow demonstrativo permanece despublicado. A evidência não constitui avaliação semântica das respostas nem validação de produção. Nenhum relatório bruto ou credencial foi publicado.

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
- A versão foi validada estruturalmente, e a cópia local importada foi testada pelo autor. Não há garantia de compatibilidade com outras versões do n8n.

**Fontes:** [Documentação n8n — exportação e importação](https://docs.n8n.io/workflows/export-import/) · [Documentação n8n — leitura/escrita de arquivos](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.readwritefile/) · [JSONPlaceholder](https://jsonplaceholder.typicode.com/).
