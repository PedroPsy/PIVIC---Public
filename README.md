# PIVIC - Análise dos Históricos dos Alunos de Sistema de Informação

Este projeto tem como objetivo realizar a extração, transformação e análise dos dados dos históricos acadêmicos dos alunos do curso de Sistema de Informação. A seguir, estão descritas as principais etapas do processo e as análises realizadas.\
Os arquivos presentes neste repositório são uma cópia do repositório originial que possui as bases de dados utilizados para a pesquisa.

1. Extração de Dados
Leitura dos Dados:
Os dados são extraídos de um arquivo Excel (historico_por_aluno.xlsx) contendo várias abas, cada uma representando diferentes conjuntos de históricos.
Seleção das Abas:
Todas as abas são lidas, exceto a aba de resumo, para garantir que apenas os dados relevantes sejam utilizados.
Unificação dos Dados:
Os dados de todas as abas são concatenados em um único DataFrame, facilitando o processamento e análise posterior.
2. Transformação dos Dados
Limpeza dos Dados:
Remoção da coluna nome, que não é necessária para as análises.
Exclusão de linhas com valores ausentes na coluna disciplina.
Conversão dos valores da coluna nota para o tipo numérico, substituindo valores inválidos por zero.
Filtragem de Situações:
Seleção apenas das disciplinas em que o aluno foi aprovado para algumas análises.
Remoção de disciplinas repetidas por aluno, considerando apenas a primeira aprovação.
3. Análise dos Dados
Média Geral por Aluno:
Cálculo da média das notas dos alunos considerando apenas as disciplinas aprovadas.
Notas por Disciplina:
Cálculo da média das notas em cada disciplina para alunos aprovados.
Quantidade de Disciplinas Cursadas:
Contagem do número de disciplinas únicas cursadas por cada aluno.
Situações Mais Comuns:
Identificação das situações mais frequentes (aprovado, reprovado, trancado, etc.).
Disciplinas com Mais Reprovações:
Listagem das disciplinas com maior número de reprovações ou faltas.
Disciplinas com Mais Trancamentos:
Listagem das disciplinas com maior número de trancamentos ou faltas.
Visualizações:
Geração de gráficos para facilitar a interpretação dos resultados, como distribuição das notas, taxa de aprovação por disciplina e médias das notas.
4. Resultados
Os resultados das análises são salvos em arquivos CSV e gráficos PNG, permitindo fácil acesso e visualização dos padrões encontrados nos dados acadêmicos.

Como Executar
Instale as dependências:
Execute o notebook analisysNotebook.ipynb para realizar todas as etapas de ETL e análise.
Os arquivos de saída estarão disponíveis na pasta do projeto.
Objetivo
O projeto busca identificar padrões nos históricos dos alunos, apontando disciplinas com maiores dificuldades, taxas de trancamento e reprovação, além de destacar as disciplinas com melhores desempenhos.

Autor:
Seu nome aqui
Licença:
MIT
