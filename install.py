#!/usr/bin/env python3
import subprocess

def run(cmd, sudo=True):
    if sudo:
        cmd.insert(0, "sudo")
    print(f"\n🔧 Executando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def get_fedora_version():
    return subprocess.check_output(["rpm", "-E", "%fedora"]).decode().strip()

def update_system():
    run(["dnf", "upgrade", "--refresh", "-y"])

def enable_repos():
    version = get_fedora_version()
    free_url = f"https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-{version}.noarch.rpm"
    nonfree_url = f"https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{version}.noarch.rpm"

    run(["dnf", "install", "-y", free_url, nonfree_url])
    run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"])

def install_rpm_packages():
    pacotes = [
        "zsh", "tmux", "git", "curl", "wget", "neovim", "vim-enhanced", "htop",
        "python3-pip", "ansible", "podman", "bat", "btop", "fd-find",

        # GNOME e interface
        "gnome-tweaks", "gnome-browser-connector", "gnome-extensions-app",

        # Navegadores e utilitários
        "chromium", "qbittorrent", "vlc", "flameshot",

        # Multimídia
        "gstreamer1-plugins-base", "gstreamer1-plugins-good", "gstreamer1-plugins-bad-free",
        "gstreamer1-plugins-bad-free-extras", "gstreamer1-libav", "ffmpeg-free", "ffmpeg",

        # Comunicação
        "telegram-desktop",

        # Streaming, Java e virtualização
        "obs-studio", "java-latest-openjdk", "virt-manager", "gparted"
    ]
    run(["dnf", "install", "-y", "--allowerasing"] + pacotes)

def install_vscode():
    run(["rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"])
    run(["sh", "-c", 'echo -e "[code]\\nname=Visual Studio Code\\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\\nenabled=1\\ngpgcheck=1\\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'])
    run(["dnf", "check-update"])
    run(["dnf", "install", "-y", "code"])

def install_brave():
    run(["rpm", "--import", "https://brave.com/signing-key.asc"])
    run(["sh", "-c", 'echo -e "[brave-browser]\\nname=Brave Browser\\nbaseurl=https://brave-browser-rpm-release.s3.brave.com/\\nenabled=1\\ngpgcheck=1\\ngpgkey=https://brave.com/signing-key.asc" > /etc/yum.repos.d/brave-browser.repo'])
    run(["dnf", "install", "-y", "brave-browser"])

def install_opera():
    run(["dnf", "config-manager", "--add-repo", "https://rpm.opera.com/rpm"])
    run(["dnf", "install", "-y", "opera-stable"])

def install_flatpak_apps():
    flatpaks = [
        "com.getpostman.Postman",
        "org.notepad_plus_plus.NotepadPlusPlus",
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
    install_opera()
    install_flatpak_apps()
    print("\n✅ Fedora configurado com sucesso com todas as ferramentas essenciais!")

if __name__ == "__main__":
    main()
