# Normalização

## Tabelas de Normalização

As tabelas de normalização tem por finalidade uniformizar os dados da aplicação e garantir o seu correto uso.

**IMPORTANTE**: Os dados constantes nas tabelas de normalização dizem respeito à estrutura do órgão respectivo. Logo, os dados automaticamente inseridos podem ser alterados ou excluídos, ao passo que novos dados podem ser adicionados, respeitando seu contexto.

Acesse o **Painel de Administração** (_http://dominio/adminurl_) da aplicação e garante que todas as tabelas de normalização sejam populadas, respeitando a dinâmica interna do órgão.

_Ps: As tabelas de normalização encontram-se prefixadas com o termo **NORMALIZAÇÃO**._

As seguintes tabelas devem ser preenchidas:

- CONFIGURAÇÕES GERAIS > [NORMALIZAÇÃO] Assuntos (Administrativo)
- CONFIGURAÇÕES GERAIS > [NORMALIZAÇÃO] Conteúdos - Of. Expedidos
- CONFIGURAÇÕES GERAIS > [NORMALIZAÇÃO] Conteúdos - Of. Recebidos
- CONFIGURAÇÕES GERAIS > [NORMALIZAÇÃO] Processos vinculados - Motivos
- CONFIGURAÇÕES GERAIS > [NORMALIZAÇÃO] Status (Administrativo)
- CONFIGURAÇÕES GERAIS > [NORMALIZAÇÃO] Tipos de gravações de mídia

## Órgãos

O GEP exige que todo usuário seja, obrigatoriamente, vinculado a um órgão previamente cadastrado. Consequentemente, é mandatório a criação do órgão, o que deve ser feito pelo **Painel de Administração** (_http://dominio/adminurl_) da aplicação, na seção **QUALIFICAÇÃO DOS USUÁRIOS >> [NORMALIZAÇÃO] Órgãos**.

Nessa parte, garanta que ao órgão esteja atribuído a permissão **Acesso ao Módulo ADMINISTRATIVO**, disponível no campo _Permissões do orgão_.

## Usuários

### Cargos

Todo novo usuário do GEP deve ser vinculado a um cargo. Estes devem ser previamente inseridos pelo **Painel de Administração** (_http://dominio/adminurl_) da aplicação, na seção **QUALIFICAÇÃO DOS USUÁRIOS >> [NORMALIZAÇÃO] Cargos**.

### Novos usuários

**IMPORTANTE**: A inserção dos novos usuários deve ser feita pelo **Painel de Administração**, o que é feito preenchendo os campos solicitados das seções abaixo, na ordem respectiva:

1. _Autenticação e Autorização › Usuários_
2. _Qualificação dos Usuários › Usuários GEP_ -> Aqui, selecione o usuário que deseja qualificar.

_Ps: É necessário que alguns usuários sejam qualificados como **subscritor**. Essa qualificação pode ser atribuída em **Qualificação dos Usuários › Usuários GEP**, marcando o campo **Pode subscrever documentos?**._
