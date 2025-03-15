import string

# Función para cifrar texto con el cifrado César
def cifrar_cesar(texto, desplazamiento):
    alfabeto = string.ascii_lowercase
    alfabeto_mayus = string.ascii_uppercase
    texto_cifrado = ""

    for caracter in texto:
        if caracter in alfabeto:
            # Cifrar minúsculas
            indice = (alfabeto.index(caracter) + desplazamiento) % len(alfabeto)
            texto_cifrado += alfabeto[indice]
        elif caracter in alfabeto_mayus:
            # Cifrar mayúsculas
            indice = (alfabeto_mayus.index(caracter) + desplazamiento) % len(alfabeto_mayus)
            texto_cifrado += alfabeto_mayus[indice]
        else:
            # Mantener otros caracteres sin cambios
            texto_cifrado += caracter

    return texto_cifrado

# Leer el archivo de texto original
archivo_entrada = "finis-mundi.txt"  # Cambia por el nombre de tu archivo
archivo_salida = "finis-mundi-encrypted.txt"
desplazamiento = 6  # Desplazamiento del cifrado César

try:
    # Leer el contenido del archivo original
    with open(archivo_entrada, "r", encoding="utf-8") as file:
        texto_original = file.read()

    # Cifrar el texto
    texto_cifrado = cifrar_cesar(texto_original, desplazamiento)

    # Crear un nuevo archivo con el contenido cifrado
    with open(archivo_salida, "w", encoding="utf-8") as file:
        file.write(texto_cifrado)

    print(f"Texto cifrado guardado en '{archivo_salida}' con un desplazamiento de {desplazamiento}.")

except FileNotFoundError:
    print(f"El archivo '{archivo_entrada}' no fue encontrado. Asegúrate de que existe en el directorio.")
