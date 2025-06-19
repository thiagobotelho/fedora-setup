#!/usr/bin/env python3
import subprocess

def run(cmd, sudo=True, input=None):
    if sudo:
        cmd.insert(0, "sudo")
    print(f"\n🔧 Executando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, input=input)

def get_fedora_version():
    return subprocess.check_output(["rpm", "-E", "%fedora"]).decode().strip()

def update_system():
    run(["dnf", "upgrade", "--refresh", "-y"])

def enable_repos():
    version = get_fedora_version()
    run(["dnf", "install", "-y", f"https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-{version}.noarch.rpm"])
    run(["dnf", "install", "-y", f"https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{version}.noarch.rpm"])
    run(["dnf", "install", "-y", "flatpak"])
    run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"])

def install_rpm_packages():
    pacotes = [
        # 🧰 Terminal e utilitários
        "zsh", "tmux", "git", "curl", "wget", "neovim", "vim-enhanced", "htop",
        "bat", "btop", "fd-find", "alacritty", "glances",

        # 🐍 DevOps / Desenvolvimento
        "python3-pip", "ansible", "podman", "terraform", "packer", "vault", "maven",

        # ☕ Java
        "java-17-openjdk", "java-21-openjdk",

        # 🛡️ Segurança
        "clamav", "clamtk", "rkhunter", "nmap", "wireshark",

        # 🎨 Interface e temas
        "gnome-tweaks", "papirus-icon-theme", "catppuccin-gtk-theme", "gnome-browser-connector", "gnome-extensions-app",

        # 🌐 Navegadores e ferramentas gráficas
        "chromium", "qbittorrent", "vlc", "flameshot", "obs-studio", "gparted",

        # 💬 Comunicação
        "telegram-desktop",

        # 🧰 Virtualização
        "virt-manager"
    ]
    run(["dnf", "install", "-y", "--allowerasing"] + pacotes)

def install_vscode():
    run(["rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"])
    repo_content = b"""[code]
name=Visual Studio Code
baseurl=https://packages.microsoft.com/yumrepos/vscode
enabled=1
gpgcheck=1
gpgkey=https://packages.microsoft.com/keys/microsoft.asc
"""
    run(["tee", "/etc/yum.repos.d/vscode.repo"], input=repo_content)
    try:
        run(["dnf", "check-update"])
    except subprocess.CalledProcessError as e:
        if e.returncode != 100:
            raise
    run(["dnf", "install", "-y", "code"])

def install_brave():
    run(["rpm", "--import", "https://brave-browser-rpm-release.s3.brave.com/brave-core.asc"])
    repo_content = b"""[brave-browser]
name=Brave Browser
baseurl=https://brave-browser-rpm-release.s3.brave.com/x86_64/
enabled=1
gpgcheck=1
gpgkey=https://brave-browser-rpm-release.s3.brave.com/brave-core.asc
"""
    run(["tee", "/etc/yum.repos.d/brave-browser.repo"], input=repo_content)
    run(["dnf", "install", "-y", "brave-browser"])

def install_flatpak_apps():
    flatpaks = [
        "com.getpostman.Postman",
        "com.github.dail8859.NotepadNext",
        "com.jetbrains.PyCharm-Community"
    ]
    for app in flatpaks:
        run(["flatpak", "install", "-y", "flathub", app])

def main():
    update_system()
    enable_repos()
    install_rpm_packages()
    install_vscode()
    install_brave()
    install_flatpak_apps()
    print("\n✅ Fedora configurado com sucesso com ferramentas para terminal, DevOps, segurança e interface gráfica!")

if __name__ == "__main__":
    main()
