#include <avr/interrupt.h>
#include <stdint.h>
#include <avr/io.h>

#define UP   1
#define DOWN 2

#define BASE      0
#define VEL_A     1
#define VEL_B     2
#define CALIBRATE 3
#define SLEEP     4
#define CENTER    5

#define NOT_READY 0
#define READY     1

#define CENTER_SPEED 255

#define NONE_LIMIT   0
#define TOP_LIMIT    1
#define BOTTOM_LIMIT 2
#define LEFT_LIMIT   3
#define RIGHT_LIMIT  4

#define CALIBRATE_NONE  0
#define CALIBRATE_BETA  1
#define RETURN_BETA     2
#define CALIBRATE_ALPHA 3
#define RETURN_ALPHA    4

#define CALIBRATE_SPEED 20
#define RETURN_SPEED    255

#define POS_TO_ORIGIN_B -1600
#define POS_TO_ORIGIN_A  1600

#define LEFT_DIR  0
#define RIGHT_DIR 1
#define UP_DIR    1
#define DOWN_DIR  0

#define PIN_SWITCH_B 3
#define PIN_SWITCH_A 7

#define LIMITS_A 1600
#define LIMITS_B 1600

 
char recieved;
volatile int state              = BASE;
volatile int calibrate_state    = CALIBRATE_NONE;
volatile int alpha_state        = NONE_LIMIT;
volatile int beta_state         = NONE_LIMIT;
volatile int alpha_center_state = NOT_READY;
volatile int beta_center_state  = NOT_READY;

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
    digitalWrite(13, LOW);
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
            else if (bitRead(recieved, 5))
            {
                state = SLEEP;
                sleepA(1);
                sleepB(1);
            }
            else if (bitRead(recieved, 3))
            {
                state = CENTER;
                speedA(0);
                speedB(0);
                alpha_center_state = NOT_READY;
                beta_center_state = NOT_READY;
                if (posA == 0)
                {
                    speedA(0);
                    alpha_center_state = READY;
                }
                else
                {
                    if (posA > 0)
                    {
                        dir_a = dirA(DOWN_DIR);
                    }
                    else
                    {
                        dir_a = dirA(UP_DIR);
                    }
                    speedA(CENTER_SPEED);
                }
                if (posB == 0)
                {
                    speedB(0);
                    beta_center_state = READY;
                }
                else
                {
                    if (posB > 0)
                    {
                        dir_b = dirB(LEFT_DIR);
                    }
                    else
                    {
                        dir_b = dirB(RIGHT_DIR);
                    }
                    speedB(CENTER_SPEED);
                }
                if (alpha_center_state == READY && beta_center_state == READY)
                {
                    state = BASE;
                    speedA(0);
                    speedB(0);
                    beta_state = NONE_LIMIT;
                    alpha_state = NONE_LIMIT;
                }
            }
            break;

        case VEL_A:
            if (alpha_state == TOP_LIMIT)
            {
                if (next_dir_a == DOWN_DIR)
                {
                    speedA(0);
                    dir_a = dirA(next_dir_a);
                    speedA(recieved);
                    alpha_state = NONE_LIMIT;
                }
                else if (next_dir_a == UP_DIR)
                {
                    speedA(0);
                    alpha_state = TOP_LIMIT;
                }
                
            }
            if (alpha_state == BOTTOM_LIMIT)
            {
                if (next_dir_a == UP_DIR)
                {
                    speedA(0);
                    dir_a = dirA(next_dir_a);
                    speedA(recieved);
                    alpha_state = NONE_LIMIT;
                }
                else if (next_dir_a == DOWN_DIR)
                {
                    speedA(0);
                    alpha_state = BOTTOM_LIMIT;
                }
                    
            }
            if (alpha_state == NONE_LIMIT)
            {
                speedA(recieved);
                dir_a = dirA(next_dir_a);
            }
            state = VEL_B;
            break;

        case VEL_B:
            if (beta_state == RIGHT_LIMIT)
            {

                if (next_dir_b == LEFT_DIR)
                {
                    speedB(0);
                    dir_b = dirB(next_dir_b);
                    speedB(recieved);
                    beta_state = NONE_LIMIT;
                }
                else if (next_dir_b == RIGHT_DIR)
                {
                    speedB(0);
                    beta_state = RIGHT_LIMIT;
                }
                
            }
            if (beta_state == LEFT_LIMIT)
            {
               
                if (next_dir_b == RIGHT_DIR)
                {
                    speedB(0);
                    dir_b = dirB(next_dir_b);
                    speedB(recieved);
                    beta_state = NONE_LIMIT;
                }
                else if (next_dir_b == LEFT_DIR)
                {
                    speedB(0);
                    beta_state = LEFT_LIMIT;
                }
                    
            }
            if (beta_state == NONE_LIMIT)
            {
                speedB(recieved);
                dir_b = dirB(next_dir_b);
            }
            
            state = BASE;
            break;

        case CALIBRATE:
            break;

        case SLEEP:
            if (bitRead(recieved, 4))
            {
                sleepA(0);
                sleepB(0);
                state = BASE;
            }
            else if (bitRead(recieved, 6))
            {
                state = CALIBRATE;
                calibrate_state = CALIBRATE_BETA;
                sleepA(1);
                speedA(0);
                sleepB(0);
                speedB(CALIBRATE_SPEED);
                dir_b = dirB(LEFT_DIR);
            }
            break;
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
        if (state == BASE)
        {
            if (posA >= LIMITS_A)
            {
                speedA(0);
                alpha_state = TOP_LIMIT;
                posA = LIMITS_A;

            }
            if (posA <= -LIMITS_A)
            {
                speedA(0);
                alpha_state = BOTTOM_LIMIT;
                posA = -LIMITS_A;

            }
        }
        if (state == CENTER)
        {
            if (posA == 0)
            {
                speedA(0);
                alpha_center_state = READY;
                if (beta_center_state == READY && alpha_center_state == READY)
                {
                    state = BASE;
                    beta_state = NONE_LIMIT;
                    alpha_state = NONE_LIMIT;
                }
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
        if (state == BASE)
        {
            if (posB >= LIMITS_B)
            {
                speedB(0);
                beta_state = RIGHT_LIMIT;
                posB = LIMITS_B;

            }
            if (posB <= -LIMITS_B)
            {
                speedB(0);
                beta_state = LEFT_LIMIT;
                posB = -LIMITS_B;
            }
        }
        if (state == CENTER)
        {
            if (posB == 0)
            {
                speedB(0);
                beta_center_state = READY;
                if (alpha_center_state == READY && beta_center_state == READY)
                {
                    state = BASE;
                    beta_state = NONE_LIMIT;
                    alpha_state = NONE_LIMIT;
                }
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
