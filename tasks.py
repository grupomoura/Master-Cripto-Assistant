# Definição das tasks
from datetime import datetime
from textwrap import dedent
from crewai import Task
import streamlit as st
from langchain_community.tools import DuckDuckGoSearchRun
from agents import preco_historico_agente, volume_negociacao_agente, indicadores_tecnicos_agente, sentimento_mercado_agente, noticias_eventos_agente, indicadores_mercado_agente, correlacionamento_agente, analise_fundamentalista_agente

from crewai_tools import (
    tool,
    WebsiteSearchTool
)

# Ferramenta de busca no DuckDuckGo e API de buscas
@tool('DuckDuckGoSearch')
def search(search_query: str):
    """Search the web for information on a given topic. 
    The search_query argument of your query must be in string format"""
    return DuckDuckGoSearchRun().run(str(search_query))

web_rag_tool = WebsiteSearchTool()

step = 1
total_steps = 8
def agent_callback(output):
    global total_steps
    global step
    step += 1
    st.toast(f"Processo {step}/{total_steps} em andamento...")

# # Callback para exibir o progresso dos agentes
# def agent_callback(agent_name, task_name, step, total_steps):
#     st.toast(f"Agente: {agent_name} {step}/{total_steps} - {task_name} em andamento.")

class Tasks():
    def preco_historico_task(user_question):
        return Task(
            description=(
                f"Coletar e analisar o histórico de preços do ativo {user_question} para identificar tendências e padrões no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista de Histórico de Preços/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                """
                Agente: Analista de Histórico de Preços
                Resultado: subir ou cair
                Motivo: Informe o motivo em uma frase
                """
            ),
            tools=[search],
            callback = agent_callback,
            agent=preco_historico_agente,
            
            )

    def volume_negociacao_task(user_question):
        return Task(
            description=(
                f"Analisar o volume de negociação do ativo {user_question} para determinar a força da tendência no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista de Volume de Negociação/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                """
                Agente: Analista de Volume de Negociação
                Resultado: subir ou cair
                Motivo: Informe o motivo em uma frase
                """
            ),
            tools=[search, web_rag_tool],
            callback = agent_callback,
            agent=volume_negociacao_agente,
            
        )

    def indicadores_tecnicos_task(user_question):
        return Task(
            description=(
                f"Analisar dados do ativo {user_question} nos principais indicadores técnicos como RSI, MACD, e bandas de Bollinger para prever movimentos de preços no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista de Indicadores Técnicos/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                """
                Agente: Analista de Indicadores Técnicos
                Resultado: subir ou cair
                Motivo: Informe o motivo em uma frase
                """
            ),
            tools=[search, web_rag_tool],
            callback = agent_callback,
            agent=indicadores_tecnicos_agente,
            
        )

    def sentimento_mercado_task(user_question):
        return Task(
            description=(
                f"Analisar o sentimento do mercado com base em notícias e mídias sociais para prever o movimento do preço do ativo {user_question} no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista de Sentimento de Mercado/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                """
                Agente: Analista de Sentimento de Mercado
                Resultado: subir ou cair
                Motivo: Informe o motivo em uma frase
                """
            ),
            tools=[search, web_rag_tool],
            callback = agent_callback,
            agent=sentimento_mercado_agente,
            
        )

    def noticias_eventos_task(user_question):
        return Task(
            description=(
                f"Avaliar o impacto de notícias e eventos recentes no preço do ativo {user_question} no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista de Notícias e Eventos/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                """
                Agente: Analista de Notícias e Eventos
                Resultado: subir ou cair
                Motivo: Informe o motivo em uma frase
                """
            ),
            tools=[search, web_rag_tool],
            callback = agent_callback,
            agent=noticias_eventos_agente,
            
        )

    def indicadores_mercado_task(user_question):
        return Task(
            description=(
                f"Analise de forma criativa índices de mercado como VIX e S&P 500 para prever tendências do preço do ativo {user_question} no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista de Indicadores de Mercado/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                """
                Agente: Analista de Indicadores de Mercado
                Resultado: subir ou cair
                Motivo: Informe o motivo em uma frase
                """
            ),
            tools=[search, web_rag_tool],
            callback = agent_callback,
            agent=indicadores_mercado_agente,
            
        )

    def correlacionamento_task(user_question):
        return Task(
            description=(
                f"Analisar a correlação entre BTC, {user_question}, e o dólar americano para prever movimentos de preços no ativo {user_question} no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista de Correlacionamento/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                """
                Agente: Analista de Correlacionamento
                Resultado: subir ou cair
                Motivo: Informe o motivo em uma frase
                """
            ),
            tools=[search, web_rag_tool],
            callback = agent_callback,
            agent=correlacionamento_agente,
            
        )

    def analise_fundamentalista_task(user_question):
        return Task(
            description=(
                f"Avaliar o valor intrínseco do ativo {user_question} para prever se está subvalorizado ou sobrevalorizado identificando padrões de alteração no curto prazo entre 24hs a 7 dias."
                "Seu resultado deve ser 'subir' ou 'cair', com uma frase explicando o motivo."
                "Cite as fontes de onde tirou as informações."
                "Responda usando markdown com o texto em português do Brasil."
            ),
            # output_file=f"analysis/Analista Fundamentalista/{datetime.now().strftime('%Y%m%d%H%M%S')}_{user_question}.md",
            expected_output=dedent(
                f"""
                
                ## Resposta principal
                Em um apanhado geral, informe o veredito explicando quais critérios foram considerados
                e quais os prazos aproximados numa margem entre 24hs e 7 dias para possíveis alterações no preço do ativo {user_question}
                
                ## Resultado: subir ou cair
                Informe um fato marcante ou muito importante que poderia influenciar uma venda ou uma compra nos próximos dias,
                considerando a data atual que hoje é {datetime.now()}.

                ## Fontes de pesquisa:
                - https://finance.yahoo.com/quote/{user_question}/profile
                - https://www.investopedia.com/articles/stock-market/value-investment-stocks/what-is-intrinsic-value-stock.asp
                - https://www.investopedia.com/articles/economics/value-investment-stocks.asp
                - https://www.investopedia.com/articles/economics/investment-analysis/1001-what-is-value-investment.asp
                - https://www.investopedia.com/terms/v/value-investment.asp
                - https://www.investopedia.com/articles/trading/062513/how-to-identify-value-stocks.asp
                - https://www.investopedia.com/articles/trading/102315/value-investment-stocks-
  
                """
                ),
            tools=[search, web_rag_tool],
            callback = agent_callback,
            agent=analise_fundamentalista_agente,
            
        )
