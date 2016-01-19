#!/usr/bin/env python
import os
import sys

# Add the parent directory to the PYTHONPATH
abspath = os.path.abspath(__file__)
parent_dir = os.path.dirname(os.path.dirname(abspath))
sys.path.insert(1,parent_dir)

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bps.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
