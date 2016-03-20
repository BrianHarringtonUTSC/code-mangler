import os

from codemangler import app

app.run(port=int(os.getenv('PORT', 8000)), debug=True)
# app.run(host=os.getenv("IP", "0.0.0.0"),port=int(os.getenv("PORT", 8080)))
