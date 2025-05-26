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
                if parte == parte.upper() and len(parte) > 1:
                    parte = parte.capitalize()
                elif not parte.istitle():
                    parte = parte.capitalize()
                resultado.append(parte)
        return ' '.join(resultado)

    # Padrão simplificado e corrigido
    padrao = re.compile(
        r'\b([A-ZÀ-Ú]{2,}(?:\s+[A-ZÀ-Ú]+)*)\b'  # Captura sequências de palavras todas maiúsculas
    )

    texto_corrigido = padrao.sub(
        lambda match: capitalizar(match.group(1)),
        texto
    )
    
    return texto_corrigido

# Extrai o texto do PDF mantendo formatação original
with pdfplumber.open(".pdf") as pdf:
    texto_original = "\n".join(page.extract_text() for page in pdf.pages)

print("=== TEXTO ORIGINAL ===")
print(texto_original)

texto_corrigido = corrigir_capitalizacao(texto_original)

print("\n=== TEXTO CORRIGIDO ===")
print(texto_corrigido)