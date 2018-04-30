
int start_pin = 2;
int end_pin = 15;

String input;
double period;
double duty_period;

void setup() {
    Serial.begin(9600);
    for (int i = start_pin; i <= end_pin; i++){
        pinMode(i, OUTPUT);
        digitalWrite(i, LOW);
    }
}

void loop() {
    if (Serial.available() > 0) {
         input = Serial.readString();
         int flag = input.toInt();
         if (flag == 0) {
            double freq = input.substring(1).toDouble();
            double duty = input.substring(input.indexOf('d') + 1).toDouble();
            period = (1.0 / freq) * 1000.0;
            duty_period = period * duty;
         } else {
           while (Serial.available() == 0) {
            for (int i = 13; i >= 0; i--) {
              if (bitRead(flag, i) == 1) {
                  digitalWrite(i + start_pin, HIGH);
          
               } else {
                  digitalWrite(i + start_pin, LOW);
               }
             }
             delay(duty_period);
             for (int i = start_pin; i <= end_pin; i++){
                  digitalWrite(i, LOW);
             } 
             delay(period - duty_period);
           }
         }
    }
}
