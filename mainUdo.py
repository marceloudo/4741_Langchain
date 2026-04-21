from openai import OpenAI, api_key
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

numero_dias = input("Digite o número de dias da viagem: ")
numero_criancas = input("Digite o número de crianças na família: ")
atividade = input("Digite a atividade preferida pela família: ")


prompt = f"crie um roteiro de viagem de {numero_dias} dias, para uma família com {numero_criancas}, que gosta de {atividade}."

cliente = OpenAI(api_key=api_key)

resposta = cliente.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system",
            "content": "você é um agente de viagens especializado em criar roteiros personalizados para famílias. Com base nas informações fornecidas, crie um roteiro de viagem detalhado que inclua atividades, atrações turísticas e sugestões de restaurantes adequados para crianças."
        },
        {
            "role": "user",
            "content": prompt
        }   
    ]
)

resposta_em_texto = resposta.choices[0].message.content

print(resposta_em_texto)