import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from threading import Thread
import time
import tkinter as tk


# Datos iniciales (puedes usar tus propios datos)
x = []
y1 = []
y2 = []

# Conectar a la base de datos
def conectar_bd():
    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="exequiel3120",
        database="bd_prueba"
    )
    return conexion

# Función para obtener datos de la base de datos
def obtener_datos():
    global x, y1, y2
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT Temperatura, Humedad FROM bd")
    resultados = cursor.fetchall()
    x = list(range(1, len(resultados) + 1))
    y1 = [resultado[0] for resultado in resultados]
    y2 = [resultado[1] for resultado in resultados]
    cursor.close()
    conexion.close()

# Función de actualización del gráfico
def actualizar_grafico(frame):
    plt.clf()
    obtener_datos()
    plt.subplot(2, 2, 1)
    plt.plot(x, y1, marker='o')
    plt.title('Medición de Temperatura')
    plt.xlabel('Índice')
    plt.ylabel('Valor [C°]')
    plt.ylabel('Valor [g/m3]')
  


    plt.subplot(2, 2, 2)
    plt.plot(x, y2, marker='o', color='orange')
    plt.title('Medición de Humedad')
    plt.xlabel('Índice')
    plt.ylabel('Valor [g/m3]')



# Función principal para la animación
def animacion():
    ani = FuncAnimation(plt.gcf(), actualizar_grafico, interval=1000)
    plt.show()
    caja_alerta()

# Función principal para el hilo
def main():
    obtener_datos()

    thread_animacion = Thread(target=animacion)
    thread_animacion.start()

    # Actualizar datos continuamente en segundo plano
    while True:
        time.sleep(2)
        obtener_datos()


# Iniciar el programa
if __name__ == '__main__':
    main()