from selfsign import generate_selfsign

if __name__=='__main__':
    hostname = 'cuccloud.edu.cn'
    files = dict()
    files['cert.pem'],files['key.pem'] = generate_selfsign(hostname)
    for filename,content in files.items():
        with open(filename,'wb') as f:
            f.write(content)