import src.musicPlayer as music
from flask import Flask, request, render_template_string, Response
import json

app = Flask(__name__)

# List of main buttons
BUTTONS = [
    "AWOLNATION - Sail",
    "The White Stripes - Seven Nation Army",
]

# Your desktop method to handle commands
def handle_command(command_text):
    print(f"Command received: {command_text}")
    if command_text != "Stop":
        music.addToLibrary(command_text, "")
        music.playSong(command_text, "")
    else:
        music.stopPlaying()

# HTML template with AJAX-enabled buttons
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Command Buttons</title>
    <style>
        body {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            margin: 0;
        }
        h2 {
            font-size: 2.5em;  /* Bigger title */
        }
        .button-form {
            width: 90%;
            margin: 5px 0;
        }
        button {
            width: 100%;
            padding: 20px;
            font-size: 1.5em;
            margin: 5px 0;
        }
        #response {
            margin-top: 20px;
            font-size: 1.2em;
            color: green;
        }
    </style>
</head>
<body>
    <h2>Send Command to Desktop</h2>

    {% for btn in buttons %}
    <div class="button-form">
        <button onclick="sendCommand('{{ btn }}')">{{ btn }}</button>
    </div>
    {% endfor %}

    <!-- Stop button at the bottom -->
    <div class="button-form">
        <button style="background-color: #f44336; color: white;" onclick="sendCommand('Stop')">Stop</button>
    </div>

    <div id="response"></div>

    <script>
        function sendCommand(cmd) {
            fetch("/send_command", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ command: cmd })
            })
            .then(response => response.json())
            .then(data => {
                document.getElementById("response").innerText = "Sent: " + data.command;
            })
            .catch(err => {
                document.getElementById("response").innerText = "Error sending command";
                console.error(err);
            });
        }
    </script>
</body>
</html>
"""

@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE, buttons=BUTTONS)

@app.route("/send_command", methods=["POST"])
def send_command():
    data = request.get_json()
    command_text = data.get("command") if data else None
    if command_text:
        handle_command(command_text)
        # Return JSON manually
        return Response(json.dumps({"status": "ok", "command": command_text}),
                        mimetype="application/json")
    return Response(json.dumps({"status": "error", "message": "No command received"}),
                    status=400, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)