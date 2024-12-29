import os
import sys

# Flag global para garantir que o debugpy seja inicializado apenas uma vez
DEBUGPY_INITIALIZED = False

def main():
    global DEBUGPY_INITIALIZED

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

    # Verifica se o debugpy já foi inicializado
    if not DEBUGPY_INITIALIZED:
        if os.environ.get('RUN_MAIN') != 'true':  # Evita inicialização dupla do servidor
            try:
                import debugpy
                if not debugpy.is_client_connected():
                    debugpy.listen(("0.0.0.0", 5678))  # Porta configurada para depuração
                    print("Debugpy ativo. Conecte o depurador na porta 5678.")
                    DEBUGPY_INITIALIZED = True  # Marca que o debugpy foi iniciado
            except ImportError:
                print("O pacote 'debugpy' não está instalado. Instale-o para usar a depuração remota.")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
