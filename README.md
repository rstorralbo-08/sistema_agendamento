# Sistema de Gestão de Serviços

## 1. Nome do Projeto
**Sistema de Gestão de Serviços e Agendamentos**

---

## 2. Integrantes
* Rodrigo Torralbo

---

## 3. Objetivo
O projeto consiste numa aplicação web desenvolvida com o framework Django para automatizar o controle operacional de uma pequena empresa prestadora de serviços. O sistema centraliza o cadastro de clientes, a gestão do catálogo de serviços e o fluxo de agendamentos, implementando regras de negócio para consistência de horários e integridade referencial, além de fornecer um painel administrativo (dashboard) para acompanhamento dos indicadores principais.

---

## 4. Tecnologias Utilizadas
* **Linguagem:** Python 3.10+
* **Framework Web:** Django 4+ / 5+
  * Django ORM (Mapeamento Objeto-Relacional e Migrations)
  * Django Authentication Framework (LoginView, LogoutView, login_required)
  * Django Forms & ModelForms com validações personalizadas
  * Django Messages Framework (Alertas visuais de sucesso e erro)
  * Python-dotenv (Gestão segura de credenciais e variáveis de ambiente)
* **Base de Dados:** SQLite (padrão) / PostgreSQL / MySQL
* **Front-end / Estilização:** HTML5, CSS3, Bootstrap 5.3 e Bootstrap Icons

---

## 5. Como Instalar e Usar

1. **Clonar o repositório:**
   ```bash
   git clone https://github.com/rstorralbo-08/sistema_agendamento.git
   cd sistema_final

2. **Criar e ativar o ambiente virtual (venv):**

   **Linux / macOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows (PowerShell):**
   ```pwsh
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   **Windows (Command Prompt):**
   ```cmd
   python -m venv .venv
   .venv\Scripts\activate.bat
   ```

3. **Instalar as dependências:**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configurar as Variáveis de Ambiente (.env):**

   **Linux / macOS:**
   ```bash
   cp .env.example .env
   ```

   **Windows:**
   ```pwsh
   copy .env.example .env
   ```

   Abra o ficheiro .env criado e ajuste os parâmetros conforme o seu ambiente:
   ```
   SECRET_KEY=sua_chave_secreta_aqui
   DEBUG=True
   ALLOWED_HOSTS=127.0.0.1,localhost

   # Configurações da Base de Dados
   DB_ENGINE=django.db.backends.sqlite3
   DB_NAME=db.sqlite3
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

5. **Criar o Banco de Dados:**

   ```bash
   cd sistema
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Criar o Usuário Administrador:**

   ```bash
   python manage.py createsuperuser
   ```   

7. **Executar a Aplicação:**

   ```bash
   python manage.py runserver
   ```