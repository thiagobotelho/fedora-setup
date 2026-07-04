# Contribuindo

1. Preserve Python 3.10+ e execução sem `shell=True`.
2. Prefira repositórios oficiais e pacotes da distribuição.
3. Toda instalação destrutiva ou de hardware deve ser opt-in.
4. Mantenha Fedora e Ubuntu nos catálogos.
5. Execute:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 install.py --profile full --dry-run
```
