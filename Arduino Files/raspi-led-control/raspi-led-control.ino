#include <RGBmatrixPanel.h>

#define CLK  8   // USE THIS ON ARDUINO UNO, ADAFRUIT METRO M0, etc.
//#define CLK A4 // USE THIS ON METRO M4 (not M0)
//#define CLK 11 // USE THIS ON ARDUINO MEGA
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2

#define horizontal_length 32
#define num_bars 32
#define num_parameters 2
#define overhead_length 1
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

#define size_message num_bars+overhead_length
#define data_size num_bars*num_parameters

//Variabe to store all of the bar data, color and height
uint16_t line[num_bars][num_parameters];


int middle_mode = 1;
int middle_height = 0;

//buffer for data
byte buf[size_message];
int line_index = 0;

//common colors
uint16_t red;
uint16_t white;
uint16_t blue;
uint16_t green;
uint16_t color_list[4];

void setup() {
  Serial.begin(115200);
  matrix.begin();
  red = matrix.Color333(1, 0, 0);
  white = matrix.Color333(1, 1, 1);
  blue = matrix.Color333(0, 0, 1);
  green =  matrix.Color333(0,1,0);
  //Initialize all of the bars
  color_list[0] = red;
  color_list[1] = white;
  color_list[2] = blue;
  color_list[3] = green;
}
                                                                                          
void loop() {
  while(Serial.available()>0){
    Serial.readBytes(buf ,size_message);
    middle_mode = buf[0];
    for(int index=0; index<num_bars; index+=1){
      line[index][0]= (int)(buf[index+1]&0b1111) >= 15 ? 15 : buf[index+1]&0b1111;
      int color = (buf[index+1]>>4);
      line[index][1]= color_list[color];
    }
  }
 
  matrix.fillScreen(matrix.Color333(0, 0, 0));
  //draw all of the lines
  for(int i=0; i<num_bars; i++){
    if(!middle_mode){
      matrix.drawLine(horizontal_length-1-i, 0, horizontal_length-1-i, line[i][0], line[i][1]);
    }
    else{
      middle_height = line[i][0]/2;
      matrix.drawLine(horizontal_length-1-i, (7-middle_height), horizontal_length-1-i, (7+middle_height), line[i][1]);
    }
  }
  delay(20);
}
