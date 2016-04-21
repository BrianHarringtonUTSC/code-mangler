import os

from codemangler import app

# app.run(port=int(os.getenv('PORT', 8000)), debug=True, threaded=True)
app.run(host=os.getenv("IP", "142.1.97.144"),port=int(os.getenv("PORT", 15003)))

