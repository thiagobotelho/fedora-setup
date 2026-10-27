# Perfis e módulos de workstation

## O que observar

Comece com --profile minimal --dry-run e compare com --profile full --force-hardware --dry-run. Leia os módulos antes de habilitar drivers, firmware ou virtualização. A reversão deve ser definida por pacote, serviço e arquivo; não existe desinstalação universal segura de drivers. Faça snapshot do sistema quando disponível.

## Roteiro de leitura e validação

1. Leia o README e identifique o componente que recebe a configuração.
2. Confira namespaces, seletores, portas, identidades e dependências nos exemplos.
3. Ajuste apenas os campos necessários em um ambiente isolado; não use credenciais de produção.
4. Valide sintaxe e contratos locais antes de aplicar. Registre o resultado real separado deste guia.
5. Execute um caso permitido e um caso negado, conferindo a causa da resposta.
6. Defina reversão por recurso/arquivo e preserve dados persistentes antes de mudanças.

Os comentários dos manifests explicam escolhas; não comprovam disponibilidade do componente. Exemplos fora de entradas Kustomize não são implantados automaticamente.
