from cryptography.fernet import Fernet

# key = Fernet.generate_key()
key = "cOGnAckIE30aGn8EWEa4EaqBnMVtS1DGfKewxOknvHc="
f = Fernet(key)
token = f.encrypt(b"")

decript = f.decrypt(b"gAAAAABkVw-y0pIK163vinVW1UjG3rSUUtN7A_LAaHo0npitSKmONR8QcFD6HOo1NjYlYZuY_S7D1eq1IAVXpwTYKgcznWKQwhwk78-tMzJcuyFQ0hZAuFiHYy4u-AkWr-frZQ37YU7kX4D1pCcfYUGvBV43G3dQkAlpg-EkaPpadKynAtVf3YOR79xAC1U2Gnvev_Xkpl6bXN-bIPghtEMHyv1uQXJEorJpNTdu3SaYTz-FAzqCyIS7D9851gcbMqKeOdOmJeCOFruW0gd1RpNusBipDJGqTA==")

print(f"f = {f}")
print(f"key = {key}")
print(f"token encript = {token}")
print(f"decript = {decript}")