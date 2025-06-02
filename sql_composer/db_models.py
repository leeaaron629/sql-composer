from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

@dataclass
class Table:
    name: str
    columns: list
