from pathlib import Path

def get_project_root():
    """
    Retorna a raiz do projeto 'financas' de forma robusta e resiliente.
    Funciona mesmo se o script for executado:
    - diretamente (python arquivo.py)
    - como módulo (python -m pacote.modulo)
    - via .bat
    - via VSCode
    - com cwd diferente
    - em subpastas profundas
    """
    current = Path(__file__).resolve()

    # Sobe a árvore de diretórios até encontrar a pasta que contém o rodar.py
    for parent in current.parents:
        if (parent / "rodar.py").exists():
            return parent

    # fallback seguro: assume que estamos dentro de financas/
    return current.parents[1]