#include "proyectocapstone.h"
// Parámetros control x


String idt;
String velocidadsx;
char vectorvelx[8];
int velocidadx;

//Parámetros control y




void setup() {
  // put your setup code here, to run once:
  //Configuración pines
   DDRB |= B00111011;  // set pin8,9,11,12 to output 
   DDRD &= ~B00001010;  // set pin 2 Y 4 to input
   PORTD |= B00001010;
   configurarTimer1();
   configurarTimer0();
  Serial.begin(115200);

//while (Serial.available() ==0){}
//idt=Serial.readStringUntil('\n');

velocidadmotor(0,1);
velocidadmotor(0,2);
//if (idt.substring(0,1)=="A"){velocidadsx=idt.substring(1,idt.length());velocidadsx.toCharArray(vectorvelx,8);velocidadx=atoi(vectorvelx);Serial.println(velocidadx);}
//if (idt.substring(0,1)=="B"){velocidadsx=idt.substring(1,idt.length());velocidadsx.toCharArray(vectorvelx,8);velocidadx=atoi(vectorvelx);Serial.println(velocidadx);}







}

void loop() {
  
  // put your main code here, to run repeatedly:
  while (Serial.available() ==0){}
  idt=Serial.readStringUntil('\n');
  
  if (idt.substring(0,1)=="A"){
    velocidadsx=idt.substring(1,idt.length());
    velocidadsx.toCharArray(vectorvelx,8);
    velocidadx=atoi(vectorvelx);
    velocidadmotor(velocidadx,1);
    
   }
  if (idt.substring(0,1)=="B"){
    velocidadsx=idt.substring(1,idt.length());
    velocidadsx.toCharArray(vectorvelx,8);
    velocidadx=atoi(vectorvelx);
    velocidadmotor(velocidadx,2);
    
    
    }
  

 
  
  
    
    
    
  
  

}

ISR(TIMER1_COMPA_vect)
{  
   //toggles bit which affects pin9
  // toggles bit which affects pin9
  if (OCR1A != 65000){PORTB ^= B00000010;}// toggles bit which affects pin9
  if (OCR1A==65000){PORTB |= B00000010;}
  
  //TIMER1_CAPT_vect para caomparar capturas
  //if (velocidadx==0){digitalWrite(11,HIGH);cli();Serial.println("PA");}
  //if (velocidady>0 or velocidadx > 0){
  //contador1=contador1+1;
  //if (contador1==velocidadx){PORTB ^= B00000010;contador1=0;}
  //contador2=contador2+1;
  //if (contador2==velocidady){ PORTB ^= B00001000;contador2=0;}}
  //else {digitalWrite(9, HIGH);}
  //sei();
}
 
    // do something here unaffected by your blinking led
    


 
  //sei();


 
//ISR(TIMER2_COMPA_vect)
//{ 
  //TIMER2_CAPT_vect para caomparar capturas
//  PORTB ^= B00000010;// toggles bit which affects pin9
//  digitalWrite(13,HIGH);
//}

ISR(TIMER0_COMPA_vect){//timer0 interrupt 2kHz toggles pin 8
//generates pulse wave of frequency 2kHz/2 = 1kHz (takes two cycles for full wave- toggle high then toggle low)
  //digitalWrite(13,HIGH);
  if (OCR0A != 255){PORTB ^= B00001000;}// toggles bit which affects pin9
  if (OCR0A==255){PORTB |= B00001000;}

  }

//ISR(TIMER1_COMPA_vect)
//{
  //TIMER1_CAPT_vect para caomparar capturas
  //digitalWrite(13,HIGH);
  //PORTB ^= B00001000;// toggles bit which affects pin9
//}



//ISR(INT0_vect){
  //Lo que tiene que hacer cuando se activa
//  digitalWrite(13,HIGH);
//  moverdistancia(4000,800,1);
//  TIMSK0 |= (1 << OCIE0A);
//  PORTB ^= B00100000;
//}

//ISR(INT1_vect){
  //Lo que tiene que hacer cuando se activa
//  digitalWrite(13,HIGH);
//  moverdistancia(4000,800,2);
//  TIMSK0 |= (1 << OCIE0A);
//  PORTB ^= B00100000;
//}
