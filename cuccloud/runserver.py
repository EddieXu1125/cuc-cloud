# -*- encoding=UTF-8 -*-

from cuccloud import app
from pyOpenSSL import SSL

if __name__ == '__main__':    
    
    app.run(host='0.0.0.0',port=80, debug=True, threaded=True,ssl_content=(''))


