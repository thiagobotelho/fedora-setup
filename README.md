# fedora-setup

Script de automação para configurar rapidamente um ambiente completo no Fedora 41 ou 42. Ideal para desenvolvedores, profissionais de DevOps, SREs e usuários que desejam produtividade imediata após a formatação.

---

## 🚀 Funcionalidades

- Ativa repositórios RPM Fusion (Free e Non-Free)
- Adiciona o repositório Flathub
- Instala navegadores, IDEs, ferramentas de terminal, codecs e utilitários
- Configura repositórios de terceiros (Brave, VS Code, HashiCorp)
- Suporte completo para ambiente gráfico com GNOME Tweaks e extensões
- Automatização via script Python com `dnf` e `flatpak`

---

## 🧰 Softwares instalados

### 🖥️ Interface e utilitários gráficos
- GNOME Tweaks, Extension Manager, Browser Connector
- Flameshot, GParted, Vim (completo), terminal tools (tmux, btop, fd, glances)

### 🌐 Navegadores
- Brave (repositório oficial)
- Chromium

### 🧠 Desenvolvimento
- VS Code (RPM oficial)
- PyCharm Community (Flatpak)
- Ansible, Podman, Maven
- Python 3 + Pip

### 🔐 Segurança e rede
- ClamAV, ClamTK, RKHunter
- Nmap, Wireshark

### 🎥 Multimídia
- VLC, qBittorrent, OBS Studio
- Codecs GStreamer e FFmpeg

### 💬 Comunicação
- Telegram Desktop
- Postman (Flatpak)
- Notepad++ (NotepadNext via Flatpak)

### ☁️ Virtualização e infraestrutura
- Virtual Machine Manager (`virt-manager`)
- Ferramentas HashiCorp: Terraform, Packer, Vault

---

## 📦 Como usar

Clone o repositório e execute o instalador:

```bash
git clone https://github.com/thiagobotelho/fedora-setup.git
cd fedora-setup
chmod +x install.py
sudo ./install.py
