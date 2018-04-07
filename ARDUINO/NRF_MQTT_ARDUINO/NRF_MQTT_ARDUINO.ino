#include<SPI.h>
#include<RF24.h>

#define DEV_ADDR 1

int DEST_ADDR;

int final_msg_length;

String final_message;

// CE, CSN pins
RF24 radio(9, 10);

void setup(void)
{
  while(!Serial);
  Serial.begin(9600);
  
  /*************Radio specific definitions*************/
  radio.begin();
  radio.setPALevel(RF24_PA_MAX);
  radio.setChannel(0x76);
  radio.openWritingPipe(0xF0F0F0F0E1LL);
  const uint64_t pipe = (0xE8E8F0F0E1LL);
  radio.openReadingPipe(1, pipe);
  radio.enableDynamicPayloads();
  radio.powerUp();
  /****************************************************/
  
}

void loop(void)
{
  /**** Simulating random Dstination addresses for now ****/
  DEST_ADDR = random(2, 5);
  /****************************************************/
  
  radio.startListening();
  Serial.println("Starting loop. Radio on.");
  char receivedMessage[32] = {0};
  if(radio.available())
  {
    radio.read(receivedMessage, sizeof(receivedMessage));
    Serial.println(receivedMessage);
    Serial.println("Turning off the radio.");
    radio.stopListening();

    String stringMessage(receivedMessage);

    if(stringMessage == "GETSTRING")
    {
      Serial.println("Looks like they want a string!");
      
      /*************************Framing the final packet ************************************/
      final_message = String(DEV_ADDR) + " MESSAGE FROM NRF " + String(DEST_ADDR);
      /**************************************************************************************/

      final_msg_length = final_message.length();
      Serial.println(final_msg_length);
      final_msg_length += 1;
      //const char text[] = "SOURCE_ADDR Yo wassup, haha" + String(DEST_ADDR);
      const char text[final_msg_length];
      final_message.toCharArray(text, final_msg_length);
      radio.write(text, sizeof(text));
      Serial.println("We sent our message.");
      final_message = "";
      stringMessage = "";
//      receivedMessage = "";
    }
  }
  delay(100);
}
