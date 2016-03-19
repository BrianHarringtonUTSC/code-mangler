import os

from codemangler import app

port = int(os.getenv('PORT', 8000))
app.debug = True
app.run(port=port)
# app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", 8080)))
