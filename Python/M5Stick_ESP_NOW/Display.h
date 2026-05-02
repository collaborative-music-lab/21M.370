#pragma once
#include <Arduino.h>
#include <SPI.h>

// ST7789 commands
#define ST7789_SWRESET  0x01
#define ST7789_SLPOUT   0x11
#define ST7789_DISPON   0x29
#define ST7789_CASET    0x2A
#define ST7789_RASET    0x2B
#define ST7789_RAMWR    0x2C
#define ST7789_MADCTL   0x36
#define ST7789_COLMOD   0x3A

// RGB565 color constants
const uint16_t COLOR_BLACK = 0x0000;
const uint16_t COLOR_WHITE = 0xFFFF;
const uint16_t COLOR_RED   = 0xF800;
const uint16_t COLOR_GREEN = 0x07E0;
const uint16_t COLOR_PINK  = 0xF81F;  // Red + Blue = pink

/****
FONTs
****/

const uint8_t font5x7[][5] PROGMEM = {
  {0x00,0x00,0x00,0x00,0x00}, // space
  {0x00,0x00,0x5F,0x00,0x00}, // !
  {0x00,0x07,0x00,0x07,0x00}, // "
  {0x14,0x7F,0x14,0x7F,0x14}, // #
  {0x24,0x2A,0x7F,0x2A,0x12}, // $
  {0x23,0x13,0x08,0x64,0x62}, // %
  {0x36,0x49,0x55,0x22,0x50}, // &
  {0x00,0x05,0x03,0x00,0x00}, // '
  {0x00,0x1C,0x22,0x41,0x00}, // (
  {0x00,0x41,0x22,0x1C,0x00}, // )
  {0x14,0x08,0x3E,0x08,0x14}, // *
  {0x08,0x08,0x3E,0x08,0x08}, // +
  {0x00,0x50,0x30,0x00,0x00}, // ,
  {0x08,0x08,0x08,0x08,0x08}, // -
  {0x00,0x60,0x60,0x00,0x00}, // .
  {0x20,0x10,0x08,0x04,0x02}, // /

  // Digits
  {0x3E,0x51,0x49,0x45,0x3E}, // 0
  {0x00,0x42,0x7F,0x40,0x00}, // 1
  {0x42,0x61,0x51,0x49,0x46}, // 2
  {0x21,0x41,0x45,0x4B,0x31}, // 3
  {0x18,0x14,0x12,0x7F,0x10}, // 4
  {0x27,0x45,0x45,0x45,0x39}, // 5
  {0x3C,0x4A,0x49,0x49,0x30}, // 6
  {0x01,0x71,0x09,0x05,0x03}, // 7
  {0x36,0x49,0x49,0x49,0x36}, // 8
  {0x06,0x49,0x49,0x29,0x1E}, // 9
};

class M5LCD {
public:
  void begin() {
    // Pins
    pinMode(TFT_DC, OUTPUT);
    pinMode(TFT_RST, OUTPUT);
    pinMode(TFT_CS, OUTPUT);
    digitalWrite(TFT_CS, HIGH);

    // Reset
    digitalWrite(TFT_RST, LOW);
    delay(50);
    digitalWrite(TFT_RST, HIGH);
    delay(150);

    // SPI init
    SPI.begin(TFT_SCLK, -1, TFT_MOSI, TFT_CS);
    SPI.beginTransaction(SPISettings(40000000, MSBFIRST, SPI_MODE0));

    sendCmd(ST7789_SWRESET); delay(150);
    sendCmd(ST7789_SLPOUT);  delay(150);
    sendCmd(ST7789_COLMOD);  sendData(0x55); // 16-bit color
    sendCmd(ST7789_MADCTL);  sendData(0x70);//sendData(0x70); // RGB order + row/col swap
    sendCmd(ST7789_DISPON);  delay(150);
  }

  void drawPixel(int x, int y, uint16_t color) {
    if (x < 0 || y < 0 || x >= WIDTH || y >= HEIGHT) return;
    setAddrWindow(x, y, x, y);
    sendCmd(ST7789_RAMWR);
    sendData16(swapBytes(color));
  }

  // RGB565 helper
  static uint16_t rgb(uint8_t r, uint8_t g, uint8_t b) {
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3);
  }

  void drawChar(int x, int y, char c, uint16_t color) {
    if (c < 32 || c > 57) return; // digits + punctuation
    const uint8_t* chr = font5x7[c - 32];

    for (int i = 0; i < 5; i++) {
      uint8_t col = pgm_read_byte(&chr[i]);
      for (int j = 0; j < 7; j++) {
        if (col & (1 << j)) {
          // Draw a font_scale x font_scale block for each pixel
          for (int dx = 0; dx < font_scale; dx++) {
            for (int dy = 0; dy < font_scale; dy++) {
              drawPixel(x + i * font_scale + dx, y + j * font_scale + dy, color);
            }
          }
        }
      }
    }
  }

  void drawText(int x, int y, const char* text, uint16_t color) {
    while (*text) {
      drawChar(x*font_scale, y*font_scale, *text++, color);
      x += 6 * font_scale;
    }
  }

  void backlight(bool enable) {
    Wire1.beginTransmission(0x34);
    Wire1.write(0x12);  // Power Output Control register
    Wire1.endTransmission(false);
    Wire1.requestFrom(0x34, 1);

    if (!Wire1.available()) {
      Serial.println("AXP192: Failed to read power control register");
      return;
    }

    uint8_t pwr = Wire1.read();

    if (enable) {
      // Enable LDO2 (bit 2)
      pwr |= (1 << 2);
      
      // Optional: set voltage to 3.0V for LDO2 (register 0x28)
      Wire1.beginTransmission(0x34);
      Wire1.write(0x28);
      Wire1.write(0xCC);  // 0xCC = 3.0V
      Wire1.endTransmission();
    } else {
      // Disable LDO2 (bit 2)
      pwr &= ~(1 << 2);
    }

    Wire1.beginTransmission(0x34);
    Wire1.write(0x12);
    Wire1.write(pwr);
    Wire1.endTransmission();

    Serial.print("Backlight ");
    Serial.println(enable ? "enabled" : "disabled");
  }
  int font_scale = 1;

  void fill(uint16_t color) {
    setAddrWindow(0, 0, WIDTH - 1, HEIGHT - 1);
    sendCmd(ST7789_RAMWR);
    digitalWrite(TFT_DC, HIGH);
    digitalWrite(TFT_CS, LOW);
    for (uint32_t i = 0; i < WIDTH * HEIGHT; ++i) {
      SPI.write16(swapBytes(color));
    }
    digitalWrite(TFT_CS, HIGH);
  }

private:
  static const int TFT_CS   = 5;
  static const int TFT_DC   = 23;
  static const int TFT_RST  = 18;
  static const int TFT_MOSI = 15;
  static const int TFT_SCLK = 13;

  static const int WIDTH = 240;
  static const int HEIGHT = 135;

  void sendCmd(uint8_t cmd) {
    digitalWrite(TFT_DC, LOW);
    digitalWrite(TFT_CS, LOW);
    SPI.write(cmd);
    digitalWrite(TFT_CS, HIGH);
  }

  void sendData(uint8_t data) {
    digitalWrite(TFT_DC, HIGH);
    digitalWrite(TFT_CS, LOW);
    SPI.write(data);
    digitalWrite(TFT_CS, HIGH);
  }

  void sendData16(uint16_t data) {
    digitalWrite(TFT_DC, HIGH);
    digitalWrite(TFT_CS, LOW);
    SPI.write16(data);
    digitalWrite(TFT_CS, HIGH);
  }

  void setAddrWindow(uint16_t x0, uint16_t y0, uint16_t x1, uint16_t y1) {
    x0 += 40; x1 += 40; // Horizontal offset
    y0 += 53; y1 += 53; // Vertical offset

    sendCmd(ST7789_CASET); // Column address set
    sendData16(x0);
    sendData16(x1);

    sendCmd(ST7789_RASET); // Row address set
    sendData16(y0);
    sendData16(y1);
  }

  uint16_t swapBytes(uint16_t c) {
    return (c >> 8) | (c << 8);
  }
};
