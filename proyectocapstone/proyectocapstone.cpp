#include "proyectocapstone.h"

//Gracias por el aporte a este código de https://www.instructables.com/Arduino-Timer-Interrupts/; https://roboticsbackend.com/arduino-create-library/  https://www.luisllamas.es/cadenas-de-texto-puerto-serie-arduino/ https://hetpro-store.com/TUTORIALES/arduino-atoi/, demás a los vídeos de Paul McWorther y Sparkfun
//Con estos códigos aprendí a progamar esto 
//Hecho por Martín de la Barra. Para uso privado sin usos comerciales. Sen guarda de todos los derechos y beneficios de esta librería




//velocidad=1/(4*10^-6*OCR1A), la velocidad mínima, por los timers, son de 995 steps/seg, y la máxima de 10400 steps/seg
void velocidadmotor(int vel, int motor){
  //motor 1
  if(motor==1 and vel>0){PORTB |= B00000001;OCR1A=int(25000/vel);};
  if(motor==1 and vel<0){PORTB &= B11111110;OCR1A=int(abs(25000/vel));};
  if(motor==1 and vel==0){OCR1A=65000;}
  

  //motor 2
  if(motor==2 and vel>0){PORTB |= B00010000; OCR0A=int(25000/vel);};
  if(motor==2 and vel<0){PORTB &= B11101111; OCR0A=int(25000/(abs(vel)));};
  if(motor==2 and vel==0){OCR0A=255;};
  }

void moverdistancia(int velocidad, int distancia,int motor){
 velocidadmotor(velocidad,motor);
 OCR0A= int(abs(velocidad/(distancia*8))); 
}


void configuracionboton1(){
  //Caída con flanco de bajada
  EICRA |= (1 << ISC01);
  EICRA &= ~ (1 << ISC00);
  EIMSK  |= (1 << INT0); //Habilita interrupción int0
}

void configuracionboton2(){
  //Caída con flanco de bajada
  EICRA |= (1 << ISC01);
  EICRA &= ~ (1 << ISC00);
  EIMSK  |= (1 << INT1); //Habilita interrupción int1
}




void configurarTimer1(){
    TCCR1A = 0; //reiniciar registro timer
    TCCR1B = 0;
    //OCR1A = 15624/64;  // = (target time / timer resolution) - 1 or 1 / 6.4e-5 - 1 = 15624
    //OCR1A = 24;  // divide by two >>EDIT added this line<<
    TCCR1B |= (1 << WGM12);// CTC mode on
    //TCCR1B |= (1 << CS10);// Set CS11 8 prescaler:
    TCCR1B |= (1 << CS11);
    TIMSK1 |= (1 << OCIE1A);// timer compare intrupt enable
    //sei();
}

void configurarTimer0(){
    //set timer0 interrupt at 2kHz
    TCCR0A = 0;// set entire TCCR2A register to 0
    TCCR0B = 0;// same for TCCR2B
    
    // set compare match register for 2khz increments
    //OCR0A = 24;// = (16*10^6) / (2000*256) - 1 (must be <256)
    // turn on CTC mode
    TCCR0A |= (1 << WGM01);
    // Set CS01  bits for 8 prescaler
    TCCR0B |= (1 << CS01); 
    //TCCR0B |= (1 << CS00); 
    
    //(1 << CS00)|  
    // enable timer compare interrupt
    TIMSK0 |= (1 << OCIE0A);
    //sei();
}

//void configurarTimer2(){
  //TCCR2A = 0;// set entire TCCR2A register to 0
  //TCCR2B = 0;// same for TCCR2B
  // set compare match register for 8khz increments
  //OCR2A = 249;// = (16*10^6) / (8000*8) - 1 (must be <256)
  // turn on CTC mode
  //TCCR2A |= (1 << WGM21);
  //TCCR2A |= (1 << WGM20);
  // Set CS21 bit for 8 prescaler
  //TCCR2B |= (1 << CS21);   
   //enable timer compare interrupt
  //TIMSK2 |= (1 << OCIE2A);
//}
