#include <RGBmatrixPanel.h>

#define CLK  8   // USE THIS ON ARDUINO UNO, ADAFRUIT METRO M0, etc.
//#define CLK A4 // USE THIS ON METRO M4 (not M0)
//#define CLK 11 // USE THIS ON ARDUINO MEGA
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2

//parameters defining the data comming in 
#define horizontal_length 32
#define num_bars 32
#define num_parameters 2
#define overhead_length 1 // one extra byte for whether to use middle mode or not

//class object to control the LED screen
RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

//constants for the size of the whole message
#define size_message num_bars+overhead_length
#define data_size num_bars*num_parameters

//Variabe to store all of the bar data, color and height
uint16_t line[num_bars][num_parameters];

//Variables to control middle mode or not
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
  //Setup the serial module
  Serial.begin(115200);
  matrix.begin();
  //get the values for all the colors
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
    //Read in the serial data
    Serial.readBytes(buf ,size_message);
    //capture the middle mode byte
    middle_mode = buf[0];
    //extract the column data for each frequency bin
    for(int index=0; index<num_bars; index+=1){
      line[index][0]= (int)(buf[index+1]&0b1111) >= 15 ? 15 : buf[index+1]&0b1111;
      int color = (buf[index+1]>>4);
      line[index][1]= color_list[color];
    }
  }
 
  matrix.fillScreen(matrix.Color333(0, 0, 0));
  //draw all of the lines 
  for(int i=0; i<num_bars; i++){
    //put them starting from the center if its in middle mode
    if(!middle_mode){
      matrix.drawLine(horizontal_length-1-i, 0, horizontal_length-1-i, line[i][0], line[i][1]);
    }
    //run in normal mode
    else{
      middle_height = line[i][0]/2;
      matrix.drawLine(horizontal_length-1-i, (7-middle_height), horizontal_length-1-i, (7+middle_height), line[i][1]);
    }
  }
  //do some delaay before reading serial data again
  delay(20);
}
