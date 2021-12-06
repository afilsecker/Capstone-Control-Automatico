#include <avr/interrupt.h>
#include <stdint.h>
#include <avr/io.h>

#define BASE  0
#define VEL_A 1
#define VEL_B 2

char recieved;
int  state = BASE;

void setup() {
    // put your setup code here, to run once:
    set_motores();
    Serial1.begin(115200);
}

void loop() {
    // put your main code here, to run repeatedly:
}

void serialEvent1()
{
    recieved = Serial1.read();
    switch(state)
    {
        case BASE:
            if (bitRead(recieved, 7))
            {
                state = VEL_A;
                dirA(bitRead(recieved, 0));
                dirB(bitRead(recieved, 1));
            }
            break;
        case VEL_A:
            speedA(recieved);
            state = VEL_B;
            break;
        case VEL_B:
            speedB(recieved);
            state = BASE;
    }
    
}
