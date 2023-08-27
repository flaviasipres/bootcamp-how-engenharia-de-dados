# Projeto final do bootcamp Engenharia de Dados | How

### Objetivo:
Criar um fluxo de trabalho eficiente para a análise robusta e escalável de dados agrícolas.
### Motivação:
Aproveitar os dados científicos disponibilizados pela Embrapa para tomar decisões mais embasadas e aplicar conhecimentos comprovados na prática.
### Construção do Projeto:
A construção do projeto envolve várias etapas que permitem coletar, armazenar, processar e analisar os dados agrícolas. Seguem abaixo as etapas realizadas:
- **Definição dos Objetivos e Requisitos:** Esta etapa consistiu na identificação dos objetivos do projeto, como a otimização da produção agrícola e na definição dos requisitos, como tipos de dados a serem coletados e fontes de dados.
- **Coleta de Dados:** O foco neste passo foi construir a conexão com a fonte de dados da Embrapa para coletar dados como cultivares, obtentores, etc.
- **Armazenamento em S3:** Foi escolhido o serviço S3 da AWS para armazenar os dados coletados de forma escalável e organizada em estruturas de pastas e arquivos que facilitem a gestão e a recuperação.
- **Catalogação de Dados com AWS Glue:** Esta etapa teve como objetivo catalogar os dados, extraindo os metadados, como esquema dos dados, formatos, tipos de colunas, etc.
- **Configuração do Amazon Athena e Análise de dados:** Optou-se por utilizar o Athena tornamdo-se possível consultas SQL interativas nos dados catalogados para análise.
- **Visualização de Dados:** Utilização do Power BI como ferramentas de visualização para criar painéis de controle e gráficos com os insights obtidos.
### Arquitetura do Projeto:
![image](https://github.com/flaviasipres/bootcamp-how-engenharia-de-dados/assets/68780037/9b9f5986-2b6b-41ea-a9a9-30d936cf4c6c)
Para verificar as capturas do desenvolvimento do projeto, [clique aqui]().
