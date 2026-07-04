# Changelog

## [Unreleased]

### Added

- Suporte Fedora 44+, Ubuntu 26.04 LTS, Debian e WSL.
- Perfis e módulos com dry-run e modo interativo.
- Detecção de NVIDIA, HyperX, Secure Boot e memória.
- Integração com terminal-config e openshift-cli-installer.
- OpenRGB, KVM/libvirt e repositório HashiCorp opcionais.
- Perfil Precision 3591/P127F e inventário conhecido de periféricos.
- Módulo Dell com fwupd, Thunderbolt, DDC/CI e helper para S3423DWC.
- Suporte NVIDIA híbrido com switcheroo-control.
- Firmware/LVFS para qualquer workstation.
- Módulo multimídia com RPM Fusion, FFmpeg, VA-API, fontes e AppImage.
- Spectacle como ferramenta de captura de tela do perfil desktop.
- Preparação de chave akmods quando Secure Boot está habilitado.
- Testes, CI e releases por tags semânticas.

### Removed

- Instalação monolítica e obrigatória de todos os aplicativos.
- VirtualBox misturado ao stack KVM.
