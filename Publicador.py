"""
Publicador
"""

# importing the mqtt library instance and time library
import paho.mqtt.client as mqtt
import time

client = mqtt.Client() # here we are getting the instance of the Client class

exitFlag = True # this is taken for the authentication purpose


client.username_pw_set(username="Javier",password="TICS") # username and password set by me for connection


# ========================Call Backs==========================================================================
def on_publish(client,userdata,mid):        # call back for the published data
    print("Payload Published: "+str(mid))   # printing the message id of the published message


def on_connect(pvtClient,userdata,flags,rc):   # call back for the connection acknowledgement
    global exitFlag # here I am setting the exitFlag based on connection status, we will use this flag later on
    if(rc == 0):  # on successful connection
        print("publisher Connected")  # printing the data
        print("Connected to client! Return Code:"+str(rc)) # printing the data on the screen
        exitFlag = False


    elif(rc ==5): # in case of authentication error
        print("Authentication Error! Return Code: "+str(rc))  # printing the data on the screen
        client.disconnect()
        exitFlag = True


# here we are using this call back for the logs generation, these logs are helpful to us while debugging
def on_log(client, userdata, level, buf):   # call backs for the logs,
    print("Logs: "+str(buf))                # printing the logs on the screen, this will show the logs
    #                                         about the flags that will used by the publisher and subscriber


def on_disconnect(pvtClient, userdata, rc): # this call back will run, when a disconnect() is received
    print("disconnecting reason  " +str(rc))
    client.disconnect()

# ============================================================================================================

# important part
# =================== Associating the functions with the call backs===========================================
client.on_publish       = on_publish
client.on_connect       = on_connect
client.on_log           = on_log
client.on_disconnect    = on_disconnect
# ============================================================================================================


# =======  Establishing Connection ========
host       = "34.229.172.176"
port       = 1883
keepAlive  = 60

client.connect(host,port,keepAlive)
# =========================================


# starting the loop
# we are using this loop and sleep in-between client.connect(...) and client.publish(...)
# so we can observe the call backs
client.loop_start();        # starting a loop in order to observe the call backs
time.sleep(2)               # giving a sleep time for the connection to setup

# once connected, publish the message
# ============Publishing the message ======
topic_name = "Proyecto/sensor2"
QOS        = 2                  # here we can use different Quality of service, based on our requirement
retain     = True

# if the connection is successful then this while loop will run
while(exitFlag == False):   # here we are using the flags which we have set earlier,
    time.sleep(.5)          # giving some time for the call backs to process
    payload = input("\nMessage: ")
    client.publish(topic_name,payload,QOS,retain)  # publishing the message (payload)
    if(payload == "exit(0)"):   # in case user has entered "exit(0)" then exit and disconnect
        client.disconnect()