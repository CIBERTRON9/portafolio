"""
Implementación simple del algoritmo RSA en Python.

Autor: Javier Cerda
Año:2024
Asignatura: Criptografía y Seguridad Informática

Descripción:
Este script demuestra el funcionamiento básico del algoritmo
de criptografía asimétrica RSA. Permite generar claves públicas
y privadas, cifrar un mensaje y posteriormente descifrarlo.

El objetivo es educativo, mostrando los pasos matemáticos
fundamentales de RSA.
"""

import random
from math import gcd


# Función para calcular el inverso modular
def mod_inverse(e, phi):
    for d in range(3, phi):
        if (d * e) % phi == 1:
            return d


# Generación de claves RSA
def generar_claves():
    p = 60
    q = 50

    n = p * q
    phi = (p - 1) * (q - 1)

    e = 17

    while gcd(e, phi) != 1:
        e = random.randrange(2, phi)

    d = mod_inverse(e, phi)

    return ((e, n), (d, n))


# Cifrado
def cifrar(mensaje, clave_publica):
    e, n = clave_publica
    return [pow(ord(char), e, n) for char in mensaje]


# Descifrado
def descifrar(mensaje_cifrado, clave_privada):
    d, n = clave_privada
    return ''.join([chr(pow(char, d, n)) for char in mensaje_cifrado])


# Ejecución y demostración Ingresando el mensaje a cifrar y descifrar
publica, privada = generar_claves()

mensaje = "HOla Mundo"

cifrado = cifrar(mensaje, publica)
descifrado = descifrar(cifrado, privada)

print("Clave pública:", publica)
print("Clave privada:", privada)
print("Mensaje:", mensaje)
print("Cifrado:", cifrado)
print("Descifrado:", descifrado)