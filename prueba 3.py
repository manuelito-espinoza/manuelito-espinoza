import numpy as np

peliculas = []
asientos = {}
ventas = {}
asistentes = {}

def mostrar_menu():
    print("----- MENU -----")
    print("1. Nueva película")
    print("2. Mostrar películas")
    print("3. Reservar asiento")
    print("4. Mostrar asientos disponibles")
    print("5. Comprar entrada")
    print("6. Importar películas")
    print("7. Exportar películas")
    print("8. Actualizar película")
    print("9. Calcular total de ventas por película")
    print("10. Calcular total de asistentes por película")
    print("11. Salir")

def agregar_pelicula():
    nombre = input("Ingrese el nombre de la película: ")
    descripcion = input("Ingrese la descripción de la película: ")
    categoria = input("Ingrese la categoría de la película: ")
    costo = float(input("Ingrese el costo de la película: "))
    peliculas.append({"nombre": nombre, "descripcion": descripcion, "categoria": categoria, "costo": costo})
    asientos[nombre] = np.zeros((20, 10), dtype=bool)
    ventas[nombre] = 0
    asistentes[nombre] = 0
    print("Película agregada exitosamente.")

def mostrar_peliculas():
    print("----- Películas disponibles -----")
    for i, pelicula in enumerate(peliculas):
        print(f"{i+1}. {pelicula['nombre']}")
    print()

def seleccionar_pelicula():
    mostrar_peliculas()
    pelicula_index = int(input("Seleccione el número de la película: ")) - 1

    if 0 <= pelicula_index < len(peliculas):
        return peliculas[pelicula_index]
    else:
        print("Opción inválida. Por favor, seleccione un número de película válido.")
        return None

def mostrar_asientos(pelicula):
    print(f"----- Asientos disponibles para la película {pelicula['nombre']} -----")
    asientos_pelicula = asientos[pelicula['nombre']]
    for fila in asientos_pelicula:
        fila_str = " ".join(["[]" if not asiento else "X" for asiento in fila])
        print(fila_str)

def reservar_asiento():
    pelicula = seleccionar_pelicula()
    if pelicula:
        asientos_pelicula = asientos[pelicula['nombre']]
        mostrar_asientos(pelicula)
        fila = int(input("Ingrese el número de fila del asiento: "))
        columna = int(input("Ingrese el número de columna del asiento: "))
        if 1 <= fila <= 20 and 1 <= columna <= 10:
            if asientos_pelicula[fila - 1, columna - 1]:
                print("El asiento ya está reservado.")
            else:
                asientos_pelicula[fila - 1, columna - 1] = True
                mostrar_asientos(pelicula)
                print("Reserva exitosa.")
                asistentes[pelicula['nombre']] += 1
        else:
            print("Asiento inválido. Por favor, ingrese un número de fila y columna válido.")

def mostrar_asientos_disponibles():
    pelicula = seleccionar_pelicula()
    if pelicula:
        mostrar_asientos(pelicula)

def comprar_entrada():
    pelicula = seleccionar_pelicula()
    if pelicula:
        mostrar_asientos(pelicula)
        asientos_pelicula = asientos[pelicula['nombre']]
        fila = int(input("Ingrese el número de fila del asiento: "))
        columna = int(input("Ingrese el número de columna del asiento: "))
        if 1 <= fila <= 20 and 1 <= columna <= 10:
            if asientos_pelicula[fila - 1, columna - 1]:
                print("El asiento ya está reservado.")
            else:
                asientos_pelicula[fila - 1, columna - 1] = True
                mostrar_asientos(pelicula)
                print("Compra de entrada exitosa.")
                boleta = len(asientos_pelicula[asientos_pelicula == True])
                valor = pelicula['costo']
                ventas[pelicula['nombre']] += valor
                with open("tickets.txt", "a") as file:
                    file.write(f"Asiento: {fila}-{columna}\n")
                    file.write(f"Película: {pelicula['nombre']}\n")
                    file.write(f"Número de boleta: {boleta}\n")
                    file.write(f"Valor: {valor}\n\n")
                    print("Se ha generado un ticket en tickets.txt.")
                asistentes[pelicula['nombre']] += 1
        else:
            print("Asiento inválido. Por favor, ingrese un número de fila y columna válido.")

def importar_peliculas():
    archivo = input("Ingrese el nombre del archivo de importación: ")
    try:
        with open(archivo, "r") as file:
            for line in file:
                nombre, descripcion, categoria, costo = line.strip().split(",")
                costo = float(costo)
                peliculas.append({"nombre": nombre, "descripcion": descripcion, "categoria": categoria, "costo": costo})
                asientos[nombre] = np.zeros((20, 10), dtype=bool)
                ventas[nombre] = 0
                asistentes[nombre] = 0
        print("Películas importadas exitosamente.")
    except FileNotFoundError:
        print("Archivo no encontrado.")

def exportar_peliculas():
    archivo = input("Ingrese el nombre del archivo de exportación: ")
    try:
        with open(archivo, "w") as file:
            for pelicula in peliculas:
                file.write(f"Nombre: {pelicula['nombre']}\n")
                file.write(f"Descripción: {pelicula['descripcion']}\n")
                file.write(f"Categoría: {pelicula['categoria']}\n")
                file.write(f"Costo: {pelicula['costo']}\n")
                file.write("\n")
        print("Películas exportadas exitosamente.")
    except IOError:
        print("Error al escribir el archivo.")

def actualizar_pelicula():
    pelicula = seleccionar_pelicula()
    if pelicula:
        print("Ingrese los nuevos datos de la película:")
        nombre = input("Nombre: ")
        descripcion = input("Descripción: ")
        categoria = input("Categoría: ")
        costo = float(input("Costo: "))
        pelicula["nombre"] = nombre
        pelicula["descripcion"] = descripcion
        pelicula["categoria"] = categoria
        pelicula["costo"] = costo
        print("Película actualizada exitosamente.")

def calcular_ventas():
    print("----- Total de ventas por película -----")
    for pelicula in peliculas:
        nombre = pelicula["nombre"]
        total_ventas = ventas[nombre]
        print(f"{nombre}: ${total_ventas:.2f}")
    print()

def calcular_asistentes():
    print("----- Total de asistentes por película -----")
    for pelicula in peliculas:
        nombre = pelicula["nombre"]
        total_asistentes = asistentes[nombre]
        print(f"{nombre}: {total_asistentes} asistentes")
    print()

# Loop principal del programa
while True:
    mostrar_menu()
    opcion = input("Ingrese una opción: ")

    if opcion == "1":
        agregar_pelicula()
    elif opcion == "2":
        mostrar_peliculas()
    elif opcion == "3":
        reservar_asiento()
    elif opcion == "4":
        mostrar_asientos_disponibles()
    elif opcion == "5":
        comprar_entrada()
    elif opcion == "6":
        importar_peliculas()
    elif opcion == "7":
        exportar_peliculas()
    elif opcion == "8":
        actualizar_pelicula()
    elif opcion == "9":
        calcular_ventas()
    elif opcion == "10":
        calcular_asistentes()
    elif opcion == "11":
        print("¡Hasta luego!")
        break
    else:
        print("Opción inválida. Por favor, ingrese una opción válida.")
