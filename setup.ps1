# Saving root folder
$root = $PSScriptRoot

# Install Ollama model
ollama pull qwen3:8b

# Backend Setup
py -3.12 -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
. .\venv\Scripts\Activate.ps1

Set-Location "$root\backend"
pip install -r requirements.txt

# Adding folders that the project needs
Set-Location "$root"
New-Item -ItemType Directory -Path "PowerShellPIDs"
New-Item -ItemType Directory -Path "frontend"

# Frontend Setup
Set-Location "$root\frontend"
@("No", "No") | npm create vite@8.3.0 . -- --template vanilla
npm install

# Create necessary folders and files
New-Item -ItemType Directory -Path "$root\frontend\css"
New-Item -ItemType Directory -Path "$root\frontend\js"

Set-Content -Path "$root\frontend\css\style.css" -Value @'
/* Reset default browser styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Page layout */
body {
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg, #f4f4f4, #e9eef5);
    min-height: 100vh;
    padding: 30px;

    display: flex;
    flex-direction: column;
    align-items: center;
}

/* Input */
#emailInput {
    width: 100%;
    font-size: 16px;
    padding: 12px 14px;
    margin-top: 15px;
    border-radius: 10px;
    border: 1px solid #ccc;
    outline: none;
    background: white;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    resize: none;

    transition: 0.2s ease;
}

#emailInput:focus {
    border-color: #4a90e2;
    box-shadow: 0 0 0 3px rgba(74,144,226,0.15);
}

/* Button */
#sendBtn {
    margin-top: 12px;
    margin-bottom: 30px;

    padding: 12px 18px;
    font-size: 16px;
    cursor: pointer;

    border: none;
    border-radius: 10px;
    background: #4a90e2;
    color: white;

    font-weight: 600;
    transition: 0.2s ease;
}

#sendBtn:hover {
    background: #3b7ccc;
    transform: translateY(-1px);
}

#sendBtn:active {
    transform: translateY(0);
}

/* Disabled state */
#sendBtn:disabled {
    background-color: #999;
    color: #666;
    cursor: not-allowed;
    opacity: 0.6;
}

/* Output */
#output {
    margin-top: 15px;
    padding: 15px;

    background-color: #ffffff;
    border-radius: 12px;
    border: 1px solid #e0e0e0;

    white-space: pre-wrap;
    min-height: 100px;
    width: 100%;

    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
'@

Set-Content -Path "$root\frontend\js\app.js" -Value @'
// Loading configuration from external JSON file
export async function loadConfig(){
    try {
        // Trying to load the configuration JSON file from the backend
        const res = await fetch("http://localhost:8000/config/configJson");
        if (!res.ok) {
            throw new Error("Failed to load JSON file");
        }

        const config = await res.json();
        return config.apiBaseUrl;

    } catch (error) {
        console.error("Error loading config:", error);
        return null;
    }
}

// Function for sending logs to the backend
export async function backendLogSender(message, extra = {extra: "none"}) {
    if (typeof BACKEND_ENDPOINT !== "string") {
    console.warn("Log skipped - invalid backend endpoint");
    return;
    }

    const payload = {
        message: message,
        ...extra,
        url: window.location.href,
        userAgent: navigator.userAgent,
        timestamp: new Date().toISOString()
    }

    try {
        const res = await fetch(BACKEND_ENDPOINT + "/log/js_error", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        });

        if (!res.ok) {
            throw new Error(`HTTP error: ${res.status}`);
        }
        
    } catch (error) {
        console.error("Failed to send log to backend:", error);
    }
}

// backend endpoint variable
let BACKEND_ENDPOINT = null;

// Waiting for web content to load
document.addEventListener("DOMContentLoaded", async () => {
    BACKEND_ENDPOINT = await loadConfig();
    if (!BACKEND_ENDPOINT) {
        console.error("Configuration loading error");
        return;
    }
    
    const EMAIL_REPLY_ENDPOINT = BACKEND_ENDPOINT + "/email/reply";
    
    // Selecting HTML elements
    const emailInput = document.getElementById("emailInput");
    const sendBtn = document.getElementById("sendBtn");
    const output = document.getElementById("output");
    
    if (!emailInput || !sendBtn || !output) {
        console.error("DOM element selection error");
        await backendLogSender("DOM element selection error");
        return;   
    }
    
    // Adding click event listener to the send button
    sendBtn.addEventListener("click", async () => {
        const emailText = emailInput.value;
        
        // Alert for blank email input
        if (!emailText.trim()) {
            output.textContent = "Write an email text first.";
            await backendLogSender("Empty email input", { length: emailText.length });
            return;
        }

        output.textContent = "⏳ Processing…";
        sendBtn.disabled = true;

        // Sending POST request to backend API
        try {
            const response = await fetch(EMAIL_REPLY_ENDPOINT, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email_text: emailText
                })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`)
            }
            
            const data = await response.json().catch(() => { 
                throw new Error("Invalid JSON from server");
            });

            if (
                typeof data !== "object" ||
                data === null ||
                !Object.hasOwn(data, "reply") ||
                typeof data.reply !== "string"
            ) {
                throw new Error("Invalid response format");
            }
            output.textContent = data.reply;


        // If something goes wrong it will catch the error
        } catch (error) {
            console.error("Backend communication error:", error);
            output.textContent = "Communication error";
            await backendLogSender("Backend communication error", { error: error.message });
            return;

        } finally {
            sendBtn.disabled = false;
        }
    });
});
'@

# HTML file rewrite
Set-Content -Path "$root\frontend\index.html" -Value @'
<!DOCTYPE html>
<html lang="en">
<!-- Main settings of the web page -->
<head>
    <meta charset="UTF-8">
    <title>AI Email Agent</title>

    <!-- Settings for responsive design -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <h1>AI Email Agent</h1>

    <textarea id="emailInput" placeholder="Write an email text…" rows="10" cols="70"></textarea><br>

    <button id="sendBtn">Send to AI</button>

    <h2>AI Response:</h2>
    <pre id="output"></pre>


    <!-- Loads JavaScript file(s) -->
    <script type="module" src="js/app.js"></script>
</body>
</html>
'@
