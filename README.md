# EduTrack API — Sistema de Chamada de Alunos (Django + DRF) 🏫

## 🏛️ Instituições de Fomento e Parceria

Este projeto foi desenvolvido com o apoio e orientação técnica de:

* **Instituto Federal de Brasília (IFB)** 🤝 **Instituto HBR**

**Orientador:** Prof. Claudio Ulisse

---


## Visão Geral

API REST desenvolvida em **Django + Django REST Framework** para modernizar o sistema de chamada de alunos de uma universidade pública. O sistema visa combater o absenteísmo escolar (que afeta cerca de **20–30% dos alunos**, segundo o INEP) por meio de um controle digital eficiente.

Este projeto foi desenvolvido como **Projeto Integrador**, permitindo que professores registrem presença em tempo real e que a coordenação visualize dados estatísticos de evasão escolar.

A API é **segura**, **documentada** e projetada para suportar **relacionamentos acadêmicos complexos**, como Turmas, Matrículas e Presenças.

---

## Funcionalidades Principais

* **Gestão de Pessoas:** Cadastro de Professores e Alunos, incluindo dados demográficos.
* **Gestão Acadêmica:** Criação de Turmas e Matrícula de Alunos (relacionamento N:N).
* **Registro de Chamada:** Marcação de presença ou falta em datas específicas.
* **Liderança de Turma:** Definição de Representante de Turma (relacionamento 1:1).
* **Dashboard Estatístico:** Visualização consolidada de dados da turma e frequência.
* **Documentação Automática:** Interfaces Swagger e Redoc integradas.

---

## Tecnologias Utilizadas 🛠️

| Tecnologia            | Versão | Descrição                                               |
| --------------------- | ------ | ------------------------------------------------------- |
| Python                | 3.10+  | Linguagem de programação utilizada no desenvolvimento   |
| Django                | 5.0    | Framework web responsável pela estrutura base           |
| Django REST Framework | 3.14+  | Framework para construção de APIs RESTful               |
| SQLite                | Padrão | Banco de dados utilizado no ambiente de desenvolvimento |
| drf-spectacular       | Latest | Geração automática de documentação OpenAPI              |
| Pip / Venv            | Padrão | Gerenciamento de pacotes e ambiente virtual             |

---

## Estrutura do Projeto 📂

```text
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
```

---

## Descrição dos Diretórios

| Diretório / Arquivo | Descrição                                                   |
| ------------------- | ----------------------------------------------------------- |
| manage.py           | Script principal do Django para comandos administrativos    |
| db.sqlite3          | Banco de dados local (desenvolvimento)                      |
| config/             | Configurações globais do projeto                            |
| config/settings.py  | Apps instalados, banco de dados e middlewares               |
| core/               | Aplicação principal com regras de negócio acadêmicas        |
| core/models.py      | Definição das entidades (Professor, Turma, Aluno, Presença) |
| core/views.py       | Lógica dos endpoints e ViewSets                             |
| core/serializers.py | Transformação de dados (Python ↔ JSON)                      |
| core/admin.py       | Personalização do painel administrativo                     |

---

## Instalação e Execução ⚙️

### 1. Clonar o repositório

```bash
git clone https://github.com/SEU-USUARIO/nome-do-projeto.git
cd nome-do-projeto
```

### 2. Criar e ativar o ambiente virtual

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install django djangorestframework drf-spectacular
```

### 4. Aplicar migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Criar superusuário

```bash
python manage.py createsuperuser
```

### 6. Executar o servidor

```bash
python manage.py runserver
```

A API estará disponível em:

```
http://127.0.0.1:8000/api/docs
```

---

## Estrutura do Banco de Dados (Modelos) 💾
[Diagrama ER](diagrama_er.png)

### Entidades Principais

#### Professor 🧑‍🏫

* nome
* email
* departamento

Relação: **1:N** com Turma.

#### Turma 📚

* nome
* descricao
* status

Relação: possui **1 Professor** e **N Alunos** (via Matrícula).

#### Aluno 🎒

* nome
* matricula
* email
* curso

Relação: pode estar matriculado em **N Turmas**.

#### Matrícula ✍️

* Tabela associativa entre Aluno e Turma
* Armazena `presenca_acumulada`

#### Presença 📅

* data
* status (Presente / Ausente)

Ligada a uma Matrícula específica.

---

## Endpoints Principais 🌐

**Base URL:**

```
http://127.0.0.1:8000/api/
```

| Recurso       | Método | Endpoint                            | Descrição                  |
| ------------- | ------ | ----------------------------------- | -------------------------- |
| Professores   | GET    | /professores/                       | Lista todos os professores |
| Professores   | POST   | /professores/                       | Cadastra novo professor    |
| Alunos        | POST   | /alunos/                            | Cadastra novo aluno        |
| Turmas        | POST   | /turmas/                            | Cria nova turma            |
| Matrícula     | POST   | /turmas/{id}/matricular-aluno/      | Matricula aluno            |
| Representante | PUT    | /turmas/{id}/definir-representante/ | Define líder da turma      |
| Presença      | POST   | /presencas/                         | Registra presença ou falta |

---

## Endpoint Especial: Dashboard Completo 📈

Fornece uma visão consolidada de uma turma específica.

```
GET /api/turmas/{id}/dashboard/
```

### Retorna:

* Dados da Turma
* Professor responsável
* Representante da turma
* Lista de alunos matriculados com presença acumulada

---

## Documentação Automática 📖

Disponível via **drf-spectacular**:

* Swagger UI: `http://127.0.0.1:8000/api/docs/`
* Redoc: `http://127.0.0.1:8000/api/redoc/`
* Schema JSON: `http://127.0.0.1:8000/api/schema/`

---

## Acesso ao Admin 🔐

Painel administrativo para gestão manual dos dados:

```
http://127.0.0.1:8000/admin/
```

---

## Objetivo do Projeto 💡

Integrar conhecimentos de:

* Modelagem de Banco de Dados Relacional
* Desenvolvimento de APIs RESTful com Django
* Serialização e Views complexas
* Documentação de Software

**Foco:** solução real para gestão educacional e redução da evasão escolar.

---

## Autenticação e Perfis 🔒

A API suporta múltiplos perfis de acesso:

* **Administrador:** acesso total (CRUD completo)
* **Professor:** acesso às suas turmas e registros de presença
* **Aluno:** acesso de leitura ao próprio histórico

Atualmente, para desenvolvimento e testes, são utilizados:

* `SessionAuthentication`
* `BasicAuthentication`

---

## Créditos

Developed by **Adriana Santos**
