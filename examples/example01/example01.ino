#include <SPI.h>
#include <Ethernet.h>
#include <EthernetUdp.h>
#include <Genibus.h>

#define GB_MASTER_ADDRESS  0x01

byte macAddress[] = { 0xde, 0xad, 0xaf, 0xfe, 0xaa, 0x55  };
byte subnet[] = { 255, 255, 255, 0 };
unsigned int localPort = 6734;

/* TODO: The IP-configuration has to be adjusted to your needs!!! */
IPAddress ipAddress(192, 168, 100, 20);
byte gateway[] = { 192, 168, 100, 1 };

#define LED_PIN  13  /* Pin 13 has an LED connected on most Arduino boards, otherwise this should be changed. */


void writeByte(byte value)
{
  /* TODO: Write to UDP, LCD or an additional serial port. */  
}

void setup(void)
{
 
  pinMode(LED_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  Serial.begin(9600);
  Ethernet.begin(macAddress, ipAddress);
 
/*
** 'Udp.begin()' generates a strange
**   "As of Arduino 1.0, the Udp class in the Ethernet library has been renamed to EthernetClient."
** compiler error (This doesn't hold for Arduino examples).
*/
//  Udp.begin(localPort);
  
  delay(1000); 
}

void loop(void)
{
  byte receivedByte;
  byte byteCount;
  byte idx;
  
  connectRequest(GB_MASTER_ADDRESS);
  while (Serial.available() == 0) {
    /* Blocking for now. */
  }
  /* Well, it seems the pump is talking to us :-) */
  digitalWrite(LED_PIN, HIGH);

  idx = 0;
  while (Serial.available() > 0) {  /* We are not considering inter-byte delays -- reception may prematurely terminate !? */
    receivedByte = Serial.read();
    ++idx;
    writeByte(receivedByte);
  }
  
  delay(2000);
}
