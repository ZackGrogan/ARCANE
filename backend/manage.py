import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "arcane_backend.settings")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.join(current_dir, 'backend'))
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
