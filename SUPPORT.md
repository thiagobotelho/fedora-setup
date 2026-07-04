# Suporte

| Plataforma | Nível |
|---|---|
| Fedora Workstation 44+ | suportada |
| Ubuntu Desktop 26.04 LTS | suportada |
| Debian estável atual | melhor esforço |
| Fedora/Ubuntu em WSL 2 | suportada sem módulos desktop/hardware |
| Linux `x86_64` | suportado |
| Linux `aarch64` | melhor esforço, conforme pacotes externos |
| Hardware Dell | firmware e periféricos conforme suporte do LVFS/Linux |
| Monitores DDC/CI | controle conforme recursos anunciados pelo monitor |
| Dispositivos HyperX | iluminação conforme suporte do OpenRGB |

Drivers NVIDIA dependem do modelo da GPU, kernel, Secure Boot e disponibilidade
nos repositórios da distribuição.

Recursos de utilitários proprietários dependem do fabricante. As alternativas
Linux são limitadas ao que `ddcutil`, OpenRGB e o próprio hardware expõem.
