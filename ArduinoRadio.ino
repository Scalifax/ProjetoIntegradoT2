const int b_A1 = A1, b_A2 = A2, b_A3 = A3, b_A4 = A4, b_A5 = A5, b_Erro = 8, led_FreqChange = 2, led_Erro = 3; //Button pins and Led pins
bool Break = 0, sb_Erro = 0, emergency_off = 1, reset_rx = 1; //Variable for the switch logic

//Storing message for/from the Serial:
String rx = " ";

//------------------------------------------Radio declaration:
int received = 0, current_freq = 0;
const int d0 = 4, d1 = 5, d2 = 6, d3 = 7;

struct radio{
  bool d0, d1, d2, d3;
};

//Radio frequency table:
struct radio F87_7M = {0, 0, 0, 0};  //87.7[MHz]
struct radio F87_9M = {1, 0, 0, 0};  //87.9[MHz]
struct radio F88_1M = {0, 1, 0, 0};  //88.1[MHz]
struct radio F88_3M = {1, 1, 0, 0};  //88.3[MHz] 
struct radio F88_5M = {0, 0, 1, 0};  //88.5[MHz]
struct radio F88_7M = {1, 0, 1, 0};  //88.7[MHz]
struct radio F88_9M = {0, 1, 1, 0};  //88.9[MHz] 
struct radio F106_7M = {0, 0, 0, 1}; //106.7[MHz]
struct radio F106_9M = {1, 0, 0, 1}; //106.9[MHz]
struct radio F107_1M = {0, 1, 0, 1}; //107.1[MHz]
struct radio F107_3M = {1, 1, 0, 1}; //107.3[MHz]
struct radio F107_5M = {0, 0, 1, 1}; //107.5[MHz]
struct radio F107_7M = {1, 0, 1, 1}; //107.7[MHz]
struct radio F107_9M = {0, 1, 1, 1}; //107.9[MHz]

void set_pins(struct radio *freq){ //Set the pins to order set on the struct
  digitalWrite(d0, freq->d0);
  digitalWrite(d1, freq->d1);
  digitalWrite(d2, freq->d2);
  digitalWrite(d3, freq->d3);

  for(int i = 0; i < 3; i++){ //Show using an LED that the pins have been set
    digitalWrite(led_FreqChange, 1);
    delay(250);
    digitalWrite(led_FreqChange, 0);
    delay(250);
  }
}

void setFrequency(int received_freq){ //Switch case to set the frequency
  switch(received_freq){
      case 877:
        set_pins(&F87_7M);
        break;
      case 879:
        set_pins(&F87_9M);
        break;
      case 881:
        set_pins(&F88_1M);
        break;
      case 883:
        set_pins(&F88_3M);
        break;
      case 885:
        set_pins(&F88_5M);
        break;
      case 887:
        set_pins(&F88_7M);
        break;
      case 889:
        set_pins(&F88_9M);
        break;
      case 1067:
        set_pins(&F106_7M);
        break;
      case 1069:
        set_pins(&F106_9M);
        break;
      case 1071:
        set_pins(&F107_1M);
        break;
      case 1073:
        set_pins(&F107_3M);
        break;
      case 1075:
        set_pins(&F107_5M);
        break;
      case 1077:
        set_pins(&F107_7M);
        break;
      case 1079:
        set_pins(&F107_9M);
        break;
  }
}

bool debug = false;

void setup() {
  
  //Pin mode definition:
  pinMode(b_Erro, INPUT_PULLUP);
  pinMode(led_Erro, OUTPUT);
  pinMode(led_FreqChange, OUTPUT);
  pinMode(d0, OUTPUT);
  pinMode(d1, OUTPUT);
  pinMode(d2, OUTPUT);
  pinMode(d3, OUTPUT);

  Serial.begin(115200); //Serial Initialized
}

void loop() {

  sb_Erro = digitalRead(b_Erro); //Reads the emergency button

  //-------Switch for the emergency button logic:
  if(!sb_Erro && !Break){

    switch(emergency_off){
      case 0:
        if(debug){
          Serial.println("Emergency mode deactivate");
        }
        emergency_off = 1;
      break;

      case 1:
        if(debug){
          Serial.println("Emergency mode activate");
        }
        setFrequency(877); //Set the communcation frequency to the one with bigger range
        current_freq = 877;
        emergency_off = 0;
      break;
    }
    
    Break = 1;
  }
  else if(sb_Erro){
    Break = 0;
  }

  //----------Main Button/Serial/Frequency logic:

  if(debug){
    Serial.println("--------Main loop started--------");
  }
  
  //Verify the area button pressed:
  if(analogRead(b_A1) <= 10){
    Serial.write('A');
  }
  else if(analogRead(b_A2) <= 10){
    Serial.write('B');
  }
  else if(analogRead(b_A3) <= 10){
    Serial.write('C');
  }
  else if(analogRead(b_A4) <= 10){
    Serial.write('D');
  }
  else if(analogRead(b_A5) <= 10){
    Serial.write('E');
  }


  //Receive the frequency using Serial:
  while(Serial.available()){
    
    if(reset_rx){
      rx = "";
      reset_rx = 0;
    }

    char temp = (char)Serial.read();
    rx += temp;
  }

  if(rx != "" && debug){ //DEBUG
    Serial.print("\n");
    Serial.println(rx);
  }

  if(rx == "X"){ //Veirfy if it is the connection erro message
      digitalWrite(led_Erro, 1);
      delay(500);
      digitalWrite(led_Erro, 0);
      delay(500);
  }
  else{
    received = rx.toInt(); //converts string to int
    if(received != current_freq && emergency_off == 1){ //Check if it's a new frequency

      current_freq = received;
      setFrequency(current_freq); //Changes the radio freq
    }
  }

  if(debug){
    Serial.print("\n");
    delay(500);
  }

  reset_rx = 1;
  delay(500);
}
