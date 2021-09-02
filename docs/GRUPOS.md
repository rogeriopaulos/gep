# Grupos e Permissões

O GEP possui um funcionamento fundamentado numa lógica particular de grupos e permissões.

## Criação

Para criar os grupos e permissões pré-definidos, na raiz do projeto, com o ambiente virtual ativado, execute:

```
python manage.py create_groups
```

Caso tenha optado pelo deploy da aplicação em containers Docker, o comando correto é (na raiz do projeto):

```
docker-compose run --rm django python manage.py create_groups
```

Acesse o **Painel de Administração** da aplicação e clique em _AUTENTICAÇÃO E AUTORIZAÇÃO > Grupos_ e certifique que os grupos **COORDENADORES** e **USUÁRIOS** foram criados.

_Ps: Para incluir um usuário em um grupo, na página inicial do Painel de Administração clique em "AUTENTICAÇÃO E AUTORIZAÇÃO > Usuários". Clique no nome de usuário desejado e na aba "Permissões" procure pelo item "Grupos". Em seguida, escolha os grupos desejados no box "grupos disponíveis" e inclua no box "grupos escolhido(s)". Ao final, salve o procedimento._

A distribuição dos grupos é segmentada de acordo com a atividade exercida pelo usuário e seus poderes dentro do órgão. Por exemplo, o funcionário com poderes de gestão deverá integrar o grupo _COORDENADOR_, ao passo que aqueles que não possuem poderes decisórios, devem integrar o grupo _USUÁRIOS_.

## Permissões

Os grupos referidos são apenas abstrações, criados com a finalidade de sistematizar as permissões exigidas pela aplicação para acessar ou realizar determinadas ações. A distribuição das referidas permissões opera-se da seguinte forma:

### Grupo COORDENADOR

- Acessar, criar e editar qualquer processo ou ato do GEP;
- Habilitar* usuários do GEP em um processo.

### Grupo USUÁRIOS

- Acessar os processos do GEP, desde que previamente habilitado;
- Criar e editar atos nos processos previamente habilitados.

_* A habilitação consiste em conceder acesso a um processo e definir se o habilitado pode criar ou editar atos no respectivo processo._
