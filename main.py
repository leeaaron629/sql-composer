import os

from dotenv import load_dotenv

load_dotenv()

PROJECT_NAME = os.getenv("PROJECT_NAME")

def main():
    print(f"Hello from {PROJECT_NAME}!")

if __name__ == "__main__":
    main()
