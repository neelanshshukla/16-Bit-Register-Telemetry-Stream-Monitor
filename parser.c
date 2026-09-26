#include <stdio.h>
#include <stdlib.h>

int main() {
    // 1. Open the raw input text file
    FILE *file = fopen("network_traffic.txt", "r");
    if (file == NULL) {
        printf("Error: Cannot open network_traffic.txt\n");
        return 1;
    }

    // 2. Open the JavaScript file to write our data variable
    FILE *js_file = fopen("data.js", "w");
    if (js_file == NULL) {
        printf("Error: Cannot create data.js\n");
        fclose(file);
        return 1;
    }

    // Start the JavaScript array syntax
    fprintf(js_file, "const hardwareTelemetryData = [\n");

    unsigned int raw_packet;
    int is_first = 1;

    // 3. Read packets line by line until the end of the file
    while (fscanf(file, "%u", &raw_packet) != EOF) {
        
        // BITWISE EXTRACTORS (Your core formulas)
        unsigned int device_id = (raw_packet >> 12) & 0x0F;
        unsigned int priority = (raw_packet >> 8) & 0x0F;
        unsigned int payload = raw_packet & 0xFF;

        // If it's not the first item, add a comma to separate objects
        if (!is_first) {
            fprintf(js_file, ",\n");
        }
        is_first = 0;

        // Write a clean, simple object structure line
        fprintf(js_file, "  { \"device_id\": %u, \"priority\": %u, \"payload\": %u }", device_id, priority, payload);
    }

    // Close the JavaScript array syntax
    fprintf(js_file, "\n];\n");

    fclose(file);
    fclose(js_file);
    printf("Successfully updated data.js!\n");
    return 0;
}
