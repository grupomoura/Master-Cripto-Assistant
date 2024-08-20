from textwrap import dedent
import streamlit as st
from datetime import datetime
from crewai import Crew
from agents import (MODEL, preco_historico_agente, volume_negociacao_agente,
                    indicadores_tecnicos_agente, sentimento_mercado_agente,
                    noticias_eventos_agente, indicadores_mercado_agente,
                    correlacionamento_agente, analise_fundamentalista_agente)
from tasks import Tasks
import json

def reset_system():
    st.toast("Pesquisa reiniciada!")
    if st.session_state:
        del st.session_state.question
        del st.session_state.disable_input
        st.rerun()

def main():

    if 'disable_input' not in st.session_state:
        st.session_state.disable_input = False

    if 'process_history' not in st.session_state:
        st.session_state.process_history = []

    # Set up the customization options
    st.sidebar.title('Modelos')
    
    if len(st.session_state.process_history) < 1:
        MODEL = st.sidebar.selectbox(
            'Selecione um modelo de IA',
            ['llama3-8b-8192', 'mixtral-8x7b-32768', 'gemma-7b-it', 'llama3-70b-8192'], 
            disabled=st.session_state.disable_input,
        )

    # Histórico de pesquisas
    # st.sidebar.title("Histórico de pesquisas")
    # if len(st.session_state.process_history) > 0:
    #     st.sidebar.markdown("Não há nenhuma pesquisa registrada ainda.")
    # else:
    #     for idx, process in enumerate(st.session_state.process_history):
    #         if "Agent stopped" not in process: 
    #             st.sidebar.status(label=f"**Processo {idx+1}:** {process}", state="complete")

    st.title('Master Cripto Assistant')
    multiline_text = """
    Este sistema de previsão de preços de ativos é composto por uma equipe de agentes especializados, cada um focado em uma área crítica de análise de mercado. Esses agentes utilizam uma combinação de técnicas avançadas e dados em tempo real para fornecer previsões curtas e objetivas sobre a tendência de preço de um ativo específico, como "subir" ou "cair", acompanhadas por uma justificativa concisa.
    """
    st.markdown(multiline_text, unsafe_allow_html=True)

    st.info("A pesquisa pode demorar entre 5 a 10 minutos", icon="ℹ️")

    spacer, col = st.columns([5, 1])  
    with col:  
        st.image('groqcloud_darkmode.png')

    user_question = st.text_input(
        "Qual cripto deseja obter informação:",
        key="question",
        disabled=st.session_state.disable_input,
    )

    # Checa se o usuário já fez uma pergunta e se a entrada está habilitada
    if len(user_question) >= 2 and st.session_state.disable_input == False:
        st.session_state.disable_input = True
        st.rerun()

    # Botão para reiniciar a pesquisa
    # if len(st.session_state.process_history) > 0 and st.session_state.disable_input == False:
    #     if st.button("Nova pesquisa"):     
    #         reset_system()

    # Após o recarregamento, inicia a pesquisa com os agentes
    if st.session_state.disable_input:
        st.toast("Processo 1/8 em andamento...")

        with st.spinner("Aguarde alguns minutos, nossa equipe iniciou uma pesquisa avançada e retornará assim que chegarem a uma conclusão..."):
            preco_historico_task = Tasks.preco_historico_task(user_question=user_question)
            volume_negociacao_task = Tasks.volume_negociacao_task(user_question=user_question)
            indicadores_tecnicos_task = Tasks.indicadores_tecnicos_task(user_question=user_question)
            sentimento_mercado_task = Tasks.sentimento_mercado_task(user_question=user_question)
            noticias_eventos_task = Tasks.noticias_eventos_task(user_question=user_question)
            indicadores_mercado_task = Tasks.noticias_eventos_task(user_question=user_question)
            correlacionamento_task = Tasks.correlacionamento_task(user_question=user_question)
            analise_fundamentalista_task = Tasks.analise_fundamentalista_task(user_question=user_question)

            crew = Crew(
                agents=[
                    preco_historico_agente, 
                    volume_negociacao_agente, 
                    indicadores_tecnicos_agente,
                    sentimento_mercado_agente, 
                    noticias_eventos_agente, 
                    indicadores_mercado_agente, 
                    correlacionamento_agente,
                    analise_fundamentalista_agente
                ],
                tasks=[
                    preco_historico_task, 
                    volume_negociacao_task, 
                    indicadores_tecnicos_task,
                    sentimento_mercado_task, 
                    noticias_eventos_task,
                    indicadores_mercado_task, 
                    correlacionamento_task,
                    analise_fundamentalista_task
                ],
            )

            result = crew.kickoff()
            st.success("Pesquisa concluída!")

            st.markdown(result, unsafe_allow_html=True)

            st.session_state.process_history.append(result)

            with st.status("Relatório detalhado: "):
                if "Agent stopped" not in preco_historico_task.output: 
                    st.markdown(preco_historico_task.output, unsafe_allow_html=True)
                if "Agent stopped" not in volume_negociacao_task.output:
                    st.markdown(volume_negociacao_task.output, unsafe_allow_html=True)
                if "Agent stopped" not in indicadores_tecnicos_task.output:
                    st.markdown(indicadores_tecnicos_task.output, unsafe_allow_html=True)
                if "Agent stopped" not in sentimento_mercado_task.output:
                    st.markdown(sentimento_mercado_task.output, unsafe_allow_html=True)
                if "Agent stopped" not in noticias_eventos_task.output:
                    st.markdown(noticias_eventos_task.output, unsafe_allow_html=True)
                if "Agent stopped" not in indicadores_mercado_task.output:
                    st.markdown(indicadores_mercado_task.output, unsafe_allow_html=True)
                if "Agent stopped" not in correlacionamento_task.output:
                    st.markdown(correlacionamento_task.output, unsafe_allow_html=True)
                if "Agent stopped" not in analise_fundamentalista_task.output:
                    st.markdown(analise_fundamentalista_task.output, unsafe_allow_html=True)
                
            with open('process_history.txt', 'a') as f:
                f.write(f"\n\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {result}")

        if len(st.session_state.process_history) > 0:
            st.sidebar.warning('Os resultados apresentados não são sugestões de investimento, use por sua conta e risco.', icon="⚠️")
            st.info('Atualize a página com F5 para novas pesquisas.', icon="ℹ️")
            st.sidebar.info(dedent(
            """
                ### Aspectos possivelmente considerados: ###\n
                Padrões e tendências,\n
                Volumes de negociação,\n
                Indicadores técnicos,\n
                Sentimento do mercado,\n
                Eventos e notícias,\n
                Índices de mercado,\n
                Correlação entre ativos,\n
                Análise fundamentalista
            """
        ), icon="ℹ️")
        
        # if st.button("Nova pesquisa"):     
        #     reset_system()
            
if __name__ == "__main__":
    main()
