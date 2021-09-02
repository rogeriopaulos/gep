# Extras

## ADMIN HONEYPOT

Quando do _deploy_ da aplicação, exige-se que seja definida a verdadeira url de acesso ao **Painel de Administração**. Recomenda-se, nesse caso, que urls não lógicas sejam escolhidas. Somando-se a isso, o GEP conta com uma funcionalidade de __honeypot__, onde todas as tentativas de acesso a url */admin* será logada e disponibilizada para o sysadmin.

Os logs serão disponibilizados no **Painel de Administração**, na seção *ADMIN_HONEYPOT > Login attempts*.

Para maiores informações, veja esse [link](https://github.com/dmpayton/django-admin-honeypot).


## AUDIT LOG

Todos as açoes de CRUD realizadas nas tabelas do GEP são auditadas e disponibilizadas no **Painel de Administração**, na seção *Audit log › Entradas de log*.

Para maiores informações, veja esse [link](https://github.com/jjkester/django-auditlog).


## AXES

Os logs de acesso da aplicação, bem como as tentativas falhas, são disponibilizados no **Painel de Administração**, na seção *Axes › Access attempts* e *Axes › Access logs*.

Para maiores informações, veja esse [link](https://github.com/jazzband/django-axes).

_Ps: Em ambiente de desenvolvimento, que utiliza as diretrizes definidas em **./app/settings/local.py**, essa funcionalidade é desabilitada (cf. variável **AXES_ENABLED**)._