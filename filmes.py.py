import json
import datetime


def carregar_dados():
    try:
        with open("filmes.json", "r", encoding="utf-8") as arquivo:
            conteudo = json.load(arquivo)
            if isinstance(conteudo, dict):
                return conteudo.get("filmes", []), conteudo.get("ultima_modificacao", "N/A")
            return conteudo, "N/A"
    except (FileNotFoundError, json.JSONDecodeError):
        return [], "N/A"


def salvar_dados(lista):
    try:
        dados = {
            "ultima_modificacao": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
            "filmes": lista
        }
        with open("filmes.json", "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, indent=4, ensure_ascii=False)
    except Exception:
        print("ERRO: Falha ao salvar.")


def adicionar_filme(lista):
    try:
        nome = input("Nome do filme: ").strip()
        if not nome:
            print("ERRO: Nome inválido.")
            return

        print("[1] Assistido | [2] Não assistido")
        escolha = input("Status: ")

        status = "Assistido" if escolha == "1" else "Não assistido" if escolha == "2" else None

        if not status:
            print("ERRO: Opção inválida.")
            return

        try:
            nota = int(input("Nota (1 a 5): "))
            if nota < 1 or nota > 5:
                print("ERRO: Nota deve ser de 1 a 5.")
                return
        except ValueError:
            print("ERRO: Digite um número válido.")
            return

        lista.append({
            "nome": nome,
            "status": status,
            "nota": nota,
            "data": datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        })
        print("Filme adicionado!")
    except Exception:
        print("ERRO ao adicionar.")


def editar_filme(lista):
    if not lista:
        print("Lista vazia.")
        return

    listar_filmes(lista)
    try:
        indice = int(input("\nNúmero do filme: ")) - 1

        if 0 <= indice < len(lista):
            novo_nome = input("Novo nome: ").strip()
            print("[1] Assistido | [2] Não assistido")
            escolha = input("Novo status: ")

            if novo_nome:
                lista[indice]['nome'] = novo_nome

            if escolha == "1":
                lista[indice]['status'] = "Assistido"
            elif escolha == "2":
                lista[indice]['status'] = "Não assistido"

            print("Filme atualizado!")
        else:
            print("ERRO: inválido.")
    except ValueError:
        print("ERRO: número inválido.")


def listar_filmes(lista):
    if not lista:
        print("\nLista vazia.")
    else:
        print("\n--- FILMES ---")
        for i, f in enumerate(lista, 1):
            print(f"{i}. {f['nome']} | {f['status']} | ⭐ {f['nota']} | {f.get('data', '')}")


def buscar_filme(lista):
    termo = input("Buscar: ").lower().strip()
    resultados = [f for f in lista if termo in f['nome'].lower()]

    if resultados:
        for f in resultados:
            print(f"- {f['nome']} ({f['status']}) ⭐{f['nota']}")
    else:
        print("Nada encontrado.")


def estatisticas(lista, ultima_mod):
    total = len(lista)
    assistidos = sum(1 for f in lista if f['status'] == "Assistido")

    print("\n--- ESTATÍSTICAS ---")
    print(f"Última alteração: {ultima_mod}")
    print(f"Total: {total}")
    print(f"Assistidos: {assistidos}")
    print(f"Não assistidos: {total - assistidos}")


def menu():
    lista, ultima_mod = carregar_dados()

    while True:
        print("\n======================")
        print("   LISTA DE FILMES 🎬")
        print("======================")
        print("ADD    - Adicionar filme")
        print("LIST   - Listar filmes")
        print("EDIT   - Editar filme")
        print("SEARCH - Buscar filme")
        print("STATS  - Estatísticas")
        print("EXIT   - Sair")
        cmd = input("Comando: ").upper().strip()

        try:
            if cmd == "ADD":
                adicionar_filme(lista)
            elif cmd == "LIST":
                listar_filmes(lista)
            elif cmd == "EDIT":
                editar_filme(lista)
            elif cmd == "SEARCH":
                buscar_filme(lista)
            elif cmd == "STATS":
                estatisticas(lista, ultima_mod)
            elif cmd == "EXIT":
                salvar_dados(lista)
                break
            else:
                print("Comando inválido.")
        except Exception:
            print("Erro na operação.")


if __name__ == "__main__":
    menu()