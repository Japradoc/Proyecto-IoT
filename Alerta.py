import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error


def mostrar_ventana(val1, val2):
    ventana = tk.Tk()
    ventana.title("Valores parámetros")

    etiqueta1 = tk.Label(ventana, text=f"Temperatura: {val1}")
    etiqueta1.pack()

    etiqueta2 = tk.Label(ventana, text=f"Humedad: {val2}")
    etiqueta2.pack()

    ventana.after(1000, ventana.destroy)


# Función para verificar la condición y mostrar la alerta
def verificar_umbral():
    try:
        # Conectar a la base de datos (reemplaza con tus credenciales)
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='exequiel3120',
            database='bd_prueba'
        )

        if connection.is_connected():
            global x, y1, y2
            cursor = connection.cursor()
            # Ejemplo: Obtener los dos últimos valores de las dos columnas de la base de datos
            cursor.execute("SELECT Temperatura, Humedad FROM bd")
            resultados = cursor.fetchall()
            x = list(range(1, len(resultados) + 1))
            y1 = [resultado[0] for resultado in resultados]
            y2 = [resultado[1] for resultado in resultados]
            print(resultados)
            print(y1)
            print(y2)

            # Establecer un umbral (reemplaza 10 y 20 con tus valores umbral)
            umbral_Temperatura = 40
            umbral_Humedad = 40
            mostrar_ventana(y1[len(y1)-1],y2[len(y2)-1])

            # Verificar la condición
            if y1[len(y1)-1] is None:
                pass
            elif y1[len(y1)-1] > umbral_Temperatura:
                # Mostrar una caja de alerta
                messagebox.showwarning("Alerta", "Se ha superado el umbral de temperatura")
                messagebox.after(1000, messagebox.destroy)

                print(y1[len(y1)-1])
                print(y2[len(y2)-1])

            if y2[len(y2)-1] is None:
                print(y1[len(y1)-1])
                print(y2[len(y2)-1])
                pass
            elif y2[len(y2)-1] > umbral_Humedad:
                # Mostrar una caja de  alerta
                messagebox.showwarning("Alerta", "Se ha superado el umbral de Humedad")
                messagebox.after(1000, messagebox.destroy)
                print(y1[len(y1)-1])
                print(y2[len(y2)-1])
            # Cerrar el cursor y confirmar los cambios (si los hay)
            cursor.close()
            connection.commit()

    except Error as e:
        print(f"Error: {e}")

    finally:
        # Cerrar la conexión a la base de datos
        if connection.is_connected():
            connection.close()

        # Repetir la verificación después de un cierto tiempo (por ejemplo, 5000 milisegundos = 5 segundos)
        root.after(2000, verificar_umbral)

# Crear la ventana principal
root = tk.Tk()
root.title("Caja de Alerta")
mensaje_centro = tk.Label(root, text=f"Analizando mediciones...")
mensaje_centro.pack()


# Llamar a la función para iniciar la verificación
verificar_umbral()

# Iniciar el bucle principal de la interfaz gráfica
root.mainloop()
