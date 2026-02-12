from auth.hashing import hash_password, verify_password

hashed = hash_password("secret123")

print(hashed)
print(verify_password("secret123", hashed))   # True
print(verify_password("wrong", hashed))       # False
