import random
import time

print("====SILICON TRAFFIC GENERATOR ONLINE ===")
print("Generating mock hardware stream data. . . . . . ")

# Open the file in write mode ('w') to refresh the data stream
with open("network_traffic.txt" , "w") as file:
    # Generate 50 simulated network packets
    for _ in range(50):
        device_id = random.randint(0, 15)    #Fits in 4Bits (0-15)
        priority = random.randint(0, 15)       #Fits in 4 bits (0 -15)
        payload = random.randint(0, 255)    #Fits in 8 Bits (0 - 255)

        #BITWISE PACKING:  Shift bits into their designated slots
        #Device ID: gotes to the top 4 bits, Priority to the middle 4, Payload to the bottom 8
        packet = (device_id  << 12)  | (priority  << 8)  | (payload)

        # Write the combined 16-Bit integer to the text stream file
        file.write(f"{packet}\n")

        print("Successfully writtten 50 packed packets to network_traffic.txt!")