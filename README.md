# OpenFlow — API de Gestão de Workflows e Tarefas

API REST desenvolvida em **Python e Flask** para gerir workflows e tarefas, com autenticação JWT e persistência de dados em SQLite.

Este projeto foi desenvolvido para aplicar conhecimentos de desenvolvimento back-end, organização de APIs, autenticação, modelagem de dados e operações CRUD.

## Tecnologias utilizadas

- **Python** — linguagem principal
- **Flask** — framework para desenvolvimento da API
- **Flask-SQLAlchemy** — integração com o banco de dados
- **SQLite** — armazenamento dos dados
- **Flask-JWT-Extended** — autenticação por tokens JWT
- **Flask-CORS** — configuração de CORS
- **Marshmallow** — suporte à serialização e validação de dados
- **Git e GitHub** — versionamento do projeto

## Funcionalidades

- Cadastro de usuários
- Login com autenticação JWT
- Acesso a perfil protegido por token
- Criação, consulta, atualização e exclusão de workflows
- Criação, consulta, atualização e exclusão de tarefas
- Associação de tarefas a workflows
- Controle de acesso aos workflows e tarefas por usuário
- Persistência de dados em SQLite

## Estrutura do projeto

```text
OpenFlow/
└── backend/
    ├── app.py
    ├── requirements.txt
    ├── .gitignore
    └── app/
        ├── __init__.py
        ├── config.py
        ├── extensions.py
        ├── database/
        │   └── db.py
        ├── models/
        │   ├── user.py
        │   ├── workflow.py
        │   └── task.py
        ├── routes/
        │   ├── auth.py
        │   ├── profile.py
        │   ├── users.py
        │   ├── workflows.py
        │   └── tasks.py
        ├── schemas/
        ├── services/
        └── utils/
```

## Principais endpoints

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/users` | Cadastrar usuário |
| POST | `/login` | Autenticar usuário |
| GET | `/perfil` | Consultar perfil autenticado |
| GET | `/workflows` | Listar workflows |
| POST | `/workflows` | Criar workflow |
| GET | `/workflows/<id>` | Consultar workflow |
| PUT | `/workflows/<id>` | Atualizar workflow |
| DELETE | `/workflows/<id>` | Excluir workflow |
| GET | `/tasks` | Listar tarefas |
| POST | `/tasks` | Criar tarefa |
| GET | `/tasks/<id>` | Consultar tarefa |
| PUT | `/tasks/<id>` | Atualizar tarefa |
| DELETE | `/tasks/<id>` | Excluir tarefa |

As operações protegidas exigem um token JWT válido.

## Como executar localmente

**1. Clonar o repositório**

```bash
git clone https://github.com/Magnum2029/OpenFlow.git
cd OpenFlow/backend
```

**2. Criar e ativar um ambiente virtual**

No Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**3. Instalar as dependências**

```powershell
python -m pip install -r requirements.txt
```

**4. Configurar as variáveis de ambiente**

Criar um arquivo `.env` dentro da pasta `backend` e configurar as variáveis exigidas pela aplicação, incluindo as chaves secretas e a conexão com o banco de dados.

O arquivo `.env` não deve ser enviado ao GitHub.

**5. Iniciar a API**

```powershell
python app.py
```

Por padrão, durante o desenvolvimento local, a API pode ser acessada em:

```text
http://127.0.0.1:5000
```

## Segurança

- Autenticação baseada em JWT
- Proteção de endpoints autenticados
- Verificação de permissões por usuário
- Senhas verificadas por hash
- Variáveis sensíveis armazenadas fora do controle de versão
- Banco de dados local excluído do repositório

## Objetivo do projeto

O OpenFlow foi desenvolvido como projeto prático de back-end para consolidar conhecimentos em Python, Flask, APIs REST, autenticação e bancos de dados relacionais.

O desenvolvimento envolveu a implementação de regras de negócio, relacionamentos entre entidades e controle de acesso aos recursos.

## Autor

**Magnum de Oliveira Santos**

Desenvolvedor Front-End | Back-End Python | Full Stack Júnior

- [GitHub](https://github.com/Magnum2029)
- [LinkedIn](https://www.linkedin.com/in/magnum-de-oliveira-santos-b138041a1/)
- [Portfólio](https://magnum2029.github.io/portfolio-magnum/)
