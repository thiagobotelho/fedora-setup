#!/usr/bin/env python3
import subprocess

def run(cmd, sudo=True, input=None):
    if sudo:
        cmd.insert(0, "sudo")
    print(f"\n🔧 Executando: {' '.join(cmd)}")
    subprocess.run(cmd, check=True, input=input, text=True)

def get_fedora_version():
    return subprocess.check_output(["rpm", "-E", "%fedora"]).decode().strip()

def update_system():
    run(["dnf", "upgrade", "--refresh", "-y"])

def is_repo_enabled(repo_id):
    result = subprocess.run(["dnf", "repolist"], capture_output=True, text=True)
    return repo_id in result.stdout

def is_flathub_enabled():
    result = subprocess.run(["flatpak", "remotes"], capture_output=True, text=True)
    return "flathub" in result.stdout

def enable_repos():
    version = get_fedora_version()

    # Habilitar RPM Fusion Free
    if not is_repo_enabled("rpmfusion-free"):
        run(["dnf", "install", "-y", f"https://mirrors.rpmfusion.org/free/fedora/rpmfusion-free-release-{version}.noarch.rpm"])
    else:
        print("🆗 Repositório rpmfusion-free já habilitado.")

    # Habilitar RPM Fusion Non-Free
    if not is_repo_enabled("rpmfusion-nonfree"):
        run(["dnf", "install", "-y", f"https://mirrors.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-{version}.noarch.rpm"])
    else:
        print("🆗 Repositório rpmfusion-nonfree já habilitado.")

    # Habilitar Flathub
    if not is_flathub_enabled():
        run(["flatpak", "remote-add", "--if-not-exists", "flathub", "https://flathub.org/repo/flathub.flatpakrepo"])
    else:
        print("🆗 Flathub já está configurado.")
        
def install_rpm_packages():
    pacotes = [
        # 🧰 Terminal e utilitários
        "zsh", "tmux", "git", "curl", "wget", "neovim", "vim-enhanced",
        "bat", "btop", "fd-find", "alacritty", "glances", "vagrant",
        "lftp", "filezilla",

        # 🐍 DevOps / Desenvolvimento
        "python3-pip", "ansible", "podman", "maven",

        # ☕ Java
        "java-21-openjdk",

        # 🛡️ Segurança
        "clamav", "clamtk", "rkhunter", "nmap", "wireshark",

        # 🎨 Interface e Temas
        "gnome-tweaks", "gnome-browser-connector", "gnome-extensions-app",

        # 🌐 Navegadores e ferramentas gráficas
        "chromium", "qbittorrent", "vlc", "flameshot", "obs-studio", "gparted",

        # 💬 Comunicação
        "telegram-desktop",

        # 🧰 Virtualização
        "virt-manager", "VirtualBox"
    ]
    run(["dnf", "install", "-y", "--allowerasing"] + pacotes)

def install_vscode():
    run(["rpm", "--import", "https://packages.microsoft.com/keys/microsoft.asc"])
    
    repo_content = """[code]
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
    repo_content = """[brave-browser]
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

def install_hashicorp_tools():
    version = get_fedora_version()
    repo_content = f"""[hashicorp]
name=HashiCorp Stable - $basearch
baseurl=https://rpm.releases.hashicorp.com/fedora/{version}/$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://rpm.releases.hashicorp.com/gpg
"""
    run(["tee", "/etc/yum.repos.d/hashicorp.repo"], input=repo_content)
    run(["dnf", "update", "-y"])
    run(["dnf", "install", "-y", "terraform", "packer", "vault"])
    
def main():
    update_system()
    enable_repos()
    install_rpm_packages()
    install_vscode()
    install_brave()
    install_flatpak_apps()
    install_hashicorp_tools()
    print("\n✅ Fedora configurado com sucesso com ferramentas para terminal, DevOps, segurança e interface gráfica!")

if __name__ == "__main__":
    main()
