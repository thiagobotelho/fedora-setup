# fedora-setup

Automação modular para preparar workstations **Fedora 44+**, **Ubuntu 26.04
LTS** e Debian para DevOps, infraestrutura, OpenShift e Kubernetes. O
instalador oferece perfis prontos, módulos opcionais, detecção de ambiente e
modo de simulação antes de alterar o sistema.

## Princípios

- nenhuma instalação pesada sem perfil ou módulo explícito;
- `--dry-run` para revisar todas as ações;
- detecção de WSL, RAM, NVIDIA, Secure Boot e dispositivos HyperX;
- KVM/libvirt em vez de misturar VirtualBox com o hipervisor nativo;
- ferramentas de terminal e OpenShift delegadas aos repositórios próprios;
- execução de subprocessos sem `shell=True`.

## Perfis

| Perfil | Conteúdo |
|---|---|
| `minimal` | sistema base, Git, Python, utilitários e diagnóstico |
| `devops` | base, containers, Ansible, compiladores e integrações |
| `workstation` | DevOps, aplicações desktop e integrações |
| `full` | workstation, KVM, hardware, HashiCorp e integrações |

Módulos disponíveis:

- `base`
- `firmware`
- `devops`
- `desktop`
- `multimedia`
- `vscode`
- `dell`
- `virtualization`
- `nvidia`
- `hyperx`
- `hashicorp`
- `integrations`

## Requisitos

- Fedora, Ubuntu ou Debian com acesso administrativo via `sudo`;
- Python 3.10 ou mais recente;
- Git e acesso à internet;
- ambiente gráfico para os módulos desktop.

Use `--dry-run` antes da primeira execução para conferir os comandos sem
alterar o sistema.

## Instalação e uso

```bash
git clone https://github.com/thiagobotelho/fedora-setup.git
cd fedora-setup

# Primeiro: inventário e simulação
python3 install.py --show-hardware
python3 install.py --profile workstation --dry-run

# Depois: instalação
python3 install.py --profile workstation
```

Modo guiado:

```bash
python3 install.py --interactive
```

Módulos específicos:

```bash
python3 install.py --modules base devops integrations
python3 install.py --modules nvidia --dry-run
python3 install.py --modules hyperx --keyboard-layout us
```

Para instalar todos os módulos, primeiro simule o perfil completo:

```bash
python3 install.py --profile full --dry-run
```

Depois de revisar a saída, execute novamente sem `--dry-run`.

Atualização completa do sistema é opcional:

```bash
python3 install.py --profile workstation --upgrade
```

## Integrações

O módulo `integrations` clona ou atualiza:

- [terminal-config](https://github.com/thiagobotelho/terminal-config)
- [openshift-cli-installer](https://github.com/thiagobotelho/openshift-cli-installer)

Em seguida executa os instaladores desses projetos. É possível desativar cada
um:

```bash
python3 install.py --profile devops --no-terminal-config
python3 install.py --profile devops --no-openshift-cli
```

## Ferramentas principais

O catálogo inclui Git/Git LFS, Python/pipx, ShellCheck, jq, Ansible, Podman,
Buildah, Skopeo, GitHub CLI, OpenTofu, Go, Java, Maven, yamllint, ferramentas
DNS/rede e captura de tráfego.

O módulo `hashicorp` adiciona o repositório oficial e instala Terraform,
Packer e Vault. Ele fica separado porque o perfil DevOps já oferece OpenTofu.

As CLIs `oc`, `kubectl`, Helm, Argo CD, Tekton, RHACM e RHACS são
responsabilidade do `openshift-cli-installer`.

## Firmware, codecs e compatibilidade desktop

Os perfis `workstation` e `full` consultam atualizações de firmware pelo LVFS,
mas nunca executam `fwupdmgr update` automaticamente.

O módulo `multimedia` é explícito porque habilita codecs/repositórios que podem
ter restrições de patente conforme o país:

- Fedora: RPM Fusion, FFmpeg completo, grupo multimedia, OpenH264, VA-API,
  codecs Bluetooth, fontes Noto/Liberation e compatibilidade AppImage/FUSE.
- Ubuntu: multiverse, FFmpeg, codecs extras, VA-API, fontes e FUSE.

Gear Lever é instalado pelo Flathub para gerenciar AppImages. Instale cada
aplicativo por apenas um formato (RPM/DEB ou Flatpak), evitando duplicatas.

## NVIDIA

O módulo só é executado em Linux nativo quando uma GPU NVIDIA é detectada, a
menos que `--force-hardware` seja usado.

- Fedora: RPM Fusion, `akmod-nvidia` e suporte CUDA do driver.
- Ubuntu: `ubuntu-drivers install`, que escolhe o driver recomendado.
- WSL: o driver deve ser instalado no host Windows; o módulo é ignorado.

O script detecta a GPU pelo dispositivo PCI e deixa RPM Fusion ou
`ubuntu-drivers` selecionar o pacote apropriado. Em notebooks híbridos,
`switcheroo-control` é habilitado; valide após reiniciar:

```bash
nvidia-smi
switcherooctl list
```

Com Secure Boot habilitado, revise as mensagens de assinatura/enrollment do
módulo antes de reiniciar. No Fedora, o instalador prepara a chave do akmods e
mostra o comando `mokutil --import`; o enrollment no menu MOK permanece
necessariamente interativo. Sempre aguarde `modinfo -F version nvidia`
responder antes do reboot.

## Hardware Dell e monitores DDC/CI

O módulo `dell` instala:

- `fwupd`/LVFS para consultar firmware Dell;
- `bolt` para dispositivos Thunderbolt/USB4;
- `power-profiles-daemon`, `thermald` e `switcheroo-control`;
- `ddcutil` e I²C para controlar o monitor externo.

O helper `dell-monitor` oferece controle de monitores compatíveis com DDC/CI:

```bash
dell-monitor detect
dell-monitor capabilities
dell-monitor brightness 70
dell-monitor contrast 75
dell-monitor get-input
dell-monitor input 0x11
```

Não copie o código `0x11` sem conferir: descubra os valores anunciados pelo
monitor em `dell-monitor capabilities`. Ative **DDC/CI** no OSD. Quando houver
mais de um monitor, defina `DELL_MONITOR_MODEL` com o nome exibido por
`ddcutil detect`.

Atualizações de firmware não são aplicadas automaticamente:

```bash
fwupdmgr get-devices
fwupdmgr get-updates
```

## OpenRGB e layout de teclado

O módulo `hyperx` detecta dispositivos USB HyperX, instala o OpenRGB da
distribuição e configura o layout somente quando solicitado.

O HyperX NGENUITY é disponibilizado pelo fabricante somente para Windows. No
Linux, OpenRGB é a alternativa para iluminação compatível; macros e firmware
podem continuar exigindo Windows e a memória interna do teclado.

Layouts suportados:

```bash
--keyboard-layout us       # US
--keyboard-layout us-intl  # US International
--keyboard-layout br       # ABNT2
```

## Virtualização

O módulo instala KVM, QEMU, libvirt e virt-manager. Por padrão ele é ignorado
em WSL e em máquinas com menos de 12 GiB de RAM. Para forçar:

```bash
python3 install.py --modules virtualization --force-hardware
```

## Aplicações desktop

O perfil workstation habilita Flathub e instala Brave, Postman e Flatseal,
além de utilitários GNOME, GParted, Spectacle e VLC. O Spectacle é instalado
explicitamente porque pertence ao KDE e não acompanha o Fedora Workstation
GNOME por padrão. O VS Code é instalado
pelo repositório oficial da Microsoft, sem sandbox de Flatpak. Em WSL, use o
VS Code do Windows com Remote WSL; os módulos gráficos são ignorados.

## Pós-instalação

Algumas mudanças exigem logout ou reboot:

- grupos `libvirt`, `kvm` e `wireshark`;
- driver NVIDIA;
- layout de teclado;
- shell padrão configurado pelo `terminal-config`.
- grupo `i2c` para controle DDC/CI do monitor.

Valide com:

```bash
podman info
ansible --version
oc version --client
kubectl version --client
terraform version   # quando o módulo HashiCorp for escolhido
```

## Desenvolvimento

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 install.py --profile full --dry-run
```

Consulte também [SUPPORT.md](SUPPORT.md), [CHANGELOG.md](CHANGELOG.md),
[CONTRIBUTING.md](CONTRIBUTING.md) e [LICENSE](LICENSE).
