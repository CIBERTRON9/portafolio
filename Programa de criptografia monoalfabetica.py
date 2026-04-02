"""
Criptoanálisis monoalfabético con:
 - Análisis de frecuencia (unigrama, bigrama, trigrama)
 - Hill Climbing para optimización de mapeo
 - Validación con diccionario de palabras españolas
 - Línea base con permutaciones aleatorias
 
Autor: Javier Cerda
Año de creación: 2024
Asignatura: Criptografía y Seguridad Informática


Este programa intenta descifrar un texto cifrado mediante sustitución
utilizando técnicas de análisis estadístico del idioma español.

El proceso consiste en:
1. Analizar la frecuencia de letras del texto cifrado.
2. Generar un mapeo inicial basado en las letras más comunes del español.
3. Evaluar posibles descifrados usando n-gramas (bigramas y trigramas).
4. Validar resultados comparando palabras con un diccionario español.
5. Optimizar el mapeo mediante el algoritmo Hill Climbing.

El objetivo es encontrar el mapeo de sustitución que produzca
el texto más probable en español.

"""
import random
from collections import Counter
from typing import Dict, Set, Tuple

# 1. Texto cifrado
cipher_text = "VPMVQ PMO UMOMV XUVPZ UVPMO XUVPZ PMOZUZ ZUZVP"
# Descomponer en lista de palabras y texto continuo
cipher_words = cipher_text.split()
cipher = cipher_text.replace(" ", "")

# 2. Frecuencias unigrama (español)
letter_freq = {
    'E': 13.72, 'A': 11.72, 'O': 8.44, 'S': 7.20,
    'N': 6.83, 'R': 6.41, 'I': 5.28, 'L': 5.24,
    'D': 4.67, 'T': 4.60, 'U': 4.55, 'C': 3.87,
    'M': 3.08, 'P': 2.89, 'B': 1.49, 'H': 1.18,
    'Q': 1.11, 'Y': 1.09, 'V': 1.05, 'G': 1.00,
    'Z': 0.47, 'X': 0.14, 'Ñ': 0.17
}

# 3. Frecuencias bigramas (log-probabilidades, ejemplo reducido)
bigram_freq = {
    'DE': 2.0, 'EN': 1.8, 'LA': 1.7, 'ES': 1.6,
    'OS': 1.5, 'AR': 1.4, 'ER': 1.3, 'CI': 1.2,
    'TE': 1.1, 'OR': 1.0
}

# 4. Frecuencias trigramas (log-probabilidades, ejemplo reducido)
trigram_freq = {
    'QUE': 3.0, 'DEL': 2.5, 'LOS': 2.2, 'ENT': 2.0,
    'EST': 1.8, 'ADO': 1.6, 'PAR': 1.4, 'CON': 1.2
}

# 5. Cargar diccionario español
def load_spanish_dictionary(filepath: str = "spanish_words.txt") -> Set[str]:
    words = set()
    for enc in ("utf-8", "latin-1"):
        try:
            with open(filepath, encoding=enc) as f:
                for line in f:
                    w = line.strip().lower()
                    if w.isalpha():
                        words.add(w)
            break
        except (FileNotFoundError, UnicodeDecodeError):
            continue
    return words

spanish_dict = load_spanish_dictionary()

# 6. Funciones de decodificación
def decode_text(text: str, mapping: Dict[str, str]) -> str:
    return ''.join(mapping.get(ch, ch) for ch in text)

# 7. Funciones de scoring
def score_dictionary(decoded: str, dictionary: Set[str]) -> float:
    words = decoded.lower().split()
    if not words:
        return 0.0
    valid = sum(1 for w in words if w in dictionary)
    return valid / len(words)

def score_ngrams(decoded: str,
                 bigrams: Dict[str, float],
                 trigrams: Dict[str, float]) -> float:
    score = 0.0
    text = decoded.replace(" ", "")
    # bigramas
    for i in range(len(text) - 1):
        bg = text[i:i + 2].upper()
        score += bigrams.get(bg, 0)
    # trigramas
    for i in range(len(text) - 2):
        tg = text[i:i + 3].upper()
        score += trigrams.get(tg, 0)
    return score

def combined_score(decoded: str, dictionary: Set[str]) -> float:
    # combinar diccionario y n-gramas
    d_score = score_dictionary(decoded, dictionary)
    n_score = score_ngrams(decoded, bigram_freq, trigram_freq)
    return d_score * 10 + n_score  # pesos ajustables

# 8. Generar mapeo inicial (por frecuencia unigrama)
alphabet = list(letter_freq.keys())
cipher_letters = list(set(cipher))

# ordenar unigrama desc
sorted_plain = sorted(letter_freq, key=lambda k: -letter_freq[k])
# ordenar en texto desc
sorted_cipher = [c for c, _ in sorted(Counter(cipher).items(), key=lambda x: -x[1])]

# mapeo inicial
init_map: Dict[str, str] = {
    c: (sorted_plain[i] if i < len(sorted_plain) else '?')
    for i, c in enumerate(sorted_cipher)
}
# completar mapeo con remanentes
remaining = [c for c in alphabet if c not in init_map.values()]
for c in alphabet:
    if c not in init_map:
        init_map[c] = remaining.pop()

# 9. Hill Climbing
def hill_climbing(cipher_text: str,
                  init_mapping: Dict[str, str],
                  iterations: int = 2000) -> Tuple[Dict[str, str], str, float]:
    best_map = init_mapping.copy()
    best_decoded = decode_text(cipher_text, best_map)
    best_score = combined_score(best_decoded, spanish_dict)

    for _ in range(iterations):
        m = best_map.copy()
        a, b = random.sample(alphabet, 2)
        # swap
        inv = {v: k for k, v in m.items()}
        ca, cb = inv.get(a), inv.get(b)
        if ca and cb:
            m[ca], m[cb] = m[cb], m[ca]
        decoded = decode_text(cipher_text, m)
        sc = combined_score(decoded, spanish_dict)
        if sc > best_score:
            best_score = sc
            best_map = m
            best_decoded = decoded

    return best_map, best_decoded, best_score

# 10. Ejecución
# Línea base aleatoria
random_map = {c: random.choice(alphabet) for c in cipher_letters}
baseline_dec = decode_text(cipher_text, random_map)
baseline_score = combined_score(baseline_dec, spanish_dict)
print(f"Baseline aleatorio -> Score: {baseline_score:.2f}, Texto: {baseline_dec}")

# Hill Climbing desde init_map
hc_map, hc_decoded, hc_score = hill_climbing(cipher_text, init_map, iterations=5000)
print(f"\nHill Climbing -> Score: {hc_score:.2f}")
print(hc_decoded)

# Mostrar mapeo final
print("\nMapeo final (cifrada->clara):")
for c in sorted(hc_map):
    print(f"  {c} -> {hc_map[c]}")

# Validación final con diccionario
d_frac = score_dictionary(hc_decoded, spanish_dict)
print(f"\nFracción de palabras válidas: {d_frac:.2f}")
