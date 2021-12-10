#include <avr/interrupt.h>
#include <stdint.h>
#include <avr/io.h>

#define UP   1
#define DOWN 2

#define BASE      0
#define VEL_A     1
#define VEL_B     2
#define CALIBRATE 3

#define CALIBRATE_NONE  0
#define CALIBRATE_BETA  1
#define RETURN_BETA     2
#define CALIBRATE_ALPHA 3
#define RETURN_ALPHA    4

#define CALIBRATE_SPEED 20
#define RETURN_SPEED    255

#define POS_TO_ORIGIN_B -6400
#define POS_TO_ORIGIN_A 6400

#define LEFT_DIR  0
#define RIGHT_DIR 1
#define UP_DIR    1
#define DOWN_DIR  0

#define PIN_SWITCH_B 3
#define PIN_SWITCH_A 7

 
char recieved;
volatile int  state = BASE;
volatile int  calibrate_state = CALIBRATE_NONE;

volatile int countingA = UP;
volatile int countingB = UP;

volatile int posA = 0;
volatile int posB = 0;

volatile int dir_a;
volatile int dir_b;

volatile int next_dir_a;
volatile int next_dir_b;

void setup() {
    // put your setup code here, to run once:
    set_motores();
    pinMode(PIN_SWITCH_A, INPUT_PULLUP);
    pinMode(PIN_SWITCH_B, INPUT);
    pinMode(13, OUTPUT);
    Serial1.begin(115200);
    sei();
    
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
                next_dir_a = bitRead(recieved, 0);
                next_dir_b = bitRead(recieved, 1);
            }
            else if (bitRead(recieved, 6))
            {
                state = CALIBRATE;
                calibrate_state = CALIBRATE_BETA;
                sleepA(1);
                speedA(0);
                speedB(CALIBRATE_SPEED);
                dir_b = dirB(LEFT_DIR);
            }
            break;

        case VEL_A:
            speedA(recieved);
            dir_a = dirA(next_dir_a);
            state = VEL_B;
            break;

        case VEL_B:
            speedB(recieved);
            dir_b = dirB(next_dir_b);
            state = BASE;

        case CALIBRATE:
            break;
    }
}


ISR(TIMER3_COMPA_vect)
{
    if (countingB == UP)
    {
        countingB = DOWN;
        posB += dir_b * 2 - 1;
        if (state == CALIBRATE && calibrate_state == RETURN_BETA)
        {
            if (posB == 0)
            {
                calibrate_state = CALIBRATE_ALPHA;
                speedB(0);
                sleepA(0);
                speedA(CALIBRATE_SPEED);
                dir_a = dirA(UP_DIR);
            }
        }
    }
}

ISR(TIMER3_OVF_vect)
{
    countingB = UP;
    if (state == CALIBRATE && calibrate_state == CALIBRATE_BETA)
    {
        if (!digitalRead(PIN_SWITCH_B))
        {
            speedB(RETURN_SPEED);
            dir_b = dirB(RIGHT_DIR);
            calibrate_state = RETURN_BETA;
            posB = POS_TO_ORIGIN_B;
        }
    }
}

ISR(TIMER1_COMPA_vect)
{
    if (countingA == UP)
    {
        countingA = DOWN;
        posA += dir_a * 2 - 1;
        if (state == CALIBRATE && calibrate_state == RETURN_ALPHA)
        {
            if (posA == 0)
            {
                calibrate_state = CALIBRATE_NONE;
                speedA(0);
                state = BASE;
            }
        }
    }
}

ISR(TIMER1_OVF_vect)
{
    countingA = UP;
    if (state == CALIBRATE && calibrate_state == CALIBRATE_ALPHA)
    {
        if (!digitalRead(PIN_SWITCH_A))
        {
            speedA(RETURN_SPEED);
            dir_a = dirA(DOWN_DIR);
            calibrate_state = RETURN_ALPHA;
            posA = POS_TO_ORIGIN_A;
        }
    }
    
}
