# 🌿 Plataforma de Visualização com Streamlit

Este repositório contém uma aplicação construída com **Streamlit**, voltada à visualização de dados provenientes de um banco PostgreSQL. A estrutura está organizada para facilitar tanto a colaboração quanto a personalização individual por quem clonar este projeto.

---

## 📁 Estrutura do Projeto

### `./application/`

Contém o núcleo da aplicação. Modularizado para melhorar a manutenção e a legibilidade do código.

#### 📂 `application/.streamlit/`

- **`secrets.example.toml`**  
  Arquivo modelo com a estrutura necessária para conectar ao banco de dados.
  
  🔐 **Como usar:**  
  - Copie o arquivo, cole no mesmo diretório e o renomeie para `secrets.toml`.
  - Preencha com seu **usuário** e **senha** pessoais de acesso ao banco.

```bash
   cp application/.streamlit/secrets.example.toml application/.streamlit/secrets.toml
```
#### 🐍 app.py

Arquivo principal da aplicação Streamlit.
Integra os componentes visuais com as consultas ao banco e as funções auxiliares.

    Deve ser executado com:
    cd application && streamlit run app.py

#### 🧪 test.py

Utilizado para testar funcionalidades e componentes individuais da interface antes de sua inclusão definitiva no app.py.

#### 📦 Módulos auxiliares dentro de application/
📄 db.py
Responsável por estabelecer a conexão com o banco de dados PostgreSQL utilizando os parâmetros do arquivo secrets.toml.

📄 queries.py
Contém todas as consultas SQL estruturadas da aplicação, separadas por funcionalidade (poluentes, temperatura, umidade, bairros etc).

📄 charts.py
Armazena as funções responsáveis pela criação dos gráficos com Altair, separando a lógica de visualização da lógica de dados.

📄 utils.py
Inclui funções auxiliares genéricas, como o tratamento de colunas de datas e transformações reutilizáveis.

📄 __init__.py
Arquivo necessário para tornar a pasta application/ um módulo Python válido, permitindo a importação dos submódulos entre si.

### 📂 moreInfo/

Pasta dedicada a documentação extra e utilitários.
🪟 Views.sql – Contém as views SQL utilizadas na aplicação.

🚶‍♂️‍➡️ShortCut.md – Um guia rápido com atalhos e comandos úteis para quem estiver estudando ou desenvolvendo com Streamlit.

## 🚀 Instruções para Rodar o Projeto

Mude para o diretório do projeto. 
O caminho pode ser descoberto clicando com o botão direito do mouse na pasta raiz do projeto e selecionando "copiar como caminho":

```bash
   cd 'caminho_no_seu_computador_para_a_pasta_do_projeto/weather-sync-dashboard'
```

Então crie seu ambiente virtual na pasta raiz do projeto:
```bash
   python -m venv .venv
```

**IMPORTANTE**: garanta que o interpretador correto do python está selecionado! O interpretador selecionado deve ser o que se encontra dentro da pasta do ambiente virtual:
Windows deve ser: ".venv\Scripts\python.exe"
Linux/macOS: ".venv/bin/python"
Não utilize o interpretador na raiz da instalação do Python!

Em seguida, ative o ambiente virtual: 
```bash
   ## PARA LINUX/macOS:
   # Na pasta raiz do projeto:
   activate 
   # Ou, caso não funcione, ainda na raiz:
   .venv\Scripts\activate.bat

   ## PARA WINDOWS PowerShell:
   .venv\Scripts\Activate.ps1
```

Por fim, se deu tudo certo, instale as dependências usando o venv na raiz do projeto:
```bash
   pip install -r requirements.txt
```

Se você criou seu arquivo secrets.toml a partir do exemplo, como explicado anteriormente, é só executar a aplicação:

```bash
   # A partir da raiz do projeto:
   cd application/
   streamlit run app.py
```

O seu navegador principal será aberto e mostrará os gráficos streamlit do Weather Sync!