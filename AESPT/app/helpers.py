import aes
from base64 import b64decode
from base64 import b64encode


KEY = "evlzctfverymahan"
cipher = aes.AESCipher(KEY)

def encrypt(plaintext):
    return cipher.encrypt(plaintext)

def decrypt(ciphertext):
    return cipher.decrypt(ciphertext)


# Generate AES Encrypted Cookie based on format:
#           encrypt( "username:<0/1>"(=>admin_flag) )
#           ex. "batterycharger:1", cookie: b64encode(927e323b9ea14b1d8f1459d106b6074a6db48f0b24f00137859d3d4cb08284b0)
#                                           OWUwMTk0M2E0YjY4MGJhZGIzZGZkZGEwN2Q1MmM4YjE=
def generateCookie(username, admin):
    cookie_string = username+":1" if admin else username+":0"
    encrypted_cookie = encrypt(cookie_string)
    # encode encrypted_cookie string to bytes and convert to b64
    encoded_cookie = b64encode(encrypted_cookie.encode())
    return encoded_cookie.decode()

def decryptCookie(encoded_cookie):
    try:
        encrypted_cookie = b64decode(encoded_cookie)
    except:
        return None

    cookie_string = decrypt(encrypted_cookie)
    cookie_data = cookie_string.split(":")
    username = cookie_data[0]
    admin = bool(int(cookie_data[1]))

    return  {'username' : username, 'admin' : admin}
    