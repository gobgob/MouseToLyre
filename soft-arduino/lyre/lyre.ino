//Adapted from https://code.google.com/p/tinkerit/wiki/SerialToDmx

#include <DmxSimple.h>

// After installing, switch to Serial Monitor and set the baud rate to 9600.
//
// Type commands in the box and hit 'Send'.
//
// <number>c : Select a DMX channel
// <number>v : Set DMX channel to new value

void setup() {
	Serial.begin(9600);
}

int value = 0;
int channel;

void loop()
{
	int c;

	while(!Serial.available())
	{
		//Do nothing and wait.
	}
	c = Serial.read();
	if ((c>='0') && (c<='9'))
	{
		value = 10*value + c - '0';
	} else {
		if (c=='c')
		{
			channel = value;
		}
		else if (c=='w')
		{
			DmxSimple.write(channel, value);
		}
		else if (c=='?')
		{
			Serial.print("I am the One");
		}
		value = 0;
	}
}
