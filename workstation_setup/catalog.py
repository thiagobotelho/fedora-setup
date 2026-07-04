BASE = {
    "fedora": [
        "git", "git-lfs", "curl", "wget", "ca-certificates", "python3",
        "python3-pip", "pipx", "jq", "unzip", "zip", "tar", "rsync",
        "openssl", "gnupg2", "dnf-plugins-core", "pciutils", "usbutils",
        "util-linux", "mokutil", "ShellCheck",
    ],
    "ubuntu": [
        "git", "git-lfs", "curl", "wget", "ca-certificates", "python3",
        "python3-pip", "pipx", "jq", "unzip", "zip", "tar", "rsync",
        "openssl", "gnupg", "software-properties-common", "pciutils",
        "usbutils", "mokutil", "shellcheck",
    ],
    "debian": [
        "git", "git-lfs", "curl", "wget", "ca-certificates", "python3",
        "python3-pip", "pipx", "jq", "unzip", "zip", "tar", "rsync",
        "openssl", "gnupg", "pciutils", "usbutils", "mokutil", "shellcheck",
    ],
}

DEVOPS = {
    "fedora": [
        "ansible-core", "podman", "podman-compose", "buildah", "skopeo",
        "crun", "containernetworking-plugins", "make", "gcc", "go",
        "java-21-openjdk-devel", "maven", "gh", "opentofu", "yamllint",
        "bind-utils", "nmap", "tcpdump", "wireshark-cli",
    ],
    "ubuntu": [
        "ansible-core", "podman", "podman-compose", "buildah", "skopeo",
        "crun", "containernetworking-plugins", "make", "gcc", "golang-go",
        "default-jdk", "maven", "gh", "yamllint", "dnsutils", "nmap",
        "tcpdump", "tshark",
    ],
    "debian": [
        "ansible-core", "podman", "podman-compose", "buildah", "skopeo",
        "crun", "containernetworking-plugins", "make", "gcc", "golang-go",
        "default-jdk", "maven", "gh", "yamllint", "dnsutils", "nmap",
        "tcpdump", "tshark",
    ],
}

DESKTOP = {
    "fedora": [
        "flatpak", "gnome-tweaks", "gnome-extensions-app", "gparted",
        "spectacle", "vlc",
    ],
    "ubuntu": [
        "flatpak", "gnome-tweaks", "gnome-shell-extension-manager",
        "gparted", "spectacle", "vlc",
    ],
    "debian": ["flatpak", "gnome-tweaks", "gparted", "spectacle", "vlc"],
}

VIRTUALIZATION = {
    "fedora": ["@virtualization", "virt-manager", "libvirt", "qemu-kvm"],
    "ubuntu": ["qemu-kvm", "libvirt-daemon-system", "libvirt-clients", "virt-manager"],
    "debian": ["qemu-system-x86", "libvirt-daemon-system", "libvirt-clients", "virt-manager"],
}

FLATPAKS = [
    "com.brave.Browser",
    "com.getpostman.Postman",
    "com.github.tchx84.Flatseal",
    "com.mattjakeman.ExtensionManager",
    "it.mijorus.gearlever",
]
