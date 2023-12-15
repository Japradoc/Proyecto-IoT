#include <Arduino.h>
#include <Wire.h>
#include <SparkFun_SHTC3.h>
#include <StarterKitNB.h>
#include "ADC121C021.h"


//Definitions
#define EN_PIN WB_IO6	 //Logic high enables the device. Logic low disables the device
#define ALERT_PIN WB_IO5 //a high indicates that the respective limit has been violated.
#define MQ2_ADDRESS 0x51 //the device i2c address
#define RatioMQ2CleanAir (1.0) //RS / R0 = 1.0 ppm
#define MQ2_RL (10.0)		   //the board RL = 10KΩ  can adjust

#define PIN_VBAT WB_A0
#define VBAT_MV_PER_LSB (0.73242188F) // 3.0V ADC range and 12 - bit ADC resolution = 3000mV / 4096
#define VBAT_DIVIDER_COMP (1.73)      // Compensation factor for the VBAT divider, depend on the board (por default 1.73); 1905
#define REAL_VBAT_MV_PER_LSB (VBAT_DIVIDER_COMP * VBAT_MV_PER_LSB)

// Objects
StarterKitNB sk;
SHTC3 mySHTC3;
ADC121C021 MQ2;

// NB-IoT
String apn="m2m.entel.cl";
String user="entelpcs";
String password="entelpcs";
String band="B2A8 LTE";
String Network="NB";

// MQTT
String clientID = "111";
String userBroker = "jvargas20";
String passwordBroker = "";
String broker ="34.229.172.176";
int port = 1883;

// msg
String topic1 ="Proyecto/sensor1";
String topic2="Proyecto/sensor2";
String topic3="jvargas20/feeds/PPM";
String topic4="jvargas20/feeds/voltajeBateria";
float batery;             

// temp&hum
String hum = "";
String temp = "";
void errorDecoder(SHTC3_Status_TypeDef message)             
{
  switch(message)
  {
    case SHTC3_Status_Nominal : Serial.println("Nominal"); break;
    case SHTC3_Status_Error : Serial.println("Error"); break;
    case SHTC3_Status_CRC_Fail : Serial.println("CRC Fail"); break;
    default : Serial.println("Unknown return code"); break;
  }
}

// PPM
float sensorPPM;

void setup() {

  sk.Setup();
  delay(500);

  Wire.begin();
  errorDecoder(mySHTC3.begin()); 
  delay(500);
  pinMode(ALERT_PIN, INPUT);
	pinMode(EN_PIN, OUTPUT);
	digitalWrite(EN_PIN, HIGH);
  while (!(MQ2.begin(MQ2_ADDRESS, Wire)))
	{
		Serial.println("please check gas device!!!");
		delay(200);
	}
  MQ2.configCycleTime(CYCLE_TIME_32);
	MQ2.configAlertHold(Disable);		
	MQ2.configAlertFlag(Disable);		
	MQ2.configAlertPin(Enable);			
	MQ2.configPolarity(High);			
	MQ2.setAlertLowThreshold(1);		
	MQ2.setAlertHighThreshold(2500);	 
  MQ2.setRL(MQ2_RL);
	MQ2.setA(-0.890);			
	MQ2.setB(1.125);			
	MQ2.setRegressionMethod(0); 
  float calcR0 = 0;
	
  /*
    Codigo para conectarse a NB-IoT
  */
  sk.UserAPN(apn, user, password);  // Define las credenciales de la red al dispositivo a NB
  delay(1000);
  sk.Connect(apn, band, Network);  // Se conecta a NB
  delay(1000);

}

void loop() {

  /*
    Codigo para verificar la conexión a NB-IoT
  */
  sk.ConnectionStatus();

  sk.bg77_at((char *)"AT+QCSQ", 500);  // Comando "AT+QCSQ"
  delay(1000);
  sk.bg77_at((char *)"AT+CEREG?", 500);  // Comando "AT+CEREG?"
  delay(1000);

  SHTC3_Status_TypeDef result = mySHTC3.update();
  hum = String(mySHTC3.toPercent());
  temp = String(mySHTC3.toDegC());
  sensorPPM = MQ2.readSensor();
  batery = (analogRead(PIN_VBAT) * REAL_VBAT_MV_PER_LSB /1000);

  /*
    Codigo para hacer los print con "Serial.prinln(variable);"
  */
  Serial.println("Humedad");
  Serial.println(hum);
  Serial.println("Temperatura");
  Serial.println(temp);
  Serial.println("Sensor PPM");
  Serial.println(sensorPPM);
  Serial.println("Batería");
  Serial.println(batery);
  /*
    Código para ver si el último mensaje fue enviado, sino se conecta al broker
  */
  if (!sk.ConnectionStatus()) // Si no hay conexion a NB
  {
    sk.Reconnect(apn);  // Se intenta reconecta
    delay(2000);
  }
  if (!sk.LastMessageStatus)  // Si no se ha enviado el ultimo mensaje
  {
    sk.ConnectBroker(clientID, userBroker, passwordBroker, 0, broker, port);  // Se conecta a ThingsBoard
    delay(2000);
  }
  /*
    Codigo para enviar mensajes al broker
  */
  sk.SendMessage(temp, topic1, 0, 0, 0, 0, 10000);    // Se envia el mensaje
  delay(2000);

  sk.SendMessage(hum, topic2, 0, 0, 0, 0, 10000);    // Se envia el mensaje
  delay(2000);

  sk.SendMessage(String(sensorPPM), topic3, 0, 0, 0, 0, 10000);    // Se envia el mensaje
  delay(2000);

  sk.SendMessage(String(batery), topic4, 0, 0, 0, 0, 10000);    // Se envia el mensaje
  delay(2000);

}
