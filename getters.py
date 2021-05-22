def get_text_file(path):
    f = open(path, 'r')
    content = f.read()
    f.close()
    return content.encode()

def get_binary_file(path):
    f = open(path, 'rb')
    content = f.read()
    f.close()
    return content
