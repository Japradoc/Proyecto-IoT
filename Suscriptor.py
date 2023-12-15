"""
Suscriptor
"""
    
import paho.mqtt.client as mqtt
import time


client      =   mqtt.Client()
topicName   =   "Proyecto/sensor1"
QOS_val        =   2

client.username_pw_set(username="Exequiel",password="TICS")

# --------------- Callbacks ---------------------------------------------------------------
def on_connect(pvtClient,userdata,flags,rc):
    if(rc == 0):  # en conexión exitosa
        print("Connected to client! Return Code:"+str(rc)) # se printea la data obtenida
        result = client.subscribe(topicName, QOS_val) 

    elif(rc ==5): # en caso de error de autenticación
        print("Authentication Error! Return Code: "+str(rc))  
        client.disconnect()


#           Callback para el mensaje
def on_message(pvtClient, userdata, msg):
    # extraemos datos del mensaje obtenido,
    print("\n============================================")
    print("Payload       : " +str(msg.payload.decode()))
    print("Message Topic : "+str(msg.topic))
    print("============================================\n")

    if(msg.payload.decode() == "exit(0)" ):
        client.disconnect()


def on_log(topic, userdata, level, buf):
    print("Logs: "+str(buf))

client.on_connect   =   on_connect
client.on_message   =   on_message
client.on_log       =   on_log

host        = "34.229.172.176"
port        = 1883
keepAlive   = 60

client.connect(host,port,keepAlive) # establecemos la conexión

time.sleep(2)               # dejamos un espacio de tiempo

client.loop_forever()   