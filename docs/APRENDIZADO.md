# Perfis e módulos de workstation


Comece com --profile minimal --dry-run e compare com --profile full --force-hardware --dry-run. Leia os módulos antes de habilitar drivers, firmware ou virtualização. A reversão deve ser definida por pacote, serviço e arquivo; não existe desinstalação universal segura de drivers. Faça snapshot do sistema quando disponível.

## Integrações

A preparação do sistema pertence a este projeto; dotfiles, CLIs e CRC pertencem a terminal-config, openshift-cli-installer e openshift-local-installer. Confira as referências utilizadas pelo módulo integrations antes de executar. A simulação mostra ações propostas; disponibilidade de KVM, drivers e dispositivos precisa ser verificada no sistema de destino.
