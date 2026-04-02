
while True:
    print("""
   Bienvenido al programa calculadora 2024\nEste es el Menu principal de Operaciones
   1)Suma
   2)Sustracción
   3)Multiplicación
   4)División
   5)Salir
    """)
    Opción= int(input("Por favor elija la operación que desea realizar: "))
    
    if Opción == 1:
        Operador1 = float(input("Ingresa un número: "))
        Operador2 = float(input("Ingresa otro número: "))
        Suma=Operador1 + Operador2
        print("El resultado de la suma es:", Suma)
    elif Opción == 2:
        Operador1 = float(input("Ingresa un número: "))
        Operador2 = float(input("Ingresa otro número: "))
        Resta=Operador1 - Operador2
        print("El resultado de la resta es:", Resta)
    elif Opción == 3:
        Operador1 = float(input("Ingresa un número: "))
        Operador2 = float(input("Ingresa otro número: "))
        Producto=Operador1* Operador2
        print("El resultado de la multiplicación es:",  Producto)
    elif Opción == 4:
            Operador1 = float(input("Ingresa un número: "))
            Operador2 = float(input("Ingresa otro número: "))
            if Operador2==0:
                print("Se ha generado un error matemático, no puede dividir un número por cero.")
            else:
                Cociente = Operador1 / Operador2
                print("El resultado de la división es:", Cociente)
    elif Opción == 5:
        print("Gracias por utilizar la calculadora creada por Javier Hasta pronto!.")
        break