from Crypto.Cipher import AES
from Crypto import Random
from cryptography.fernet import Fernet

def load_key(root):
    key_dir = root + "/keygen.key"
    iv_dir = root + "/ivgen.key"
    """
    Loads the key from the current directory named `keygen.key`
    """
    try:
        key = open(key_dir, "r").read()
        iv = open(iv_dir, "r").read()
        return key
    except:
        write_key(root)
        key = open(key_dir, "r").read()
        iv = open(iv_dir, "r").read()
        return key


def write_key(root):
    key_dir = root + "/keygen.key"
    iv_dir = root + "/ivgen.key"
    """
    Generates a key and save it into a file
    """
    key = Random.new().read(AES.block_size)
    iv = Random.new().read(AES.block_size)
    with open(key_dir, "w") as key_file:
        key_file.write(key)
    with open(iv_dir, "w") as iv_file:
        iv_file.write(iv)
    key_file.close()
    iv_file.close()


def encrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    input_file = open(filename)
    input_data = input_file.read()
    input_file.close()

    cfb_cipher = AES.new(key, AES.MODE_CFB, key)
    enc_data = cfb_cipher.encrypt(input_data)

    enc_file = open(filename, "w")
    enc_file.write(enc_data)
    enc_file.close()

def decrypt(filename, key):
    """
    Given a filename (str) and key (bytes), it decrypts the file and write it
    """
    enc_file2 = open(filename)
    enc_data2 = enc_file2.read()
    enc_file2.close()

    cfb_decipher = AES.new(key, AES.MODE_CFB, key)
    plain_data = cfb_decipher.decrypt(enc_data2)

    output_file = open(filename, "w")
    output_file.write(plain_data)
    output_file.close()