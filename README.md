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

The git repository used in the published paper is in https://github.com/cazacche/Projeto_versionamento_geostat

The project tools are two main scripts:

* The first one is read_git_repository_save_db.py. This script will read a given git repository (already downloaded in the computer) and generate a sqlite database. It is important to establish the desired columns in this step. For example, we created a column 'nota' (which means grade, in portuguese). The objective of the grade column for each commit is for the project manager to evaluate the commits. This is why we create a sqlite database, to process the repository, create new metrics for the commits and store the desired ones.

* The next and last one is plot_data.py. This script will process the generated database file and produce the figures.
