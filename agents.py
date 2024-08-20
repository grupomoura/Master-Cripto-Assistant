from crewai import Agent, Task, Crew
from langchain_community.tools import DuckDuckGoSearchRun
from textwrap import dedent
import streamlit as st
from langchain_groq import ChatGroq
from crewai_tools import (
    tool,
    WebsiteSearchTool
)

MODEL = "llama3-8b-8192"

API_KEY = st.secrets["GROQ_API_KEY"]
if not API_KEY:
    API_KEY = st.text_input("API KEY GROQ", "Não tem conta GROQ?")
    st.write("Crie sua conta GROQ", API_KEY)
    st.page_link("https://console.groq.com/keys", label="Crie sua conta GROQ", icon="🌎")

    st.error("Please set the GROQ_API_KEY environment variable.")
    exit(1)

llm = ChatGroq(
        temperature=0.1, 
        groq_api_key = st.secrets["GROQ_API_KEY"], 
        model_name=MODEL
)

# Ferramenta de busca no DuckDuckGo e API de buscas
@tool('DuckDuckGoSearch')
def search(search_query: str):
    """Search the web for information on a given topic. 
    The search_query argument of your query must be in string format"""
    return DuckDuckGoSearchRun().run(str(search_query))

# Para fazer rag coletando dados da página
web_rag_tool = WebsiteSearchTool()

# Definição dos agentes
preco_historico_agente = Agent(
    role='Analista de Histórico de Preços',
    goal='Analisar o comportamento passado do ativo.',
    verbose=True,
    memory=False,
    backstory="Você é um analista especializado em identificar padrões e tendências em históricos de preços.",
    llm=llm,
    tools=[search]
)

volume_negociacao_agente = Agent(
    role='Analista de Volume de Negociação',
    goal='Analisar o volume de compras e vendas do ativo.',
    verbose=True,
    memory=False,
    backstory="Você é um analista especializado em interpretar volumes de negociação para determinar a força das tendências.",
    llm=llm,
    tools=[search]
)

indicadores_tecnicos_agente = Agent(
    role='Analista de Indicadores Técnicos',
    goal='Utilizar indicadores técnicos para prever movimentos de preços.',
    verbose=True,
    memory=False,
    backstory="Você é um especialista em indicadores técnicos como RSI, MACD, e bandas de Bollinger.",
    llm=llm,
    tools=[search]
)

sentimento_mercado_agente = Agent(
    role='Analista de Sentimento de Mercado',
    goal='Analisar o sentimento do mercado com base em notícias e mídias sociais.',
    verbose=True,
    memory=False,
    backstory="Você é um especialista em captar e interpretar o sentimento do mercado.",
    llm=llm,
    tools=[search]
)

noticias_eventos_agente = Agent(
    role='Analista de Notícias e Eventos',
    goal='Avaliar o impacto de notícias e eventos recentes no preço do cripto ativo.',
    verbose=True,
    memory=False,
    backstory="Você monitora e analisa eventos e notícias no mercado de criptomoedas que impactam nos preços dos ativos.",
    llm=llm,
    tools=[search]
)

indicadores_mercado_agente = Agent(
    role='Analista de Indicadores de Mercado',
    goal='Analisar índices de mercado como VIX e S&P 500 para prever tendências.',
    verbose=True,
    memory=False,
    backstory="Você é um especialista em interpretar índices de mercado.",
    llm=llm,
    tools=[search] 
)

correlacionamento_agente = Agent(
    role='Analista de Correlacionamento',
    goal='Analisar a correlação entre diferentes ativos para prever movimentos de preços.',
    verbose=True,
    memory=False,
    backstory="Você é um especialista em análise de correlação entre diferentes ativos.",
    llm=llm,
    tools=[search] 
)

analise_fundamentalista_agente = Agent(
    role='Analista Fundamentalista',
    goal='Avaliar o valor intrínseco do ativo para prever se está subvalorizado ou sobrevalorizado.',
    verbose=True,
    memory=False,
    backstory="Você é um especialista em análise fundamentalista, focado em avaliar o valor intrínseco de ativos.",
    llm=llm,
    tools=[search] 
)
