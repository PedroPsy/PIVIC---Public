import pandas as pd

arquivo_excel = 'historico_por_aluno.xlsx'

# 1. Ler todas as abas, exceto a aba "Resumo"
abas = pd.read_excel(arquivo_excel, sheet_name=None)
abas = {nome: df for nome, df in abas.items() if nome.lower() != 'resumo'}

# 2. Concatenar os dados de todas as abas
dados = pd.concat(abas.values(), ignore_index=True)
#remove a coluna nome da tabela 
dados = dados.drop('nome', axis = 1)

# 3. Remover entradas com disciplinas vazias 
dados = dados.dropna(subset=['disciplina'])

# 4. Converter nota para número 
dados['nota'] = pd.to_numeric(dados['nota'], errors='coerce').fillna(0.0)

# 5. Análise: Média geral por aluno apenas para as disciplinas aprovadas
dados_aprovados = dados[dados['situacao'] == 'APROVADO']
media_geral_por_aluno = dados_aprovados.groupby('matricula')['nota'].mean().reset_index()
media_geral_por_aluno.columns = ['matricula', 'media_geral']

# 6. Análise: Quantidade de disciplinas cursadas por aluno
dados_unicos = dados_aprovados.drop_duplicates(subset=['matricula', 'disciplina'])

# Calcula a média das notas em cada disciplina apenas para alunos aprovados
media_geral_por_disciplina = dados_unicos.groupby('disciplina')['nota'].mean().reset_index()
media_geral_por_disciplina.columns = ['disciplina', 'media_geral']
media_geral_por_disciplina['media_geral'] = media_geral_por_disciplina['media_geral'].astype(float)
media_geral_por_disciplina ['media_geral'] = media_geral_por_disciplina['media_geral'].apply(lambda x:f'{x:.2f}')


# Calcula a quantidade de disciplinas cursadas por aluno
disciplinas_por_aluno = dados_unicos.groupby('matricula')['disciplina'].nunique().reset_index()
disciplinas_por_aluno.columns = ['matricula', 'qtd_disciplinas']

# 7. Análise: Situações mais comuns (aprovado, reprovado, etc.)
situacoes = dados['situacao'].value_counts().reset_index()
situacoes.columns = ['situacao', 'frequencia']

# 8. Análise: Disciplinas com mais reprovações (REPROVADO ou REP. FALTA)
reprovacoes = dados[dados['situacao'].str.contains("REPROVADO|REP", case=False, na=False)]
reprov_por_disciplina = reprovacoes['disciplina'].value_counts().reset_index()
reprov_por_disciplina.columns = ['disciplina', 'reprovacoes']

# 9. Análise: Alunos com mais trancamentos ou faltas
trancamentos = dados[dados['situacao'].str.contains(r"TRANCADO|REP\. FALTA", case=False, na=False)]
trancamentos_por_disciplina = trancamentos['disciplina'].value_counts().reset_index()
trancamentos_por_disciplina.columns = ['disciplina', 'trancamentos']

# 10. Salvar todas as análises em CSV
dados.to_csv('00_dados_completos.csv', index=False)
media_geral_por_disciplina.to_csv('01_media_por_disciplina.csv', index=False)
disciplinas_por_aluno.to_csv('02_disciplinas_por_aluno.csv', index=False)
situacoes.to_csv('03_situacoes_mais_comuns.csv', index=False)
reprov_por_disciplina.to_csv('04_disciplinas_com_mais_reprovacoes.csv', index=False)
trancamentos_por_disciplina.to_csv('05_alunos_com_mais_trancamentos.csv', index=False)


