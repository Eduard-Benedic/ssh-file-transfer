from cryptography.fernet import Fernet


class Encryptor:
  def encrypt(img: bytes, algorithm: str | list[str]) -> list[bytes]:
    key = Fernet.generate_key()
    fernet = Fernet(key)
    print(len(fernet.encrypt(img)))
    print(len(fernet.decrypt(img)))
    pass

"""
Takes in an image and along with one or more algorithms and returns an encrypted
image.
"""
def encrypt(file: bytes, algorithm: str | list[str]) -> list[bytes]:
  key = Fernet.generate_key()
  fernet = Fernet(key)
  encrypted_msg = fernet.encrypt(file)
  print(type(encrypted_msg), '\n\n\n')
  print(type(fernet.decrypt(encrypted_msg)))
  pass

# message = "cryptocurrency key"

# key = Fernet.generate_key()

# fernet = Fernet(key)

# print(type(message.encode()))
