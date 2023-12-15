# Proyecto-IoT
Proyecto Final Laboratorio TICS

Los códigos Publicador.py y Suscriptor.py están hechos para probar la conexión al servidor MQTT. Como lo dice su nombre, la función del primero es enviar mensajes al servidor mientras que los del segundo únicamente es recibirlos.
Por otro lado, NB-IoT corresponde al código que utiliza la placa de los sensores para enviar los datos. Como se puede ver, es prácticamente idéntica al código utilizado en la experiencia de laboratorio salvo algunos cambios como la dirección a la que se deben enviar los datos.

En relación a la recepción e implementación del dashboard solicitado, los archivos Receptor_MQTT y Visualizador contienen el código implementado para recibir datos del servidor MQTT de forma continua y almacenarlos en una base de datos desarrollada en MariaDB. 

Finalmente, el arhivo alerta contiene el código desarrollado para establecer un sistema que permita notificar al usuario de alguna vulneración de los niveles establecidos. 
