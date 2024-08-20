import streamlit as st
from datetime import datetime
from crewai import Agent, Task, Crew
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
from textwrap import dedent
from agents import MODEL, preco_historico_agente, volume_negociacao_agente, indicadores_tecnicos_agente, sentimento_mercado_agente, noticias_eventos_agente, indicadores_mercado_agente, correlacionamento_agente, analise_fundamentalista_agente

from tasks import Tasks
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

def main():

    def reset_system():
        st.text("reset_system acessado")
        print("reset_system acessado")
        if st.session_state:
            st.text(st.session_state)
            del st.session_state.question
            st.rerun()
        else:
            st.text(st.session_state)

    # Inicializando st.session_state.disable_input se não existir
    if 'disable_input' not in st.session_state:
        st.session_state.disable_input = False

    # Set up the customization options
    st.sidebar.title('Modelos')

    if 'process_history' not in st.session_state or len(st.session_state['process_history']) == 0:
        MODEL = st.sidebar.selectbox(
            'Selecione um modelo de IA',
            ['llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it', 'llama3-70b-8192']
        )    
  
    # Histórico de processos
    if 'process_history' not in st.session_state or len(st.session_state['process_history']) == 0:
        st.session_state['process_history'] = []
        st.sidebar.title(dedent(
            """
            **Histórico de pesquisas**
            
            Não há nenhuma pesquisa registrada ainda. Clique no botão 'Nova pesquisa' para iniciar uma nova pesquisa.
            """
        ))
    else:
        if len(st.session_state['process_history']) >= 1:
            st.sidebar.title('Histórico de pesquisas')

        for idx, process in enumerate(st.session_state['process_history']):
            st.sidebar.status(label=f"**Processo {idx+1}:** {process}", state="complete")
            # st.sidebar.markdown(f"**Processo {idx+1}:** {process}")

    # Streamlit UI
    st.title('Master Cripto Assistant')
    multiline_text = """
    
    Este sistema de previsão de preços de ativos é composto por uma equipe de agentes especializados, cada um focado em uma área crítica de análise de mercado. Esses agentes utilizam uma combinação de técnicas avançadas e dados em tempo real para fornecer previsões curtas e objetivas sobre a tendência de preço de um ativo específico, como "subir" ou "cair", acompanhadas por uma justificativa concisa.
    """

    st.markdown(multiline_text, unsafe_allow_html=True)

    # Display the Groq logo
    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')

    user_question = st.text_input(
        "Qual cripto deseja obter informação:",
        key="question",
        disabled=st.session_state.disable_input,
        on_change=lambda: st.session_state.update({'disable_input': True}),
    )

    if len(user_question) >= 2:
        # Inicia a pesquisa com cada agente
        with st.spinner("Aguarde alguns minutos, nossa equipe iniciou uma pesquisa avançada e retornará assim que chegarem a uma conclusão..."):
            # Desativando input 
            st.session_state.disable_input = True
            
            # Definição das tasks
            preco_historico_task = Tasks.preco_historico_task(user_question=user_question)
            # volume_negociacao_task = Tasks.volume_negociacao_task(user_question=user_question)
            # indicadores_tecnicos_task = Tasks.indicadores_tecnicos_task(user_question=user_question)
            # sentimento_mercado_task = Tasks.sentimento_mercado_task(user_question=user_question)
            # noticias_eventos_task = Tasks.noticias_eventos_task(user_question=user_question)
            # indicadores_mercado_task = Tasks.noticias_eventos_task(user_question=user_question)
            # correlacionamento_task = Tasks.correlacionamento_task(user_question=user_question)
            # analise_fundamentalista_task = Tasks.analise_fundamentalista_task(user_question=user_question)

            # Definição do Crew
            crew = Crew(
                agents=[
                    preco_historico_agente, 
                    # volume_negociacao_agente, 
                    # indicadores_tecnicos_agente,
                    # sentimento_mercado_agente, 
                    # noticias_eventos_agente, 
                    # indicadores_mercado_agente, 
                    # correlacionamento_agente,
                    # analise_fundamentalista_agente
                ],
                tasks=[
                    preco_historico_task, 
                    # volume_negociacao_task, indicadores_tecnicos_task,
                    # sentimento_mercado_task, noticias_eventos_task,
                    # indicadores_mercado_task, correlacionamento_task,
                    # analise_fundamentalista_task
                ],
            )

            result = crew.kickoff()
            st.success("Pesquisa concluída!")

            # Exibe o resultado na tela
            st.markdown(result, unsafe_allow_html=True)

            # Adiciona o resultado ao histórico de processos
            st.session_state['process_history'].append(result)

            with st.status("Relatório detalhado: "):
                st.markdown(preco_historico_task.output, unsafe_allow_html=True)
                # st.markdown(volume_negociacao_task.output, unsafe_allow_html=True)
                # st.markdown(indicadores_tecnicos_task.output, unsafe_allow_html=True)
                # st.markdown(sentimento_mercado_task.output, unsafe_allow_html=True)
                # st.markdown(noticias_eventos_task.output, unsafe_allow_html=True)
                # st.markdown(indicadores_mercado_task.output, unsafe_allow_html=True)
                # st.markdown(correlacionamento_task.output, unsafe_allow_html=True)
                # st.markdown(analise_fundamentalista_task.output, unsafe_allow_html=True)

            # Salva o histórico de processos em um arquivo
            from pathlib import Path
            Path('process_history.txt').touch()  # Cria o arquivo se não existir
            with open('process_history.txt', 'a') as f:
                f.write(f"\n\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {result}")

            # # Atualiza a data e hora do último relatório
            # st.sidebar.subheader(f"Ultima atualização: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if 'process_history' in st.session_state and len(st.session_state.process_history) > 0:
            # Botão para reiniciar a aplicação
            if st.sidebar.button('Nova pesquisa'):
                reset_system()
                st.session_state.disable_input = False
        
        if len(st.session_state.process_history) > 0 and st.session_state.disable_input == True:
            # Adiciona um botão para limpar o histórico de processos
            if st.sidebar.button('Limpar histórico'):
                del st.session_state.process_history
                st.success("Histórico limpo com sucesso!")

            # Adiciona um botão para avaliar o relatório
            sentiment_mapping = ["one", "two", "three", "four", "five"]
            selected = st.feedback("stars")
            if selected is not None:
                st.markdown(f"Obrigado por avaliar!")
            


        if len(st.session_state.process_history) > 0:
            st.sidebar.warning('Os resultados apresentados não são sugestões de investimento, use por sua conta e risco.', icon="⚠️")
            st.info('Atualize a página com F5 para novas pesquisas.', icon="ℹ️")
        st.sidebar.info(dedent(
            """
                Aspectos possivelmente considerados:
                Padrões e tendências,
                Volumes de negociação,  
                Indicadores técnicos,
                Sentimento do mercado,
                Eventos e notícias,
                Índices de mercado,
                Correlação entre ativos,
                Análise fundamentalista
            """
        ), icon="ℹ️")

# streamlit run app.py
if __name__ == "__main__":
    main()
