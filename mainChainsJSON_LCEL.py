from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser # Incluindo o JSonOutputParser.  
from pydantic import Field, BaseModel # Incluindo o BaseModel e Field do Pydantic para criar um modelo de dados.
from dotenv import load_dotenv
from langchain.globals import set_debug # Incluindo a função para configurar o modo de depuração.
import os

# from main import Destino

set_debug(True) # Ativando o modo de depuração para obter mais informações sobre

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

class Destino(BaseModel): 
    cidade: str = Field("A cidade recomendada para visitar.")
    motivo: str = Field("O motivo pelo qual a cidade é recomendada.")

parseador = JsonOutputParser(pydantic_object=Destino) # Criando um parseador JSON que utiliza o modelo de dados Destino.

prompt_cidade = PromptTemplate(
    template= """
    Sugira uma cidade dado meu {interesse}.
    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador.get_format_instructions()}
)


modelo = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=api_key
)

cadeia = prompt_cidade | modelo | parseador # Criando a cadeia de processamento, onde o prompt é processado pelo modelo e depois o resultado é parseado para o formato JSON definido pelo modelo de dados Destino.

resposta = cadeia.invoke(
    {
        "interesse": "praias"
    }
)


print(resposta)