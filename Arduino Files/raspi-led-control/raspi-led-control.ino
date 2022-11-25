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
#define num_bars 2
#define num_parameters 2
#define overhead_length 2
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

#define size_message num_bars*num_parameters+overhead_length
#define data_size num_bars*num_parameters

//Variabe to store all of the bar data, color and height
uint16_t line[num_bars][num_parameters];

//buffer for data
byte buf[size_message];
int line_index = 0;

//common colors
uint16_t red;
uint16_t white;
uint16_t blue;

void setup() {
  Serial.begin(115200);
  matrix.begin();
  red = matrix.Color333(1, 0, 0);
  white = matrix.Color333(1, 1, 1);
  blue = matrix.Color333(1, 0, 1);
  //Initialize all of the bars
  for(int i=0; i<num_bars; i++){
    line[i][0]=1;
    line[i][1]=white;
  }
}
                                                                                          
void loop() {
  while(Serial.available()>0){
    Serial.readBytes(buf ,size_message);
    if(buf[0] == 0x23){
      for(int buf_index=1; buf_index<data_size; buf_index+=2){
        line[line_index][0]=buf[buf_index];
        int color = buf[buf_index+1];
        if (color == 1){
          color = red;
        }
        else if (color = 2){
          color = white;
        }
        else{
          color = blue;
        }
        line[line_index][1]= color;
        line_index++;
      }
      line_index = 0;
    }
  }
 
  
  matrix.fillScreen(matrix.Color333(0, 0, 0));
  //draw all of the lines
  for(int i=0; i<num_bars; i++){
    matrix.drawLine(horizontal_length-1-i, 0, horizontal_length-i, line[i][0], line[i][1]);
  }
  delay(50);
}
