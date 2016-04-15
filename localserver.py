import os

from codemangler import app

app.run(port=int(os.getenv('PORT', 8000)), debug=True, threaded=True)
