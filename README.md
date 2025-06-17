# fedora-setup

Script de automação para configurar um ambiente completo no Fedora 41/42. Ideal para desenvolvedores, profissionais DevOps e usuários que desejam economizar tempo após formatação.

## 🚀 O que este script faz?

- Ativa os repositórios RPM Fusion (Free & Non-Free)
- Adiciona Flathub como fonte Flatpak
- Instala navegadores, IDEs, utilitários, codecs, e ferramentas de desenvolvimento
- Tudo automatizado via Python com `dnf` e `flatpak`

---

## 🧰 Softwares instalados

### 🖥️ Interface e utilitários
- GNOME Tweaks, Extension Manager, Browser Connector
- Flameshot, GParted, Vim (completo), Terminal Tools (tmux, btop, fd)

### 🌐 Navegadores
- Brave, Opera, Chromium

### 🧠 Desenvolvimento
- VS Code (RPM), PyCharm Community (Flatpak), Ansible, Podman, Java OpenJDK

### 🎥 Multimídia
- VLC, qBittorrent, OBS Studio, Codecs GStreamer, FFmpeg

### 📨 Comunicação
- Postman, Telegram Desktop, Notepad++

### ☁️ Virtualização
- Virtual Machine Manager (`virt-manager`)

---

## 📦 Como usar

```bash
git clone https://github.com/seu-usuario/fedora-setup.git
cd fedora-setup
chmod +x install.py
./install.py
