import os
import re
import PyPDF2
import pandas as pd

def extrair_texto_pdf(pdf_path):
    texto_completo = ""
    with open(pdf_path, 'rb') as file:
        leitor = PyPDF2.PdfReader(file)
        for pagina in leitor.pages:
            texto_completo += pagina.extract_text() + "\n"
    return texto_completo

def extrair_dados_aluno(texto):
    # Adaptação para o padrão dos históricos da UFPB
    matricula_match = re.search(r'Histórico Escolar - Emitido\n(\d{11})', texto)
    nome_match = re.search(r'\d{11}([A-Z\s]+)\s+\(', texto)
    matricula = matricula_match.group(1) if matricula_match else None
    nome = nome_match.group(1).strip().title() if nome_match else "Não identificado"
    return matricula, nome

def extrair_disciplinas(texto, valor_default=0.0):
    padrao = re.compile(
        r'(?P<ano>\d{4}\.\d+)\s+'
        r'(?P<disciplina>[A-ZÀ-Ÿ\s]+?)\s+'
        r'(?:\d{2}|\-\-\-)?\s+'
        r'(?P<situacao>APROVADO|PENDENTE|REPROVADO|EQUIVALÊNCIA|DISPENSADO|APROVEITADO|TRANCADO|REP\. FALTA|MATRICULADO)\s*'
        r'(?P<nota>[\d\.]+)?',
        re.IGNORECASE
    )

    disciplinas = []
    for match in padrao.finditer(texto):
        disciplina = match.group('disciplina').strip()
        situacao = match.group('situacao').strip().upper()
        nota_str = match.group('nota')
        try:
            nota = float(nota_str) if nota_str else 0.0
        except ValueError:
            nota = valor_default

        disciplinas.append({
            'disciplina': disciplina,
            'nota': nota,
            'situacao': situacao
        })
    return disciplinas

def limpar_nome_para_planilha(nome, usados):
    nome_limpo = re.sub(r'[^a-zA-Z0-9]', '_', nome)[:28]
    base = nome_limpo
    contador = 1
    while nome_limpo in usados:
        nome_limpo = f"{base}_{contador}"
        contador += 1
    usados.add(nome_limpo)
    return nome_limpo

def processar_varias_pastas_de_pdfs_em_abas(pastas_pdf, arquivo_saida='historico_por_aluno.xlsx'):
    abas_usadas = set()
    resumo_alunos = []
    tem_dados = False  # Para evitar erro se nenhuma aba for criada

    with pd.ExcelWriter(arquivo_saida, engine='openpyxl', mode='w') as writer:
        for pasta_pdf in pastas_pdf:
            if not os.path.isdir(pasta_pdf):
                print(f"❌ Caminho inválido: {pasta_pdf}")
                continue

            arquivos_pdf = [f for f in os.listdir(pasta_pdf) if f.lower().endswith('.pdf')]
            if not arquivos_pdf:
                print(f"⚠️ Nenhum PDF encontrado em: {pasta_pdf}")
                continue

            for nome_arquivo in arquivos_pdf:
                caminho_pdf = os.path.join(pasta_pdf, nome_arquivo)
                print(f"📄 Processando: {caminho_pdf}")
                texto = extrair_texto_pdf(caminho_pdf)
                matricula, nome = extrair_dados_aluno(texto)
                disciplinas = extrair_disciplinas(texto)

                if not disciplinas or not matricula:
                    print(f"⚠️ Dados incompletos em {nome_arquivo}")
                    continue

                resumo_alunos.append({
                    'matricula': matricula,
                    'nome': nome
                })

                registros = []
                for disc in disciplinas:
                    registros.append({
                        'matricula': matricula,
                        'nome': nome,
                        'disciplina': disc['disciplina'],
                        'nota': disc['nota'],
                        'situacao': disc['situacao']
                    })

                df = pd.DataFrame(registros)

                matricula_no_arquivo = re.search(r'\d{11}', nome_arquivo)
                nome_aba = limpar_nome_para_planilha(
                    matricula_no_arquivo.group(0) if matricula_no_arquivo else matricula,
                    abas_usadas
                )

                df.to_excel(writer, sheet_name=nome_aba, index=False)
                tem_dados = True

        if resumo_alunos:
            df_resumo = pd.DataFrame(resumo_alunos).drop_duplicates()
            df_resumo.to_excel(writer, sheet_name='Resumo', index=False)

    if not tem_dados:
        print("⚠️ Nenhum dado foi processado. Verifique os PDFs e os padrões de extração.")
    else:
        print(f"✅ Arquivo Excel com todas as abas salvo como: {arquivo_saida}")

if __name__ == '__main__':
    pastas_com_pdfs = [
        r'2014',
        r'2016',
        r'2017',
        r'2018',
        r'2019',
        r'2020',
        r'2021',
        r'2022',
        r'2023',
        r'2024',
    ]
    processar_varias_pastas_de_pdfs_em_abas(pastas_com_pdfs)
