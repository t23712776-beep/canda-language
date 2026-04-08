import sys

def compilar_txt_para_ca(entrada, saida):
    try:
        with open(entrada, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        nome_ia = None
        codigo_ca = []

        for linha in linhas:
            linha = linha.strip()

            if not linha or linha.startswith("#"):
                continue

            # CRIAR IA
            if linha.upper().startswith("CRIAR IA"):
                nome_ia = linha.split("CRIAR IA")[1].strip()
                codigo_ca.append(f'c.AICreate("{nome_ia}");')

            # TREINAR
            elif linha.upper().startswith("TREINAR"):
                texto = linha.split("TREINAR")[1].strip()
                if nome_ia:
                    codigo_ca.append(f'c.AITrain("{nome_ia}","{texto}");')

            # CHAT
            elif linha.upper().startswith("CHAT"):
                texto = linha.split("CHAT")[1].strip()
                codigo_ca.append(f'c.AI_Input("{texto}");')

            # PERGUNTAR
            elif linha.upper().startswith("PERGUNTAR"):
                partes = linha.split("PERGUNTAR")[1].strip()
                if nome_ia:
                    codigo_ca.append(f'c.AIAsk("{nome_ia}","{partes}");')

            else:
                print(f"[AVISO] Linha ignorada: {linha}")

        with open(saida, "w", encoding="utf-8") as f:
            f.write("\n".join(codigo_ca))

        print(f"[C&A] Compilado com sucesso: {saida}")

    except Exception as e:
        print(f"[ERRO] {str(e)}")


# =============================
# MAIN
# =============================
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python txt_to_ca_compiler.py entrada.txt saida.ca")
        exit()

    entrada = sys.argv[1]
    saida = sys.argv[2]

    compilar_txt_para_ca(entrada, saida)