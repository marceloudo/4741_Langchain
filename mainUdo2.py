from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

numero_dias = input("Digite o número de dias da viagem: ")
numero_criancas = input("Digite o número de crianças na família: ")
atividade = input("Digite a atividade preferida pela família: ")

prompt = f"crie um roteiro de viagem de {numero_dias} dias, para uma família com {numero_criancas}, que gosta de {atividade}."

modelo = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=api_key
    )

resposta = modelo.invoke(prompt)
print(resposta.content)