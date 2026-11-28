# Como importar o workflow de demonstração

**Requisitos:** n8n com suporte aos nós AI Agent, OpenAI Chat Model e Calculator Tool, credenciais próprias do provedor de IA e local autorizado para gerar TXT.

## Etapas

1. Baixe `workflows/cinco_agentes_demo_sanitizado.json`.
2. Abra o n8n e crie um workflow novo.
3. No menu do editor, clique em **Import from File** e selecione o JSON.
4. Confirme os 22 nós e a sequência Triagem → Qualidade → Análise → Relatório → Auditoria.
5. Abra os nós `Modelo OpenAI 1` até `Modelo OpenAI 5` e associe suas credenciais **diretamente no n8n**. A definição usa o modelo `gpt-4o-mini` como exemplo; confira disponibilidade e cobrança antes de executar.
6. O nó `Salvar relatorio IA no Windows` escreve em `/files/relatorio_5_agentes.txt` **dentro do contêiner**. Garanta que a pasta exista, esteja autorizada na configuração do n8n e, se quiser ver o arquivo no Windows, configure um bind mount adequado para `/files`. Para instalações com restrições de acesso ao filesystem, ajuste a permissão/configuração conforme a documentação oficial.
7. Execute somente pelo **gatilho manual**, utilizando os registros fictícios da JSONPlaceholder.
8. Confira o TXT gerado e faça revisão humana do resultado antes de qualquer uso externo.

## Limitações

- Importar o JSON não configura credenciais automaticamente.
- A geração de TXT depende do volume/pasta e das permissões de escrita.
- Pode exigir ajustes entre versões do n8n.
- O JSON foi validado estruturalmente e o autor demonstrou a execução da cópia local importada em 27/11/2026. A execução em outras instalações depende da configuração local.

## Links oficiais

- https://docs.n8n.io/workflows/export-import/
- https://docs.n8n.io/integrations/builtin/cluster-nodes/root-nodes/n8n-nodes-langchain.agent/
- https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.readwritefile/
