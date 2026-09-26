// Target UI components in the HTML DOM structure
const tableBody = document.getElementById('data-table-body');
const alertsContainer = document.getElementById('alerts-container');
const totalPacketsMetric = document.getElementById('total-packets');
const faultCountMetric = document.getElementById('fault-count');

// 1. AUTOMATED HARDWARE PACKET GENERATOR (Simulating register streams inside the browser)
function generateMockHardwareTraffic() {
    let rawPacketsArray = [];
    
    for (let i = 0; i < 50; i++) {
        // Generate values matching strict bit constraints
        let deviceId = Math.floor(Math.random() * 16);  // 4-bit range: 0 to 15
        let priority = Math.floor(Math.random() * 16);  // 4-bit range: 0 to 15
        let payload = Math.floor(Math.random() * 256);  // 8-bit range: 0 to 255

        // Bitwise packing identical to your original C/Python logic
        // Shifting Device ID left by 12 bits, Priority left by 8 bits, and adding Payload
        let packedPacket = (deviceId << 12) | (priority << 8) | payload;
        rawPacketsArray.push(packedPacket);
    }
    return rawPacketsArray;
}

// 2. THE EMBEDDED BITWISE PARSING ENGINE
function runWebTelemetryPipeline() {
    // Clear out old layout entries before parsing new data stream
    tableBody.innerHTML = '';
    alertsContainer.innerHTML = '';
    
    let simulatedStream = generateMockHardwareTraffic();
    let totalFaults = 0;

    // Update global top total numbers counter card
    totalPacketsMetric.innerText = simulatedStream.length;

    // Loop directly over the simulated data stream
    simulatedStream.forEach(rawPacket => {
        
        // YOUR CORE BITWISE EXTRACTION FORMULAS (Running client-side natively!)
        let deviceId = (rawPacket >> 12) & 0x0F;
        let priority = (rawPacket >> 8) & 0x0F;
        let payload = rawPacket & 0xFF;

        // Determine status text configurations based on threshold limits
        let statusText = "NOMINAL";
        let statusClass = "text-success";

        if (priority === 15) {
            statusText = "CRITICAL";
            statusClass = "text-danger";
        }

        // Generate physical table entry element structure row string
        let rowHTML = `
            <tr>
                <td>Device ${deviceId.toString().padStart(2, '0')}</td>
                <td>${priority}</td>
                <td>${payload}</td>
                <td><span class="${statusClass}">${statusText}</span></td>
            </tr>
        `;
        tableBody.innerHTML += rowHTML;

        // If critical priority threshold is breached, generate alert box banner
        if (priority === 15) {
            totalFaults++;
            let alertHTML = `
                <div class="alert-box danger-alert">
                    ALERT: Critical status detected on Device ${deviceId} (Payload: ${payload})
                </div>
            `;
            alertsContainer.innerHTML += alertHTML;
        }
    });

    // Update active fault counter card number
    faultCountMetric.innerText = totalFaults;

    // Default cleanup display state rules mapping if faults check clean
    if (totalFaults === 0) {
        alertsContainer.innerHTML = `<div class="nominal-msg">All systems operating within normal parameters.</div>`;
    }
}

// Automatically trigger a stream decode right on window frame startup allocation
runWebTelemetryPipeline();
setInterval(runWebTelemetryPipeline, 2000);
