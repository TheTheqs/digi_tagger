from database.engine import init_db

def main():
    print("Inicializando o banco de dados Eyeing...")
    init_db()
    print("Banco de dados criado com sucesso!")

if __name__ == "__main__":
    main()
