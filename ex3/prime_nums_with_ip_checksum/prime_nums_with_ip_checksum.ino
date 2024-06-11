#include <Arduino.h>

void loop2();
bool isPrime(int num);
unsigned long induceErrors(unsigned long data, float ber, float probabilityBurst, float probabilityIsolated);
unsigned long induceBurstErrors(unsigned long data, int burstLength);
unsigned long induceIsolatedErrors(unsigned long data, float ber);
unsigned int ipChecksum(byte *addr, int count);

// Global variables
unsigned long number = 2; // Start with the first prime number
bool inducedErrors = true; // Flag to indicate if errors should be induced
float probabilityBurst = 25.0; // Probability of inducing burst errors (in percentage)
float probabilityIsolated = 75.0; // Probability of inducing isolated errors (in percentage)
float ber = 0.00; // Bit Error Rate for isolated errors
int burstLength = 5; // Length of burst errors
unsigned long primesUntil = 1000000; // Generate primes until this number then stop

void setup() {
  Serial.begin(9600); // Start serial communication at 9600 baud rate

  randomSeed(analogRead(0)); // Initialize the random number generator with a somewhat random seed from an analog pin
}

void loop() {
  // Only process prime numbers
  if (isPrime(number)) {
    // First, calculate the IP checksum for the pristine data
    unsigned int checksum = ipChecksum((byte*)&number, sizeof(number));

    // Then induce errors in the data based on the probabilities and BER
    unsigned long finalData = number;
    if (inducedErrors) {
      finalData = induceErrors(number, ber, probabilityBurst, probabilityIsolated);
    }
    // Print the data with errors and checksum to the serial monitor
    Serial.print(finalData);
    Serial.print(","); // Delimiter between data and checksum
    Serial.println(checksum);
    delay(1000); // Wait for 1 second before processing the next number
  }
  // Increment the number to check the next integer
  number++; 

  // If the number exceeds the limit, reset it to 2 to start over
  if(number > primesUntil) {
    number = 2;
  }
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

// Function to induce errors based on probabilities
unsigned long induceErrors(unsigned long data, float ber, float probabilityBurst, float probabilityIsolated) {
  float totalProbability = probabilityBurst + probabilityIsolated;
  float randomValue = random(0, 100);

  if (randomValue < (probabilityBurst / totalProbability) * 100) {
    // Induce burst errors
    return induceBurstErrors(data, burstLength);
  } else {
    // Induce isolated errors
    return induceIsolatedErrors(data, ber);
  }
}

// Function to induce isolated errors in the data
unsigned long induceIsolatedErrors(unsigned long data, float ber) {
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

// Function to induce burst errors in the data
unsigned long induceBurstErrors(unsigned long data, int burstLength) {
  unsigned long errorMask = 0;
  int startBit = random(0, 32 - burstLength); // Randomly select start bit for burst
  // Create the burst error mask
  for (int i = startBit; i < startBit + burstLength; i++) {
    errorMask |= (1UL << i);
  }
  // Apply the burst error mask to the data
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
