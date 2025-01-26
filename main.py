from flask import Flask, url_for, request

app = Flask(__name__)

@app.route("/")
def home():

    image_url = url_for("static", filename="images/zoobie.jpg")
    user_ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    user_agent = request.headers.get('User-Agent')

    return f"""
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
            </head>
            <body>
                <div class="bg">
                    <div class="text">
                        <h1>Plhrofories malaka apo Zoobie</h1>
                        <p>IP: {user_ip}</p>
                        <p>User-Agent: {user_agent}</p>
                        <p>Full headers: {request.headers}</p>
                    </div>
                </div>
            </body>
        </html>
    """

if __name__ == "__main__":
    app.run()
