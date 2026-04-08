import re
import requests
import sys

class CAInterpreter:
    def __init__(self):
        self.ais = {}
        self.api_key = None
        self.model = "meta-llama/llama-3-8b-instruct"
        self.DEBUG = False

    # =============================
    # CONFIG
    # =============================
    def setAPI(self, key):
        self.api_key = key
        print("[C&A] API configurada.")

    def setModel(self, model):
        self.model = model
        print(f"[C&A] Modelo definido: {model}")

    # =============================
    # IA
    # =============================
    def AICreate(self, name):
        self.ais[name] = {"history": []}
        print(f"[C&A] IA '{name}' criada.")

    def AITrain(self, name=None, text=None):
        if not self.ais:
            print("[ERRO] Nenhuma IA criada.")
            return

        # usa primeira IA se não passar nome
        if not name:
            name = list(self.ais.keys())[0]

        if name not in self.ais:
            print("[ERRO] IA não encontrada.")
            return

        # modo interativo
        if not text:
            print("Digite como a IA deve se comportar:")
            text = input("> ")

        self.ais[name]["history"].append(f"Sistema: {text}")
        print(f"[C&A] IA '{name}' treinada.")

    # =============================
    # API
    # =============================
    def gerar_resposta(self, prompt):
        if not self.api_key:
            return "[ERRO] API não configurada."

        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost",
                    "X-Title": "C&A Language"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                }
            )

            data = response.json()

            if self.DEBUG:
                print("\n[DEBUG API]:", data, "\n")

            if "error" in data:
                return f"[ERRO API] {data['error']['message']}"

            if "choices" not in data:
                return "[ERRO] Resposta inválida da API."

            return data["choices"][0]["message"]["content"]

        except Exception as e:
            return f"[ERRO] {str(e)}"

    # =============================
    # COMANDOS
    # =============================
    def AIAsk(self, name, question):
        if name in self.ais:
            history = "\n".join(self.ais[name]["history"])
            prompt = f"{history}\nUsuário: {question}"

            resposta = self.gerar_resposta(prompt)

            print(f"[{name}] {resposta}")

            self.ais[name]["history"].append(f"Usuário: {question}")
            self.ais[name]["history"].append(f"IA: {resposta}")

    def AI_Input(self, prompt):
        if not self.ais:
            print("[ERRO] Nenhuma IA criada.")
            return

        name = list(self.ais.keys())[0]

        while True:
            user_input = input(prompt + " ")

            if user_input.lower() in ["sair", "exit"]:
                print("[C&A] Encerrando...")
                break

            history = "\n".join(self.ais[name]["history"])
            full_prompt = f"{history}\nUsuário: {user_input}"

            resposta = self.gerar_resposta(full_prompt)

            print(f"[{name}] {resposta}")

            self.ais[name]["history"].append(f"Usuário: {user_input}")
            self.ais[name]["history"].append(f"IA: {resposta}")

    # =============================
    # EXECUTOR
    # =============================
    def run(self, code):
        lines = code.splitlines()

        for line in lines:
            line = line.strip()

            if not line or line.startswith("//"):
                continue

            # setAPI
            match = re.match(r'c\.setAPI\("(.*?)"\)', line)
            if match:
                self.setAPI(match.group(1))
                continue

            # setModel
            match = re.match(r'c\.setModel\("(.*?)"\)', line)
            if match:
                self.setModel(match.group(1))
                continue

            # AICreate
            match = re.match(r'c\.AICreate\("(.*?)"\)', line)
            if match:
                self.AICreate(match.group(1))
                continue

            # AITrain completo
            match = re.match(r'c\.AITrain\("(.*?)","(.*?)"\)', line)
            if match:
                self.AITrain(match.group(1), match.group(2))
                continue

            # AITrain com nome
            match = re.match(r'c\.AITrain\("(.*?)"\)', line)
            if match:
                self.AITrain(match.group(1))
                continue

            # AITrain vazio
            match = re.match(r'c\.AITrain\(\)', line)
            if match:
                self.AITrain()
                continue

            # AIAsk
            match = re.match(r'c\.AIAsk\("(.*?)","(.*?)"\)', line)
            if match:
                self.AIAsk(match.group(1), match.group(2))
                continue

            # AI_Input
            match = re.match(r'c\.AI_Input\("(.*?)"\)', line)
            if match:
                self.AI_Input(match.group(1))
                continue


# =============================
# MAIN
# =============================
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python ca_interpreter.py arquivo.ca")
        exit()

    arquivo = sys.argv[1]

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            codigo = f.read()

        interpreter = CAInterpreter()
        interpreter.run(codigo)

    except FileNotFoundError:
        print("[ERRO] Arquivo não encontrado.")