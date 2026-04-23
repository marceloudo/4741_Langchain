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

class Restaurantes(BaseModel):
    cidade: str = Field("A cidade recomendada para visitar.")
    restaurantes: str = Field("Os restaurantes recomendados na cidade.")

parseador_destino = JsonOutputParser(pydantic_object=Destino) # Criando um parseador JSON que utiliza o modelo de dados Destino.
parseador_restaurantes = JsonOutputParser(pydantic_object=Restaurantes) # Criando um parseador JSON que utiliza o modelo de dados Restaurantes.

prompt_cidade = PromptTemplate(
    template= """
    Sugira uma cidade dado meu {interesse}.
    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_destino.get_format_instructions()}
)

prompt_restauantes = PromptTemplate(
    template= """
    Sugira restaurantes populares entre os locais em {cidade}.
    {formato_de_saida}
    """,
    input_variables=["interesse"],
    partial_variables={"formato_de_saida": parseador_restaurantes.get_format_instructions()}
)

prompt_cultural = PromptTemplate(
    template="Sugira atividades e locais culturais em {cidade}",
)

modelo = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.5,
    api_key=api_key
)

cadeia_1 = prompt_cidade | modelo | parseador_destino # Criando a cadeia de processamento, onde o prompt é processado pelo modelo e depois o resultado é parseado para o formato JSON definido pelo modelo de dados Destino.
cadeia_2 = prompt_restauantes | modelo | parseador_restaurantes # Criando a cadeia de processamento, onde o prompt é processado pelo modelo e depois o resultado é parseado para o formato JSON definido pelo modelo de dados Restaurantes.
cadeia_3 = prompt_cultural | modelo | StrOutputParser()

cadeia = cadeia_1 | cadeia_2 | cadeia_3 # Combinando as três cadeias em uma única cadeia de processamento.

resposta = cadeia.invoke(
    {
        "interesse": "praias"
    }
)

print(resposta)