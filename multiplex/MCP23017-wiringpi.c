#include <stdio.h>
#include <wiringPi.h>
#include <mcp23017.h>

#define NUMLEDS     9
#define PINBASE     65      // or 100?
#define INPUTPIN    (PINBASE + 15)

int main (void)
{
    int i, bit;

    wiringPiSetup();
    mcp23017Setup(PINBASE, 0x20);

    printf("Raspberry Pi - MCP23017 Test\n");

    for (i = 0; i < NUMLEDS; ++i)
        pinMode(PINBASE + i, OUTPUT);
    pinMode(INPUTPIN, INPUT);

    //pullUpDnControl (PINBASE + 15, PUD_UP);

    i = 0;
    for (;;)
    {
        for (bit = 0; bit < NUMLEDS; ++bit)
            digitalWrite(PINBASE + bit, (bit == i ? 1 : 0));
        int val = digitalRead(INPUTPIN);
        printf("i = %d, read %d\n", i, val);

        i += 1;
        if (i >= NUMLEDS)
            i = 0;

        delay(500);
    }
    return 0;
}
