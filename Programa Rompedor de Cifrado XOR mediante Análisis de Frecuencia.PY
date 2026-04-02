===========================================================
Rompedor de Cifrado XOR mediante Análisis de Frecuencia
Autor: Javier Cerda
Año:2024
Asignatura: Criptografía y Seguridad Informática
Descripción:
Este script implementa un método básico de criptanálisis para
descifrar mensajes cifrados con un algoritmo XOR de una sola
clave (single-byte XOR).

El programa realiza un ataque de fuerza bruta probando todas
las claves ASCII posibles y evalúa cada resultado utilizando
un modelo estadístico basado en la frecuencia de letras en
idioma español.

Metodología:
1. Convertir el mensaje cifrado en binario a valores byte.
2. Aplicar la operación XOR con todas las claves ASCII posibles.
3. Filtrar los resultados que contengan caracteres imprimibles.
4. Evaluar cada texto descifrado usando frecuencias de letras
   en idioma español.
5. Ordenar los resultados según su probabilidad de ser un
   texto válido.

Objetivo:
Demostrar el uso de técnicas básicas de criptanálisis como
fuerza bruta y análisis estadístico en lenguaje para
identificar mensajes cifrados con algoritmos débiles.

Aplicación:
Este tipo de análisis es común en ejercicios de aprendizaje
de criptografía, desafíos de ciberseguridad (CTF) y análisis
de malware donde algunos datos pueden estar ofuscados
mediante operaciones XOR simples.
===========================================================
"""

# Mensaje cifrado en binario (cada byte separado por espacio)
cipher_bin = "01100001 01110100 01100001 01110010 01100100"

# Convertir a lista de enteros
cipher_bytes = [int(b, 2) for b in cipher_bin.split()]

# Diccionario de frecuencias de letras en español (aproximado)
spanish_letter_freq = {
    'a': 0.1253, 'e': 0.1202, 'o': 0.0868, 's': 0.0798, 'n': 0.0701,
    'r': 0.0687, 'i': 0.0625, 'd': 0.0586, 'l': 0.0497, 'c': 0.0416,
    't': 0.0404, 'u': 0.0393, 'm': 0.0315, 'p': 0.0251, 'b': 0.0221,
    'g': 0.0176, 'v': 0.0113, 'y': 0.0109, 'q': 0.0105, 'h': 0.0078,
    'f': 0.0069, 'j': 0.0052, 'ñ': 0.0031, 'z': 0.0029, 'x': 0.0017,
    'k': 0.0011, 'w': 0.0004
}

def score_frequency(text):
    """Calcula una puntuación basada en la frecuencia de letras en español."""
    score = 0
    text = text.lower()
    total_letters = sum(1 for char in text if char.isalpha())
    if total_letters == 0:
        return 0
    for char in text:
        if char in spanish_letter_freq:
            score += spanish_letter_freq.get(char, 0)
    return score / total_letters

# Lista para almacenar todas las claves válidas y sus puntuaciones
results = []

for key in range(32, 127):
    decrypted = ''.join(chr(b ^ key) for b in cipher_bytes)
    if all(32 <= ord(c) <= 126 for c in decrypted):
        score = score_frequency(decrypted)
        results.append((key, decrypted, score))

# Normalizar a porcentaje de probabilidad
total_score = sum(score for _, _, score in results)
if total_score > 0:
    results_with_prob = [
        (key, decrypted, score, 100 * score / total_score)
        for key, decrypted, score in results
    ]
    # Ordenar de mayor a menor probabilidad
    results_with_prob.sort(key=lambda x: x[3], reverse=True)

    # Mostrar todas las claves con su porcentaje
    print("Claves y probabilidades estimadas:\n")
    for key, decrypted, score, prob in results_with_prob:
        print(f"Clave {key:3} ({chr(key)}): {prob:.2f}% - \"{decrypted}\"")

    # Mostrar la mejor
    best_key, best_decrypted, _, best_prob = results_with_prob[0]
    print("\nMejor opción seleccionada automáticamente:")
    print(f"Clave con mayor probabilidad: {best_key} ({chr(best_key)})")
    print(f"Probabilidad estimada: {best_prob:.2f}%")
    print(f"Mensaje descifrado: {best_decrypted}")
else:
    print("No se encontraron claves con puntuaciones de frecuencia significativas")
