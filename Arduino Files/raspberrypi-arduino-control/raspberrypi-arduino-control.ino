#define size_message 12
char message[size_message]; //add one to account for the /n
int index = 0;
char mes = '2';
char buf[size_message];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  digitalWrite(12, LOW);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()>0){
//    if(index<size_message){
//      message[index] = Serial.read();
//      index++;
//    }
//  }
//  if(index!=0){
//    Serial.println(message[0]);
//    
//    if(message[0] == mes){
//      digitalWrite(12, HIGH);
//    }
    int rlen = Serial.readBytes(buf,size_message);
    Serial.print("I got: ");
    for(int i = 0; i<size_message; i++){
      Serial.print(buf[i]);
    }
  }
}
