import pandas as pd
import google.generativeai as genai

# 🔹 Configurar a API do Google Gemini
API_KEY = "AIzaSyA5L3HJJdwEsVuo_WGi9ZEY1tg9CKxujZU"
genai.configure(api_key=API_KEY)

# 🔹 Carregar planilha do Excel
def carregar_planilha(caminho):
    try:
        df = pd.read_excel(caminho)
        print(f"Planilha carregada com sucesso! {df.shape[0]} linhas encontradas.")
        return df
    except Exception as e:
        print("Erro ao carregar a planilha:", e)
        return None

# 🔹 Função para perguntar à IA sobre a planilha
import time

def perguntar_ia(df, pergunta):
    contexto = f"Aqui estão os primeiros dados da planilha:\n{df.head(5).to_string()}"
    prompt = f"{contexto}\n\nCom base nesses dados, {pergunta}"

    model = genai.GenerativeModel("gemini-pro")
    retries = 3
    for i in range(retries):
        try:
            resposta = model.generate_content(prompt)
            return resposta.text
        except Exception as e:
            print(f"Tentativa {i+1} falhou: {e}")
            if i < retries - 1:
                print("Tentando novamente...")
                time.sleep(5)  # Espera 5 segundos antes de tentar novamente
            else:
                print("Erro ao gerar resposta após várias tentativas.")
                return "Erro na solicitação da API."


# 🔹 Teste
if __name__ == "__main__":
    df = carregar_planilha("dados.xlsx")  # Substitua pelo nome do seu arquivo
    if df is not None:
        pergunta = input("Digite sua pergunta sobre a planilha: ")
        resposta = perguntar_ia(df, pergunta)
        print("\nResposta da IA:", resposta)
