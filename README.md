<div align="center">

EduTrack API — Sistema de Chamada de Alunos (Django + DRF) 🏫

🏢 Instituições de Fomento e Parceria

<p>Este projeto foi desenvolvido com o apoio e orientação técnica de:</p>

Instituto Federal de Brasília (IFB) ✨ Instituto HBR

Orientador: Prof. Claudio Ulisse

</div>

📋 Sumário

Visão Geral

Funcionalidades Principais

Tecnologias Utilizadas

Estrutura do Projeto

Descrição dos Diretórios

Instalação e Execução

Estrutura do Banco de Dados (Modelos)

Endpoints Principais

Endpoint Especial: Dashboard Completo

Documentação Automática

Acesso ao Admin

Objetivo do Projeto

Autenticação e Perfis

Visão Geral

API REST desenvolvida em Django + Django REST Framework para modernizar o sistema de chamada de alunos de uma universidade pública. O sistema visa combater o absenteísmo escolar (que afeta cerca de 20-30% dos alunos, segundo o INEP) através de um controle digital eficiente.

Este projeto foi desenvolvido como Projeto Integrador, permitindo que professores registrem presença em tempo real e a coordenação visualize dados estatísticos de evasão escolar.

A API é segura, documentada e desenhada para suportar relacionamentos acadêmicos complexos (Turmas, Matrículas e Presenças).

Funcionalidades Principais

Gestão de Pessoas: Cadastro de Professores e Alunos (com dados demográficos).

Gestão Acadêmica: Criação de Turmas e Matrícula de Alunos (vínculo N:N).

Registro de Chamada: Marcação de presença ou falta em datas específicas.

Liderança de Turma: Definição de Representante de Turma (vínculo 1:1).

Dashboard Estatístico: Visualização consolidada da turma e frequência.

Documentação Automática: Interface Swagger e Redoc integradas.

Tecnologias Utilizadas 🛠️

Tecnologia

Versão

Descrição

Python

3.10+

Linguagem de programação utilizada no desenvolvimento.

Django

5.0

Framework web responsável pela estrutura base.

Django REST Framework

3.14+

Framework para construção de APIs RESTful.

SQLite

Padrão

Banco de dados utilizado no ambiente de desenvolvimento.

drf-spectacular

Latest

Geração automática de documentação OpenAPI.

Pip / Venv

Padrão

Gerenciamento de pacotes e ambiente virtual.

Estrutura do Projeto 📂

sistema_chamada/
├── manage.py
├── db.sqlite3
├── README.md
├── diagrama_er.png
│
├── config/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── core/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│
└── venv/


Descrição dos Diretórios

Diretório / Arquivo

Descrição

manage.py

Script principal do Django para execução de comandos administrativos.

db.sqlite3

Banco de dados local (desenvolvimento).

config/

Configurações globais do projeto (settings, rotas principais).

config/settings.py

Configurações de apps instalados, banco de dados e middlewares.

core/

Aplicação principal contendo as regras de negócio acadêmicas.

core/models.py

Definição das tabelas (Professor, Turma, Aluno, Presença).

core/views.py

Lógica dos endpoints e ViewSets da API.

core/serializers.py

Transformação de dados (Python ↔ JSON).

core/admin.py

Personalização do Painel Administrativo do Django.

Instalação e Execução ⚙️

1. Clonar o repositório

git clone [https://github.com/SEU-USUARIO/nome-do-projeto.git](https://github.com/SEU-USUARIO/nome-do-projeto.git)
cd nome-do-projeto


2. Criar e ativar o ambiente virtual

# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate


3. Instalar dependências

pip install django djangorestframework drf-spectacular


4. Aplicar migrações (Criar Banco de Dados)

python manage.py makemigrations
python manage.py migrate


5. Criar superusuário (Admin)

python manage.py createsuperuser


6. Rodar servidor

python manage.py runserver


A API estará disponível em: http://127.0.0.1:8000/api/

Estrutura do Banco de Dados (Modelos) 💾

<div align="center"> <img src="diagrama_er.png" alt="Diagrama ER" width="600px"> </div>

Entidades Principais

Professor 🧑‍🏫

nome, email, departamento

Relação: 1:N com Turma.

Turma 📚

nome, descricao, status

Relação: Tem 1 Professor e N Alunos (via Matrícula).

Aluno 🎒

nome, matricula, email, curso

Relação: Pode estar em N Turmas.

Matrícula ✍️

Tabela associativa que liga Aluno à Turma.

Armazena presenca_acumulada.

Presença 📅

data, status (Presente/Ausente)

Ligada a uma Matrícula específica.

Endpoints Principais 🌐

Base URL: http://127.0.0.1:8000/api/

Recurso

Método

Endpoint

Descrição

Professores

GET

/professores/

Lista todos os professores.



POST

/professores/

Cadastra novo professor.

Alunos

POST

/alunos/

Cadastra novo aluno.

Turmas

POST

/turmas/

Cria nova turma.

Matrícula

POST

/turmas/{id}/matricular-aluno/

Insere aluno na turma.

Representante

PUT

/turmas/{id}/definir-representante/

Define líder da sala.

Presença

POST

/presencas/

Registra falta/presença (Dia + Matrícula).

Endpoint Especial: Dashboard Completo 📈

Mostra a visão 360º de uma turma específica, já consolidada.

URL: GET /api/turmas/{id}/dashboard/

O que retorna:

Dados da Turma (Nome, Status)

Dados do Professor Responsável

Dados do Representante

Lista de Alunos Matriculados (com Presença Acumulada)

Documentação Automática 📖

Disponível graças ao drf-spectacular:

Swagger UI: http://127.0.0.1:8000/api/docs/

Redoc: http://127.0.0.1:8000/api/redoc/

Schema JSON: http://127.0.0.1:8000/api/schema/

Acesso ao Admin 🔐

Para gestão manual dos dados (backoffice):
http://127.0.0.1:8000/admin/

Objetivo do Projeto 💡

Este projeto visa integrar conhecimentos de:

Modelagem de Banco de Dados Relacional.

Desenvolvimento de APIs RESTful com Django.

Serialização e Views complexas.

Documentação de Software.

Foco: Solução real para gestão educacional e redução de evasão.

Autenticação e Perfis 🔒

A API foi projetada para suportar diferentes perfis de acesso:

Administrador: Acesso total (CRUD de Professores, Turmas, Alunos).

Professor: Acesso às suas turmas e registro de presenças.

Aluno: Acesso de leitura ao seu histórico.

Atualmente, para fins de desenvolvimento e testes no Swagger, utiliza-se Autenticação por Sessão (SessionAuthentication) e Autenticação Básica (BasicAuthentication).

<div align="center">
Developed by <strong>[Seu Nome Aqui]</strong> 👋
</div>
