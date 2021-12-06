int pinDirA   = 8;
int pinSleepA = 10;
int pinDirB   = 4;
int pinSleepB = 6;

int posA = 0;
int posB = 0;

void set_motores(void)
{
    pinMode(pinDirA, OUTPUT);
    pinMode(pinSleepA, OUTPUT);
    pinMode(pinDirB, OUTPUT);
    pinMode(pinSleepB, OUTPUT);

    sleepA(0);
    sleepB(0);

    setup_timer_1();
    setup_timer_3();

    speedA(0);
    speedB(0);
}

void speedA(uint8_t vel)
{
    set_speed_timer_1(vel);
}

void speedB(uint8_t vel)
{
    set_speed_timer_3(vel);
}

void sleepA(bool state)
{
    digitalWrite(pinSleepA, 1 - state);
}

void sleepB(bool state)
{
    digitalWrite(pinSleepB, 1 - state);
}

void dirA(bool dir)
{
    digitalWrite(pinDirA, dir);
}

void dirB(bool dir)
{
    digitalWrite(pinDirB, dir);
}



 
