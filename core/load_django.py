import os
import sys
import django

current_dir = os.path.dirname(os.path.abspath(__file__))
django_root = os.path.abspath(os.path.join(current_dir, '..', 'braincomua_project'))

sys.path.insert(0, django_root)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'braincomua_project.settings')

django.setup()
