# gitprj
Sistema para versionamento de projetos aplicado à Geoestatística

O sistema de versionamento de projetos de geoestatística é um conjunto de scripts e procedimentos que atuarão nos seguintes campos:

* Interação com o usuário: será utilizado inicialmente um cliente git pronto;
* Um script para associar cada commit à uma entrada em um banco de dados (inicialmente sqlite) com alguns campos a serem preenchidos manualmente depois pelo gerente do projeto;
* Um novo script irá percorrer o banco de dados e as informações do repositório para gerar gráficos e tabelas relacionados ao andamento do projeto.

Papéis no sistema:
* Gerente: administram o repositório, marcam versões, criam branches e podem fazer rollbacks;
* Usuários-padrão: fazem commits para branches permitidos pelo gerente.

Trabalho publicado: https://www.researchgate.net/publication/333828369_Version_control_system_applied_to_resource_modeling_projects
