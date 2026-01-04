# Alice and Bob exchange X25519 public keys, compute a shared secret, then run HKDF to get a usable symmetric key.

from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
import binascii

def generate_x25519_keypair():
    # Generate an X25519 keypair.
    private = x25519.X25519PrivateKey.generate()
    public = private.public_key()
    return private, public

def public_bytes(public_key):
    # Serialize an X25519 public key to 32 raw bytes.
    return public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

def derive_shared_key(our_private: x25519.X25519PrivateKey, their_public_bytes: bytes, info: bytes = b"secure_channel_v1"):
    # DH exchange + HKDF to produce a 32-byte symmetric key.
    their_public = x25519.X25519PublicKey.from_public_bytes(their_public_bytes)
    shared_secret = our_private.exchange(their_public)
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=info,
    )
    key = hkdf.derive(shared_secret)
    return key

def main():
    # Alice
    alice_priv, alice_pub = generate_x25519_keypair()
    # Bob
    bob_priv, bob_pub = generate_x25519_keypair()

    alice_pub_bytes = public_bytes(alice_pub)
    bob_pub_bytes = public_bytes(bob_pub)

    print("Alice public (hex):", binascii.hexlify(alice_pub_bytes).decode())
    print("Bob   public (hex):", binascii.hexlify(bob_pub_bytes).decode())

    alice_key = derive_shared_key(alice_priv, bob_pub_bytes, info=b"secure_channel_v1")
    bob_key   = derive_shared_key(bob_priv, alice_pub_bytes, info=b"secure_channel_v1")

    print("\nDerived symmetric keys (hex):")
    print("Alice key:", binascii.hexlify(alice_key).decode())
    print("Bob   key:", binascii.hexlify(bob_key).decode())

    if alice_key == bob_key:
        print("\n[SUCCESS] Alice and Bob derived the same symmetric key.")
    else:
        print("\n[ERROR] Keys differ! (This would indicate a problem or an active attacker.)")

if __name__ == "__main__":
    main()
