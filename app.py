from flask import Flask, request, jsonify
from flask_cors import CORS  # Adicionando a importação do CORS
import pandas as pd
import google.generativeai as genai
import time

# 🔹 Configurar a API do Google Gemini
API_KEY = "AIzaSyA5L3HJJdwEsVuo_WGi9ZEY1tg9CKxujZU"
genai.configure(api_key=API_KEY)

app = Flask(__name__)

# Habilitar CORS para todas as rotas
CORS(app)

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

# 🔹 Rota para processar a pergunta
@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        data = request.get_json()  # Receber os dados JSON da requisição
        pergunta = data.get('pergunta', '')

        if not pergunta:
            return jsonify({"resposta": "A pergunta não foi fornecida."}), 400

        # Carregar a planilha
        df = carregar_planilha("dados.xlsx")  # Substitua pelo caminho correto

        if df is not None:
            resposta = perguntar_ia(df, pergunta)
            return jsonify({"resposta": resposta})  # Retorna a resposta como JSON
        else:
            return jsonify({"resposta": "Erro ao carregar a planilha."}), 500

    except Exception as e:
        print(f"Erro na requisição: {e}")
        return jsonify({"resposta": "Ocorreu um erro ao processar a pergunta."}), 500

if __name__ == "__main__":
    app.run(debug=True)
