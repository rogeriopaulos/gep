# Instalação

## Sumário

- [Pré-requisitos](#pre-requisitos)
- [Deploy em ambiente de Desenvolvimento](#deploy-em-ambiente-de-desenvolvimento)
- Deploy em ambiente de Produção:
    - [Deploy sem Docker](#deploy-sem-docker)
    - [Deploy com Docker](#deploy-com-docker)

## Pré-requisitos

_Os pré-requisitos listados a seguir tem por base as tecnologias/versões utilizadas durante o desenvolvimento da aplicação, bem como àquelas empregadas em ambiente de produção._


**Hardware:**

- Processador de 2 núcleos
- 2GB de memória RAM
- 20GB de armazenamento mínimo*
- Acesso externo via internet

_* Considera somente o espaço mínímo necessário para executar a aplicação._

**Software:**

- Desenvolvimento:

    -   SO CentOS 7.x86_64 ou Ubuntu 18.04.3 LTS
    -   Python 3.8+
    -   Postgresql 10.x+

- Produção:

    - Ambiente de produção sem docker:
        - SO CentOS 7.x86_64 ou Ubuntu 18.04.3 LTS
        - Python 3.8
        - Postgresql 10.x | 11.x
        - Nginx 1.13.x ou superior

    - Ambiente de produção com docker:
        - SO CentOS 7.x86_64 ou Ubuntu 18.04.3 LTS
        - Docker-ce 18.xx.x ou superior
        - docker-compose 1.24.x ou superior

## Deploy em ambiente de Desenvolvimento

Os procedimentos abaixo descritos foram realizados no SO CentOS 7.

_Frise-se que a presente instrução tem o intuito de fornecer as linhas gerais do processo de implantação da aplicação GEP em um ambiente de desenvolvimento - preferencialmente em uma máquina local, cabendo ao responsável a escolha final de segui-lo ou optar por soluções mais condizentes com a estrutra a qual dispõe._

Uma vez atendidos os requisitos de Hardware e Software relacionados, execute os seguintes passos:

**1)** Configure as variáveis de ambiente abaixo listadas no seu SO

```
export DJANGO_SETTINGS_MODULE=settings.local
export POSTGRES_HOST=<endereço_do_host_do_BD>
export POSTGRES_PORT=<porta_em_execução_do_BD>
export POSTGRES_DB=<nome_do_BD>
export POSTGRES_USER=<usuário_do_BD>
export POSTGRES_PASSWORD=<senha_do_BD>
```

**2)** Crie um ambiente virtual para projetos Python e ative-o

Para maiores informações, acesse esse [tutorial](https://www.treinaweb.com.br/blog/criando-ambientes-virtuais-para-projetos-python-com-o-virtualenv/) ou pesquise nos sites de busca sobre o tema.

**3)** Instale as dependências do projeto

```
pip install -r requirements/local.txt
```

**4)** Crie as tabelas necessárias no banco de dados

```
python manage.py makemigrations  # caso não haja arquivos de migração

python manage.py migrate
```

**5)** Crie um superusuário

```
python manage.py createsuperuser
```

Em seguida, forneça os dados solicitados.

**6)** Execute o servidor local

```
python manage.py runserver
```

**7)** Preencha as tabelas de normalização conforme demonstrado na seção [Normalização](NORMALIZACAO.md).

**8)** Crie os grupos e associe as permissões específicas conforme demonstrado na seção [Grupos e Permissões](GRUPOS.md).

Pronto! Com o servidor rodando, acesse a url "localhost:8000/gep" no seu navegador e você deverá acessar a página inicial na sua máquina local.

## Deploy em ambiente de Produção

### Deploy sem Docker

Os procedimentos abaixo descritos foram realizados no SO CentOS 7.

**1)** Configure as variáveis de ambiente abaixo listadas no seu SO

```
# General
# ------------------------------------------------------------------------------
export DJANGO_SETTINGS_MODULE=settings.production
export DJANGO_SECRET_KEY=<secret-key> # ex: EeMHtbY0JNIV9lZQaKpeeMjBTx3k3i0Chj
export DJANGO_ADMIN_URL=<url> # ex: admin
export DJANGO_ALLOWED_HOSTS=<ip_externo_do_host>

# Security
# ------------------------------------------------------------------------------
# TIP: better off using DNS, however, redirect is OK too
export DJANGO_SECURE_SSL_REDIRECT=False

# Email
# ------------------------------------------------------------------------------
export EMAIL_HOST=<host_smtp> # ex: smtp.gmail.com
export EMAIL_PORT=<port>
export EMAIL_HOST_USER=<host_user>
export EMAIL_HOST_PASSWORD=<password>

# Gunicorn
# ------------------------------------------------------------------------------
export WEB_CONCURRENCY=4

# dajngo-maintenance_mode
# ------------------------------------------------------------------------------
export MAINTENANCE_ADMIN_URL=<url_do_painel_admin>+"login" # ex: adminlogin

# PostgreSQL
# ------------------------------------------------------------------------------
export POSTGRES_HOST=<endereço_do_host_do_BD>
export POSTGRES_PORT=<porta_em_execução_do_BD>
export POSTGRES_DB=<nome_do_BD>
export POSTGRES_USER=<usuário_do_BD>
export POSTGRES_PASSWORD=<senha_do_BD>
```

**2)** Crie um ambiente virtual para projetos Python e ative-o

**3)** Instale as dependências do projeto

```
$ pip install -r requirements/production.txt
```

**4)** Crie as tabelas necessárias no banco de dados

```
$ python manage.py makemigrations  # caso não haja arquivos de migração

$ python manage.py migrate
```

**5)** Crie um superusuário

```
$ python manage.py createsuperuser
```

Em seguida, forneça os dados solicitados.

**6)** Criando systemd Socket e Service Files para o Gunicorn

**6.1)** Na raiz do projeto, crie o arquivo obedecendo a seguinte estrutura:

```
$ vi .envs/.production/.envsfile
```

**6.2)** Abra o .envsfile e insira todas as variáveis de ambiente exigidas pela aplicação, preenchendo-as adequadamente, conforme sugerido abaixo:

```
# /<raiz_do_projeto>/.envs/.production/.envsfile

DJANGO_SETTINGS_MODULE=settings.production
DJANGO_SECRET_KEY=<secret-key> # ex: EeMHtbY0JNIV9lZQaKpeeMjBTx3k3i0Chj
ADMIN_URL_PATH=<url> # ex: admin
DJANGO_ALLOWED_HOSTS=<ip_externo_do_host>
DJANGO_SECURE_SSL_REDIRECT=False
EMAIL_HOST=<host_smtp> # ex: smtp.gmail.com
EMAIL_PORT=<port>
EMAIL_HOST_USER=<host_user>
EMAIL_HOST_PASSWORD=<password>
WEB_CONCURRENCY=4
MAINTENANCE_ADMIN_URL=<url_do_painel_admin>+"login" # ex: adminlogin
POSTGRES_HOST=<endereço_do_host_do_BD>
POSTGRES_PORT=<porta_em_execução_do_BD>
POSTGRES_DB=<nome_do_BD>
POSTGRES_USER=<usuário_do_BD>
POSTGRES_PASSWORD=<senha_do_BD>
Atenção para inserir os dados corretos, tal como inseridos no item 1.
```

**6.3)** Crie o serviço gunicorn.socket:

```
$ sudo vim /etc/systemd/system/gunicorn.socket
```

Salve o arquivo gunicorn.socket com o conteúdo abaixo:

```
# /etc/systemd/system/gunicorn.socket

[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
```

**6.4)** Crie o gunicorn.service:

No terminal, execute o comando:

```
$ sudo vim /etc/systemd/system/gunicorn.service
```

Salve o arquivo gunicorn.service com o conteúdo abaixo:

```
# /etc/systemd/system/gunicorn.service

[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=user
Group=nginx
WorkingDirectory=/projectpath/sicaf
EnvironmentFile=/projectpath/sicaf/.envs/.production/.envsfile
ExecStart=/projectpath/sicaf/venv_sicaf/bin/gunicorn \
        --access-logfile - \
        --workers 3 \
        --bind unix:/run/gunicorn.sock \
        config.wsgi:application

[Install]
WantedBy=multi-user.target
```

- No campo User informe o usuário e grupo no qual o processo irá rodar;
- No campo Group informe um grupo a qual o nginx possa comunicar-se facilmente;

_/projectpath_ -> Substitua pelo caminho do projeto

**6.5)** Após, inicie o gunicorn.socket e habilite para iniciar no boot:

```
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
```

**6.6)** Verifique se o socket esta ok:

```
$ sudo systemctl status gunicorn.socket

# Output
● gunicorn.socket - gunicorn socket
    Loaded: loaded (/etc/systemd/system/gunicorn.socket; enabled; vendor preset: disabled)
    Active: active (running) since Sáb 2019-02-02 18:58:25 UTC; 53min ago
    Listen: /run/gunicorn.sock (Stream)

Fev 02 18:58:25 sicaf-centos systemd[1]: Listening on gunicorn socket.

$ file /run/gunicorn.sock  

# Output
/run/gunicorn.sock: socket
```

**6.7)** Teste se socket foi:

```
$ sudo systemctl status gunicorn

# Output
● gunicorn.service - gunicorn daemon
    Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
    Active: inactive (dead)

$ curl --unix-socket /run/gunicorn.sock localhost

$ sudo systemctl status gunicorn

# Output
● gunicorn.service - gunicorn daemon
    Loaded: loaded (/etc/systemd/system/gunicorn.service; disabled; vendor preset: enabled)
    Active: active (running) since Mon 2018-07-09 20:00:40 UTC; 4s ago
Main PID: 1157 (gunicorn)
    Tasks: 4 (limit: 1153)
    CGroup: /system.slice/gunicorn.service
            ├─1157 /projectpath/myprojectdir/myprojectenv/bin/python3 /projectpath/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
            ├─1178 /projectpath/myprojectdir/myprojectenv/bin/python3 /projectpath/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
            ├─1180 /projectpath/myprojectdir/myprojectenv/bin/python3 /projectpath/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application
            └─1181 /projectpath/myprojectdir/myprojectenv/bin/python3 /projectpath/myprojectdir/myprojectenv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/run/gunicorn.sock myproject.wsgi:application

    XXX XX 20:00:40 django1 systemd[1]: Started gunicorn daemon.
    XXX XX 20:00:40 django1 gunicorn[1157]: [20XX-XX-XX 20:00:40 +0000] [1157] [INFO] Starting gunicorn 19.9.0
    XXX XX 20:00:40 django1 gunicorn[1157]: [20XX-XX-XX 20:00:40 +0000] [1157] [INFO] Listening at: unix:/run/gunicorn.sock (1157)
    XXX XX 20:00:40 django1 gunicorn[1157]: [20XX-XX-XX 20:00:40 +0000] [1157] [INFO] Using worker: sync
    XXX XX 20:00:40 django1 gunicorn[1157]: [20XX-XX-XX 20:00:40 +0000] [1178] [INFO] Booting worker with pid: 1178
    XXX XX 20:00:40 django1 gunicorn[1157]: [20XX-XX-XX 20:00:40 +0000] [1180] [INFO] Booting worker with pid: 1180
    XXX XX 20:00:40 django1 gunicorn[1157]: [20XX-XX-XX 20:00:40 +0000] [1181] [INFO] Booting worker with pid: 1181
    XXX XX 20:00:41 django1 gunicorn[1157]:  - - [XX/XXX/20XX:20:00:41 +0000] "GET / HTTP/1.1" 200 16348 "-" "curl/7.58.0"
```

**Importante**: Qualquer alteração realizada nas configurações do gunicorn deve ser seguida dos seguintes comandos.

```
$ sudo systemctl daemon-reload
$ sudo systemctl restart gunicorn
$ sudo systemctl restart gunicorn.socket
```

**7)** Configurando Nginx

**7.1)** Certifique que o arquivo /etc/nginx/nginx.conf possua, mais ou menos, as seguintes configurações:

```
# /etc/nginx/nginx.conf

# user                      nginx;
worker_processes            1;

error_log                   /var/log/nginx/error.log warn;
pid                         /var/run/nginx.pid;

# Load dynamic modules. See /usr/share/nginx/README.dynamic.
#include /usr/share/nginx/modules/*.conf;

events {
    worker_connections      1024;
}

http {
    log_format  main        '$remote_addr - $remote_user [$time_local] "$request" '
                            '$status $body_bytes_sent "$http_referer" '
                            '"$http_user_agent" "$http_x_forwarded_for"';

    access_log              /var/log/nginx/access.log  main;
    # access_log            off;

    sendfile                on;
    #tcp_nopush             on;
    #tcp_nodelay            on;
    keepalive_timeout       65;
    # gzip                  on;
    # types_hash_max_size   2048;

    include                 /etc/nginx/mime.types;
    default_type            application/octet-stream;

    # Load modular configuration files from the /etc/nginx/conf.d directory.
    # See http://nginx.org/en/docs/ngx_core_module.html#include
    # for more information.
    include                 /etc/nginx/conf.d/*.conf;
}
```

**7.2)** Crie um novo arquivo de configuração da aplicação:

```
$ sudo vim /etc/nginx/conf.d/gep.conf
```

Salve o arquivo gep.conf com o conteúdo abaixo:

```
# /etc/nginx/conf.d/gep.conf

server {
  listen                80;
  server_name           SERVER_NAME;
  client_max_body_size  34M;

  location / {
    proxy_pass          http://unix:/run/gunicorn.sock;
  }

  location /static/ {
    root                /<projectpath>;
  }

  location /media/ {
    root                /<projectpath>;
  }
}
```

- No campo SERVER_NAME informe o IP ou domínio do servidor da aplicação
- _projectpath_ -> Substitua pelo caminho da pasta projeto


**7.3)** Teste a sintaxe

```
# /etc/nginx/conf.d/

$ sudo nginx -t
```

**7.4)** Reinicie o nginx

```
$ sudo systemctl restart nginx
```

**7.5)** Garanta que o nginx inicie no boot

```
$ sudo systemctl enable nginx
```

**7.6)** Garanta que o nginx possa ler/escrever na pasta media:

```
$ sudo chmod +rwx /projectpath/media
$ sudo usermod -aG groupproject nginx
```

- _projectpath_ -> Substitua pelo caminho da pasta projeto
- _groupproject_ -> Substitua pelo grupo dono do diretório do projeto

**8)** Centos 7 - SELinux

Para garantir que o tráfego http não será bloqueado pelo SELinux do Centos, execute o comando:

```
$ sudo semanage permissive -a httpd_t
```

**9)** Preencha as tabelas de normalização conforme demonstrado na seção [Normalização](NORMALIZACAO.md).

**10)** Crie os grupos e associe as permissões específicas conforme demonstrado na seção [Grupos e Permissões](GRUPOS.md).

Pronto! Com o servidor rodando, acesse a url "ip_do_host/gep" e você deverá acessar a página inicial por meio de qualquer navegador web.


### Deploy com Docker

**1)** Na raiz do projeto, crie os arquivos obedecendo a seguinte estrutura:

```
$ vi .envs/.production/.django
$ vi .envs/.production/.postgres
```

Em seguida, insira todas as variáveis de ambiente exigidas pela aplicação, preenchendo-as adequadamente:

```
# .envs/.production/.django

# General
# ------------------------------------------------------------------------------
DJANGO_SETTINGS_MODULE=settings.production
DJANGO_SECRET_KEY=<secret-key> # ex: EeMHtbY0JNIV9lZQaKpeeMjBTx3k3i0Chj
ADMIN_URL_PATH=<url> # ex: admin
DJANGO_ALLOWED_HOSTS=<ip_externo_do_host>

# Security
# ------------------------------------------------------------------------------
# TIP: better off using DNS, however, redirect is OK too
DJANGO_SECURE_SSL_REDIRECT=False

# Email
# ------------------------------------------------------------------------------
EMAIL_HOST=<host_smtp> # ex: smtp.gmail.com
EMAIL_PORT=<port>
EMAIL_HOST_USER=<host_user>
EMAIL_HOST_PASSWORD=<password>

# dajngo-maintenance_mode
# ------------------------------------------------------------------------------
MAINTENANCE_ADMIN_URL=<url_do_painel_admin>+"login" # ex: adminlogin

# Redis
# ------------------------------------------------------------------------------
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=$REDIS_URL
REDIS_HOST=redis
REDIS_PORT=6379

# .envs/.production/.postgres

# PostgreSQL
# ------------------------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=<nome_do_BD>
POSTGRES_USER=<usuário_do_BD>
POSTGRES_PASSWORD=<senha_do_BD>
```

**2)** Faça os builds das imagens necessárias

Na raiz do projeto, execute:

```
docker-compose -f production.yml build
```

**3)** Rode os containers em modo background

```
docker-compose -f production.yml up -d
```

**4)** Crie as tabelas necessárias no banco de dados

```
$ docker-compose -f production.yml run --rm django python manage.py makemigrations  # caso não haja arquivos de migração

$ docker-compose -f production.yml run --rm django python manage.py migrate
```

**5)** Crie um superusuário

```
$ docker-compose -f production.yml run --rm django python manage.py createsuperuser
```

Em seguida, forneça os dados solicitados.

**6)** Preencha as tabelas de normalização conforme demonstrado na seção [Normalização](NORMALIZACAO.md).

**7)** Crie os grupos e associe as permissões específicas conforme demonstrado na seção [Grupos e Permissões](GRUPOS.md).

Pronto! Com o servidor rodando, acesse a url "ip_do_host/gep" você deverá acessar a página inicial do GEP por meio de qualquer navegador web.