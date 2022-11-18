#include <RGBmatrixPanel.h>

#define CLK  8   // USE THIS ON ARDUINO UNO, ADAFRUIT METRO M0, etc.
//#define CLK A4 // USE THIS ON METRO M4 (not M0)
//#define CLK 11 // USE THIS ON ARDUINO MEGA
#define OE   9
#define LAT 10
#define A   A0
#define B   A1
#define C   A2

RGBmatrixPanel matrix(A, B, C, CLK, LAT, OE, false);

uint16_t line[4][2];

void setup() {
  matrix.begin();
  line[0][0] = matrix.Color333(1, 0, 0);
  line[1][0] = matrix.Color333(0, 1, 0);
  line[2][0] = matrix.Color333(1, 0, 1);
  line[3][0] = matrix.Color333(1, 1, 0);

  line[0][1] = 0;
  line[1][1] = 1;
  line[2][1] = 2;
  line[3][1] = 3;
}

void loop() {
  // put your main code here, to run repeatedly:'
  matrix.fillScreen(matrix.Color333(0, 0, 0));
  for(int i = 0; i<4; i++){
    int pos = line[i][1]+1;
    if (pos>31){
      pos = 0;
    }
    line[i][1] = pos;
    matrix.drawLine(pos, 0, pos, 15,line[i][0]);
  }
  delay(50);
}
