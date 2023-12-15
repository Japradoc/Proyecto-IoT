import paho.mqtt.client as mqtt
import pymysql

# Configuración de MQTT
mqtt_broker = "34.229.172.176"
mqtt_topic1 = "Proyecto/sensor1"
mqtt_topic2 = "Proyecto/sensor2"
# Configuración de MariaDB
db_host = "localhost"
db_user = "root"
db_password = "exequiel3120"
db_name = "bd_prueba"
tabla = "bd"

# Columna específica en la que deseas insertar datos
def columna_especifica(topico):
    if topico == mqtt_topic1:
        return "Temperatura"
    else:
        return "Humedad"


# Función de callback al recibir un mensaje MQTT
def on_message(client, userdata, msg):
    message = msg.payload.decode("utf-8")
    insertar_en_mariadb(msg.topic, message)

# Función para insertar datos en MariaDB en una columna específica
def insertar_en_mariadb(topico, mensaje):
    print(topico)
    connection = pymysql.connect(host=db_host, user=db_user, password=db_password, database=db_name)
    cursor = connection.cursor()

    try:
        # Personaliza la consulta según tus necesidades
        consulta = f"INSERT INTO bd ({columna_especifica(topico)}) VALUES (%s)"
        cursor.execute(consulta, (mensaje,))
        connection.commit()
        print("Datos insertados correctamente en MariaDB.")
        # visualizar datos de la tabla de la base.
        # Consulta SQL para seleccionar los datos de la columna
        sql_seleccionar = f"SELECT {columna_especifica(topico)} FROM {tabla}"

        # Ejecutar la consulta
        cursor.execute(sql_seleccionar)

        # Obtener los resultados
        resultados = cursor.fetchall()

        # Imprimir los datos
        print(f'Datos de la columna {columna_especifica(topico)}:')
        for resultado in resultados:
            print(resultado[0])

    except Exception as e:
        print(f"Error al insertar en MariaDB: {e}")
    finally:
        cursor.close()
        connection.close()


# Configuración del cliente MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect(mqtt_broker, 1883, 60)
client.subscribe(mqtt_topic1)
client.subscribe(mqtt_topic2)
client.loop_start()

# Esperar por siempre (puedes personalizar esto según tus necesidades)
try:
    while True:
        pass
except KeyboardInterrupt:
    print("Programa interrumpido por el usuario")

client.loop_stop()
client.disconnect()
