import os
from django.core.management.base import BaseCommand
from django.db import IntegrityError, connection
from pathlib import Path
from typing import Any, Optional


class Command(BaseCommand):
    help = "Populates the database."

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        print("\033[94mPopulating database...\033[0m")
        current_dir = os.path.dirname(__file__)
        file_path = os.path.join(current_dir, "storefront3.sql")
        sql = Path(file_path).read_text()

        try:
            with connection.cursor() as db_cursor:
                db_cursor.execute(sql)
            print("\033[92mDatabase Populated.\033[0m")
        except IntegrityError:
            print("\033[91mDatabase already populated or with duplicate entries.\033[0m")
