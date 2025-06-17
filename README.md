# fedora-setup

Script de automação para configurar rapidamente um ambiente completo no **Fedora 41/42** após formatação. Ideal para desenvolvedores, sysadmins e profissionais DevOps que desejam otimizar tempo com instalação de ferramentas essenciais.

## 🔧 O que este script faz?

- Ativa repositórios RPM Fusion e Flathub
- Instala navegadores: Brave, Opera, Chromium
- Instala ferramentas de produtividade: VS Code, Postman, Notepad++
- Instala utilitários e CLI essenciais: `zsh`, `tmux`, `btop`, `fd`, `bat`
- Instala codecs multimídia, VLC e qBittorrent
- Instala GNOME Extension Manager e Flameshot

## 🚀 Como usar

> Pré-requisitos: Fedora 41 ou 42, usuário com permissão `sudo`.

```bash
git clone https://github.com/seu-usuario/fedora-setup.git
cd fedora-setup
chmod +x install.py
./install.py
