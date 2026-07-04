# Hardware conhecido

Os arquivos deste diretório documentam o equipamento alvo sem substituir a
detecção em tempo de execução.

## Precision 3591 / P127F

- 64 GiB de RAM: adequado ao perfil `full` e KVM/libvirt.
- A GPU discreta deve ser detectada por PCI; o modelo suporta diferentes GPUs
  NVIDIA Ada e o perfil não escolhe uma delas por suposição.
- Firmware é consultado por `fwupd`; atualização exige decisão explícita.

## Dell S3423DWC

- Habilite DDC/CI no OSD.
- Conecte vídeo/dados USB-C ao primeiro computador.
- Conecte vídeo e upstream USB-B ao segundo computador.
- Configure Auto Select for USB/KVM no OSD.
- Use `dell-monitor capabilities` antes de automatizar VCP `0x60`.

## HyperX Alloy FPS RGB

- Modelo: `HX-KB1SS2-US`.
- USB: `0951:16dc`.
- Layout físico: US.
- Linux: OpenRGB para recursos de iluminação compatíveis.
- Firmware, macros avançadas e perfis internos podem exigir NGENUITY no
  Windows.
