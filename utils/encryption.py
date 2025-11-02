import base64

def encrypt(password):
    return base64.b64encode(password.encode()).decode()

def decrypt(encoded_password):
    return base64.b64decode(encoded_password.encode()).decode()
