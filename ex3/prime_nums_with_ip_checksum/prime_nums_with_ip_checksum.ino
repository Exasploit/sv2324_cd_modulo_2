#include <Arduino.h>

bool isPrime(int num);
unsigned long induceErrors(unsigned long data, float ber);
unsigned int ipChecksum(byte *addr, int count);

unsigned long number = 2; // Start with the first prime number
float ber = 0.01; // Bit Error Rate set to 2%

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate
  randomSeed(analogRead(0)); // Initialize the random number generator with a somewhat random seed from an analog pin
}

void loop() {
  // Only process prime numbers
  if (isPrime(number)) {
    // First, calculate the IP checksum for the pristine data
    unsigned int checksum = ipChecksum((byte*)&number, sizeof(number));
    // Then induce errors in the data based on the BER, if simulating error conditions
    unsigned long dataWithError = induceErrors(number, ber);
    // Print the data with errors and checksum to the serial monitor
    Serial.print(dataWithError);
    Serial.print(","); // Delimiter between data and checksum
    Serial.println(checksum);
    delay(1000); // Wait for 1 second before processing the next number
  }
  number++; // Increment the number to check the next integer
}

// Function to check if a number is prime
bool isPrime(int num) {
  if (num <= 1) return false; // handle small numbers directly
  if (num % 2 == 0) return num == 2; // handle multiples of 2
  for (int i = 3; i * i <= num; i += 2) {
    if (num % i == 0) {
      return false;
    }
  }
  return true;
}

// Function to induce errors in the data
unsigned long induceErrors(unsigned long data, float ber) {
  unsigned long errorMask = 0;
  // Loop through each bit of the data
  for (int i = 0; i < 32; i++) {
    // Randomly decide to flip each bit based on the BER
    if (random(10000) < ber * 10000) {
      errorMask |= (1UL << i); // Set the bit in the error mask
    }
  }
  // Apply the error mask to the data, flipping bits where the error mask has 1s
  return data ^ errorMask;
}

// Function to calculate IP checksum for a block of data
unsigned int ipChecksum(byte *addr, int count) {
  unsigned long sum = 0;
  // Main summing loop, adding 2 bytes at a time
  while (count > 1) {
    sum += *(unsigned short*)addr; // Sum 16-bit words
    addr += 2; // Move pointer by 2 bytes
    count -= 2; // Decrease count by 2
  }
  // If there's a leftover byte, add it to the sum
  if (count > 0) {
    sum += *addr; // Add the remaining byte
  }
  // Fold 32-bit sum to 16 bits: add upper 16 to lower 16 bits
  while (sum >> 16) {
    sum = (sum & 0xFFFF) + (sum >> 16);
  }
  // One's complement of the sum for the checksum
  return ~sum;
}
