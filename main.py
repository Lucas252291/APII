import pdfplumber
import spacy
import re


nlp = spacy.load("pt_core_news_md")

text = ""

with pdfplumber.open(".pdf") as pdf:

    print("---------------")
    print("Texto original:")
    for page in pdf.pages:
        text = page.extract_text()
        print(text)



doc = nlp(text)
for ent in doc.ents:
    print(ent.text, ent.label_)


# Função para capitalizar apenas as entidades (nomes, locais, organizações)
def capitalizar_entidades(texto):
    doc = nlp(texto)
    novo_texto = texto

    # Ordenar as entidades do final para o começo para evitar sobrescrever índices
    for ent in sorted(doc.ents, key=lambda x: x.start_char, reverse=True):
        entidade_original = texto[ent.start_char:ent.end_char]
        entidade_formatada = entidade_original.title()  # Capitaliza cada palavra
        novo_texto = novo_texto[:ent.start_char] + entidade_formatada + novo_texto[ent.end_char:]

    return novo_texto

resultado = capitalizar_entidades(text)

print("------------")
print("\nTransformando os nome :\n", resultado)

