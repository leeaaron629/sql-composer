import os

from dotenv import load_dotenv
from sql_composer.db_models import Table

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME")

def main():
    print(f"Hello from {PROJECT_NAME}!")
    table = Table(name="test", columns=[])
    print(table)

if __name__ == "__main__":
    main()
