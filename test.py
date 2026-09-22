from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

hashed = password_hash.hash("password")
print(hashed)