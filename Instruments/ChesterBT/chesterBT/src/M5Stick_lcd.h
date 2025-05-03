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
    sendCmd(ST7789_MADCTL);  sendData(0x70); // RGB order + row/col swap
    sendCmd(ST7789_DISPON);  delay(150);
  }

  void fill(uint16_t color) {
    setAddrWindow(0, 0, WIDTH - 1, HEIGHT - 1);
    sendCmd(ST7789_RAMWR);
    digitalWrite(TFT_DC, HIGH);
    digitalWrite(TFT_CS, LOW);
    for (uint32_t i = 0; i < WIDTH * HEIGHT; ++i) {
      SPI.write16(color);
    }
    digitalWrite(TFT_CS, HIGH);
  }

  void drawPixel(int x, int y, uint16_t color) {
    if (x < 0 || y < 0 || x >= WIDTH || y >= HEIGHT) return;
    setAddrWindow(x, y, x, y);
    sendCmd(ST7789_RAMWR);
    sendData16(color);
  }

  // RGB565 helper
  static uint16_t rgb(uint8_t r, uint8_t g, uint8_t b) {
    return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3);
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
    sendCmd(ST7789_CASET);
    sendData16(x0);
    sendData16(x1);
    sendCmd(ST7789_RASET);
    sendData16(y0);
    sendData16(y1);
  }
};