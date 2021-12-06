#include <avr/io.h>

#define TIMER_1_A_OUT 5
#define TIMER_3_A_OUT 6

#define F_CPU 16000000UL

#define TOP 65535

void simple_start_timers(void)
{
    setup_timer_1();
    setup_timer_3();
    set_speed_timer_1(255);
    set_speed_timer_3(1);
}

void setup_timer_1(void)
{
    TCCR1A = 0;
    TCCR1B = 0;
    TCCR1C = 0;
    DDRB |= (1 << TIMER_1_A_OUT);                       // set port output
    TCCR1A |= (1 << COM1A1) | (1 << COM1A0);            // set when counting up, clear when counting down
    TCCR1B |= (1 << WGM13);                             // PWM, Phase and Frequency Correct, TOP at ICR1
    // TIMSK1 |= (1 << TOIE1);                             // interrupt when BOTTOM (usefull for counting steps)
}

void setup_timer_3(void)
{
    TCCR3A = 0;
    TCCR3B = 0;
    TCCR3C = 0;
    DDRC |= (1 << TIMER_3_A_OUT);                       // set port output
    TCCR3A |= (1 << COM3A1) | (1 << COM3A0);            // set when counting up, clear when counting down
    TCCR3B |= (1 << WGM33);                             // PWM, Phase and Frequency Correct, TOP at ICR3
    // TIMSK3 |= (1 << TOIE3);                             // interrupt when BOTTOM (usefull for counting steps)
}

void set_speed_timer_1(uint8_t u)
{
    
    if (u == 0)  // in case we want to stop the motors
    {
        TCCR1B = 0;  // stop timer
        TCCR1B |= (1 << WGM13);                             // PWM, Phase and Frequency Correct, TOP at ICR1
    }
    else
    {
        TCCR1B |= (0 << CS12) | (0 << CS11) | (1 << CS10);     // prescaler = 1
        ICR1 = get_count(u);                                   // set top value timer
        OCR1A = ICR1 / 2;                                      // set duty cycle always 50%
    }
    
}

void set_speed_timer_3(uint8_t u)
{
    if (u == 0)  // in case we want to stop the motors
    {
        TCCR3B = 0;  // stop timer
        TCCR3B |= (1 << WGM13);                             // PWM, Phase and Frequency Correct, TOP at ICR1
    }
    else
    {
        TCCR3B |= (0 << CS32) | (0 << CS31) | (1 << CS30);     // prescaler = 1
        ICR3 = get_count(u);                                   // set top value timer
        OCR3A = ICR3 / 2;                                      // set duty cycle always 50%
    }
}

uint16_t get_count(uint8_t u)
{
    uint16_t counts[256] = {
                0, 65535, 46516, 36052, 29432, 24866, 21526, 18977, 16968, 15344, 14003, 12878, 11920, 11095, 10376,  9745,
             9187,  8689,  8242,  7839,  7473,  7140,  6836,  6556,  6298,  6060,  5839,  5634,  5443,  5264,  5097,  4939,
             4792,  4653,  4521,  4397,  4280,  4168,  4063,  3962,  3867,  3776,  3689,  3606,  3526,  3450,  3378,  3308,
             3241,  3177,  3115,  3056,  2998,  2943,  2890,  2839,  2790,  2742,  2696,  2651,  2608,  2566,  2526,  2487,
             2449,  2412,  2376,  2341,  2307,  2275,  2243,  2212,  2182,  2152,  2124,  2096,  2069,  2043,  2017,  1992,
             1967,  1944,  1920,  1898,  1875,  1854,  1832,  1812,  1791,  1772,  1752,  1733,  1715,  1697,  1679,  1661,
             1644,  1628,  1611,  1595,  1579,  1564,  1549,  1534,  1520,  1505,  1491,  1477,  1464,  1451,  1438,  1425,
             1412,  1400,  1388,  1376,  1364,  1353,  1341,  1330,  1319,  1308,  1298,  1287,  1277,  1267,  1257,  1247,
             1238,  1228,  1219,  1210,  1201,  1192,  1183,  1174,  1166,  1157,  1149,  1141,  1133,  1125,  1117,  1109,
             1101,  1094,  1087,  1079,  1072,  1065,  1058,  1051,  1044,  1037,  1031,  1024,  1017,  1011,  1005,   998,
              992,   986,   980,   974,   968,   962,   957,   951,   945,   940,   934,   929,   924,   918,   913,   908,
              903,   898,   893,   888,   883,   878,   873,   868,   864,   859,   855,   850,   846,   841,   837,   832,
              828,   824,   820,   815,   811,   807,   803,   799,   795,   791,   787,   783,   780,   776,   772,   768,
              765,   761,   758,   754,   750,   747,   743,   740,   737,   733,   730,   727,   723,   720,   717,   714,
              710,   707,   704,   701,   698,   695,   692,   689,   686,   683,   680,   677,   675,   672,   669,   666,
              663,   661,   658,   655,   653,   650,   647,   645,   642,   639,   637,   634,   632,   629,   627,   625
    };
    return counts[u];
}

void show_timerA(void)
{
  Serial.print("TCCR1A: ");
  Serial.print(TCCR1A);
  Serial.print(", TCCR1B: ");
  Serial.print(TCCR1B);
  Serial.print(", TCCR1C: ");
  Serial.print(TCCR1C);
  Serial.print(", TIMSK1: ");
  Serial.print(TIMSK1);
  Serial.print(", OCR1A: ");
  Serial.print(OCR1A);
  Serial.print(", ICR1: ");
  Serial.print(ICR1);
  Serial.println();
}
