# Contribuições

Esse projeto se baseia (em linhas gerais) nas diretrizes do [GitHub flow](https://guides.github.com/introduction/flow/index.html). Consiste na existência permanente de uma *branch* **main** (principal) e quantas outras *branchs* forem necessárias. Mudanças realizadas em uma *branch* que não a principal não afetam a **main**. Portanto, o desenvolvedor é livre para experimentar e fazer *commit* de suas alterações de maneira segura, sabendo que suas alterações não serão integradas no ramo **main** até que os mantenedores revisem e aceitem as alterações.

Entretanto, algumas regras devem ser seguidas quando da criação de uma nova *branch*:

- Antes de criar uma *branch*, crie uma *issue* que descreva o seu objetivo (clique em **Issues** na barra de navegação lateral). Importante que o título da *issue* descreva o que você deseja melhorar/alterar/corrigir na aplicação.
- Crie a *branch* nova a partir da *branch* **main**.
- Caso a alteração no projeto diga respeito a implementação de uma nova funcionalidade ou melhoria sob o código, a respectiva *branch* deve ser prefixada com o termo **feature/**. Por exemplo, "*feature/fooBar*".
- Caso a alteração no projeto diga respeito a uma correção de bug(s), a respectiva *branch* deve ser prefixada com o termo **hotfix/**. Por exemplo, "*hotfix/fooBar*".

Uma vez finalizada a *feature* ou *hotfix*, para submeter a alteração no ramo principal, efetue os seguintes passos:

1. Faça o *push* de suas alterações no repositório remoto do Github.
2. Vá para o projeto e clique em **Pull requests (PR)**.
3. Clique em **New pull request**.
4. Selecione o ramo de origem (*compare*) e garanta que o ramo de destino (*base*) seja o **main**. Clique em **Create pull request**.
5. Na tela seguinte, adicione um título para o **PR**.
6. Adicione uma breve descrição para o **PR** fazendo menção explicíta para a *issue* relacionada*. _Ex: "Renomeando funções. Veja issue #10"_.
7. Preencha os demais campos caso entenda necessário.
8. Submeta as alterações.

Pronto! O *Pull requests* estará pronto para ser analisado, aprovado e mesclado ao código principal.

_** Caso a *branch* não seja mais necessária, remova-a"**._
