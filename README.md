# 🌿 Plataforma de Visualização com Streamlit

Este repositório contém uma aplicação construída com **Streamlit**, voltada à visualização de dados provenientes de um banco PostgreSQL. A estrutura está organizada para facilitar tanto a colaboração quanto a personalização individual por quem clonar este projeto.

---

## 📁 Estrutura do Projeto

### `application/`

Contém o núcleo da aplicação.

#### 📂 `application/.streamlit/`

- **`secrets.example.toml`**  
  Arquivo modelo com a estrutura necessária para conectar ao banco de dados.
  
  🔐 **Como usar:**  
  - Copie o arquivo e renomeie para `secrets.toml`.
  - Preencha com seu **usuário** e **senha** pessoais.

  ```bash
  cp application/.streamlit/secrets.example.toml application/.streamlit/secrets.toml
  ```

#### 🐍 `app.py`

Arquivo principal da aplicação, responsável por carregar os **componentes visuais**.

* Todos os **componentes desenvolvidos devem ser adicionados aqui**.
* Cada novo componente precisa estar **comentado claramente** e **acompanhado de três corações verdes (💚💚💚)** para facilitar a identificação.

#### 🧪 `test.py`

Utilizado para **testar os componentes da página principal** antes de sua integração no `app.py`.

> Este arquivo pode ser modificado livremente conforme novos testes forem realizados.

---

### 📂 `moreinfo/`

Pasta dedicada a **documentação extra e utilitários**.

* **`Views.sql`** – Contém as *views* SQL utilizadas na aplicação.
* **`ShortCut.md`** – Um guia rápido com atalhos e comandos úteis para quem estiver estudando ou desenvolvendo com Streamlit.

---

## 🚀 Instruções para Rodar o Projeto

1. Crie e ative seu ambiente virtual:

   ```bash
   python -m venv .venv

    # Windows PowerShell
    .venv\Scripts\Activate.ps1   
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Crie seu arquivo `secrets.toml` a partir do exemplo, como explicado acima.

4. Execute a aplicação:

   ```bash
   cd application/
   streamlit run app.py
   ```

---

## 🤝 Contribuições

* Componentes novos devem ser **comentados claramente** e adicionados ao `app.py`.
* Sinta-se à vontade para utilizar o `test.py` durante o desenvolvimento.
* Evite alterar diretamente o arquivo `secrets.example.toml`.
* `secrets.toml` é um arquivo ignorado pelo git.

---
