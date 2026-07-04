# Suporte

| Plataforma | Nível |
|---|---|
| Fedora Workstation 44+ | suportada |
| Ubuntu Desktop 26.04 LTS | suportada |
| Debian estável atual | melhor esforço |
| Fedora/Ubuntu em WSL 2 | suportada sem módulos desktop/hardware |
| Linux `x86_64` | suportado |
| Linux `aarch64` | melhor esforço, conforme pacotes externos |
| Dell Precision 3591/P127F | perfil de hardware suportado |
| Dell S3423DWC | DDC/CI e KVM físico; sem Dell Display Manager |
| HyperX Alloy FPS RGB `0951:16dc` | iluminação via OpenRGB |

Drivers NVIDIA dependem do modelo da GPU, kernel, Secure Boot e disponibilidade
nos repositórios da distribuição.

O Dell Display Manager/NGENUITY não possui suporte oficial Linux. Recursos
equivalentes são limitados ao que `ddcutil`, OpenRGB e o hardware expõem.
