import pdfplumber
import re

def corrigir_capitalizacao(texto):
    def capitalizar(nome):
        excecoes = {'de', 'da', 'do', 'das', 'dos', 'e'}
        partes = nome.split()
        resultado = []
        for parte in partes:
            if parte.lower() in excecoes:
                resultado.append(parte.lower())
            else:
                # Corrigir apenas palavras em maiúsculas e que não sejam abreviações (ex: siglas)
                if parte.isupper() and len(parte) > 1:
                    parte = parte.capitalize()
                resultado.append(parte)
        return ' '.join(resultado)

    # Padrão para identificar blocos em maiúsculas (palavras compostas)
    padrao = re.compile(
        r'\b([A-ZÀ-Ú]{2,}(?:\s+[A-ZÀ-Ú]{2,})*)\b'
    )

    # Função para preservar espaços originais e capitalizar
    def substituir(match):
        texto_achado = match.group(1)
        return capitalizar(texto_achado)

    texto_corrigido = padrao.sub(substituir, texto)
    return texto_corrigido

with pdfplumber.open(".pdf") as pdf:
    texto_original = "\n".join(page.extract_text() for page in pdf.pages)

print("=== TEXTO ORIGINAL ===")
print(texto_original)

texto_corrigido = corrigir_capitalizacao(texto_original)

print("\n=== TEXTO CORRIGIDO ===")
print(texto_corrigido)
