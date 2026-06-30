"""Exemplo de uso da texto2area: texto cru (PT) -> grande area CAPES."""
from texto2area import classificar

TEXTOS = [
    "A atuacao do enfermeiro no cuidado ao paciente idoso em saude coletiva.",
    "Metodo de elementos finitos para simular trincas em concreto armado.",
    "Manejo do solo e adubacao na produtividade da soja em plantio direto.",
    "Analise do discurso e da narrativa literaria na poesia modernista brasileira.",
]

for txt in TEXTOS:
    area, margens, termos = classificar(txt)
    print(f"{area:30s} | margem {margens[0][1]:+.2f} | termos: {termos[:4]}")
