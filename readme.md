Aqui está uma documentação README para o seu projeto compatível com o GitHub. A documentação inclui todos os detalhes necessários, incluindo as instruções sobre como configurar as chaves de API no arquivo `.streamlit/secrets.toml`.

---

# Master Cripto Assistant

Este repositório contém o código para o **Master Cripto Assistant**, um sistema avançado de previsão de preços de ativos criptográficos. O sistema é composto por uma equipe de agentes especializados, cada um focado em uma área crítica de análise de mercado. Esses agentes utilizam técnicas avançadas e dados em tempo real para fornecer previsões curtas e objetivas sobre a tendência de preço de ativos específicos, acompanhadas por justificativas concisas.

## Funcionalidades

- **Previsão de Preços:** Previsões sobre a tendência de preço de um ativo específico.
- **Análise Completa:** Utilização de múltiplas técnicas de análise, incluindo histórico de preços, volume de negociação, indicadores técnicos, sentimento do mercado, notícias e eventos, indicadores de mercado, correlação entre ativos e análise fundamentalista.
- **Histórico de Pesquisas:** Armazenamento e exibição do histórico de processos de pesquisa realizados.

## Tecnologias Utilizadas

- **Python 3.9+**
- **Streamlit**
- **CrewAI** para a orquestração dos agentes
- **Bibliotecas auxiliares:** datetime, json, entre outras.

## Requisitos

- **API Keys:** Certifique-se de configurar suas chaves de API no arquivo `.streamlit/secrets.toml`. Estas chaves são necessárias para a operação dos modelos de IA e para acessar recursos de terceiros.

### Exemplo de `secrets.toml`

```toml
# Exemplo de configuração do arquivo .streamlit/secrets.toml
[api_keys]
OPENAI_API_KEY = "sua-chave-openai"
GROQ_API_KEY="sua-chave-groq" #https://console.groq.com/keys
```

## Como Executar

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/seu-usuario/master-cripto-assistant.git
   cd master-cripto-assistant
   ```

2. **Instale as dependências:**

   Certifique-se de estar em um ambiente virtual.

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure as chaves de API:**

   Crie um arquivo `.streamlit/secrets.toml` na raiz do repositório e adicione suas chaves de API.

4. **Execute a aplicação:**

   Inicie a aplicação Streamlit com o seguinte comando:

   ```bash
   streamlit run app.py
   ```

## Estrutura do Projeto

- `agents.py`: Contém a definição dos agentes que realizam a análise.
- `tasks.py`: Define as tarefas que os agentes devem executar.
- `app.py`: Arquivo principal que configura a interface do usuário usando Streamlit e executa o fluxo de trabalho da CrewAI.

## Uso

1. Acesse a interface do usuário e insira o nome de um ativo cripto no campo de pesquisa.
2. A equipe de agentes iniciará uma pesquisa avançada e retornará com uma previsão e análise detalhadas.
3. O histórico de processos de pesquisa é armazenado e pode ser acessado na barra lateral.

## Avisos

- **Isenção de Responsabilidade:** Os resultados apresentados pelo Master Cripto Assistant não são sugestões de investimento. Use por sua conta e risco.
- **Reinicialização da Aplicação:** Para realizar novas pesquisas, atualize a página com `F5`.

---
