# Segurança e privacidade

Este repositório contém **somente uma demonstração sanitizada** de um fluxo de cinco agentes de IA. Não contém o ambiente operacional original.

## O que foi excluído

- Credenciais e IDs de credenciais n8n, tokens de API e segredos OAuth/Outlook.
- IDs de workflows e execuções reais, históricos brutos, `pinData` de execução e logs.
- Dados reais de clientes, e-mails particulares, relatórios privados e respostas completas de modelos.
- Configuração dos serviços privados de monitoramento, TXT, Outlook e Docker.

No workflow publicado, os IDs dos nós são substituídos por IDs sintéticos. As credenciais dos cinco nós de modelo devem ser adicionadas **somente na instância n8n local**.

## Atenção antes de executar

1. Use uma instância controlada do n8n, inicialmente em ambiente de teste.
2. Conecte apenas contas e chaves suas; mantenha os segredos em credenciais do n8n.
3. Verifique o volume Docker que permite a escrita em `/files` e restrinja seu acesso.
4. Não importe execuções reais, relatórios com dados privados ou `.env` para este repositório.
5. O fluxo é manual e não deve enviar ou publicar resultados sem revisão humana.
6. Controle custos e permissões de APIs de IA.

Uma varredura de padrões conhecidos foi realizada, mas **não equivale a uma auditoria completa de segurança**. Se uma chave for exposta, revogue-a e gere uma nova imediatamente.

Fonte oficial: https://docs.n8n.io/hosting/configuration/environment-variables/security/
