import string
from collections import Counter

# Función para extraer palabras de una sola letra
def palabras_una_letra(texto):
    palabras = texto.lower().split()
    return [palabra for palabra in palabras if len(palabra) == 1 and palabra in string.ascii_lowercase]

# Leer y analizar un texto para palabras de una letra
def analizar_palabras_una_letra(archivo):
    with open(archivo, "r", encoding="utf-8") as file:
        texto = file.read()
    return Counter(palabras_una_letra(texto))

# Generar el mapeo basado en palabras de una letra
def generar_mapeo(frecuencias_libro, frecuencias_cifrado):
    letras_libro = [letra for letra, _ in frecuencias_libro.most_common()]
    letras_cifrado = [letra for letra, _ in frecuencias_cifrado.most_common()]
    return {cifrado: libro for cifrado, libro in zip(letras_cifrado, letras_libro)}

# Función para descifrar usando el mapeo
def descifrar_por_mapeo(texto, mapeo):
    texto_descifrado = ""
    for caracter in texto:
        if caracter.lower() in mapeo:
            nueva_letra = mapeo[caracter.lower()]
            # Mantener mayúsculas/minúsculas
            texto_descifrado += nueva_letra.upper() if caracter.isupper() else nueva_letra
        else:
            texto_descifrado += caracter
    return texto_descifrado

# Archivos de entrada
archivo_libro = "quijote.txt"       # Texto del Quijote
archivo_cifrado = "finis-mundi-encrypted.txt"  # Texto cifrado

# Analizar palabras de una sola letra
frecuencias_libro = analizar_palabras_una_letra(archivo_libro)
frecuencias_cifrado = analizar_palabras_una_letra(archivo_cifrado)

print("Frecuencias en el libro:", frecuencias_libro)
print("Frecuencias en el texto cifrado:", frecuencias_cifrado)

# Generar mapeo y descifrar
mapeo = generar_mapeo(frecuencias_libro, frecuencias_cifrado)
print("Mapeo generado:", mapeo)

# Leer el texto cifrado completo
with open(archivo_cifrado, "r", encoding="utf-8") as file:
    texto_cifrado = file.read()

texto_descifrado = descifrar_por_mapeo(texto_cifrado, mapeo)
#print("Texto descifrado:\n", texto_descifrado)

# Guardar el texto descifrado en un archivo
with open("texto_descifrado.txt", "w", encoding="utf-8") as file:
    file.write(texto_descifrado)
