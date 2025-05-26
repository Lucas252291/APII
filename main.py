import pdfplumber
import re
import spacy

def corrigir_capitalizacao(texto):
    def capitalizar(nome):
        excecoes = {'de', 'da', 'do', 'das', 'dos', 'e'}
        partes = nome.split()
        resultado = []
        for parte in partes:
            if parte.lower() in excecoes:
                resultado.append(parte.lower())
            else:
                if parte.isupper() and len(parte) > 1:
                    parte = parte.capitalize()
                resultado.append(parte)
        return ' '.join(resultado)

    padrao = re.compile(r'\b([A-ZÀ-Ú]{2,}(?:\s+[A-ZÀ-Ú]{2,})*)\b')

    def substituir(match):
        texto_achado = match.group(1)
        return capitalizar(texto_achado)

    texto_corrigido = padrao.sub(substituir, texto)
    return texto_corrigido

def anonimizar_texto(texto):
    nlp = spacy.load("pt_core_news_sm")
    doc = nlp(texto)

    anonimizado = texto
    # Substituir as entidades do spaCy (PER, LOC, ORG, DATE reconhecidas)
    for ent in reversed(doc.ents):
        if ent.label_ in ['PER', 'LOC', 'ORG', 'DATE']:
            anonimizado = anonimizado[:ent.start_char] + f"[{ent.label_}]" + anonimizado[ent.end_char:]
    
    # Agora, anonimizar datas no formato dd/mm/aaaa que spaCy pode não reconhecer
    # Regex para datas no formato dia/mês/ano (com / ou -)
    regex_datas = re.compile(r'\b\d{2}[/-]\d{2}[/-]\d{4}\b')
    
    # Substitui essas datas por [DATE]
    anonimizado = regex_datas.sub("[DATE]", anonimizado)
    
    return anonimizado

with pdfplumber.open(".pdf") as pdf:
    texto_original = "\n".join(page.extract_text() for page in pdf.pages)

print("=== TEXTO ORIGINAL ===")
print(texto_original)

texto_corrigido = corrigir_capitalizacao(texto_original)
print("\n=== TEXTO CORRIGIDO ===")
print(texto_corrigido)

texto_anonimizado = anonimizar_texto(texto_corrigido)
print("\n=== TEXTO ANONIMIZADO ===")
print(texto_anonimizado)
