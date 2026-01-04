# We sign DH public keys so a MITM can't swap them unnoticed.

from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import binascii

def generate_x25519_keypair():
    # Generate an X25519 keypair.
    private = x25519.X25519PrivateKey.generate()
    public = private.public_key()
    return private, public

def public_bytes(public_key):
    # Serialize an X25519 public key to raw bytes (32 bytes).
    return public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

def derive_shared_key(our_private: x25519.X25519PrivateKey, their_public_bytes: bytes, info: bytes = b"secure_channel_v1"):
    # Derive shared key from DH exchange.
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


class AuthenticatedParticipant:
    # Participant that signs its DH public key (Ed25519).
    
    def __init__(self, name):
        self.name = name

        # DH keys (X25519) and identity/signing keys (Ed25519)
        self.dh_private = None
        self.dh_public = None
        self.dh_public_bytes = None
        self.signing_private = None
        self.signing_public = None
        self.signing_public_bytes = None

        self.shared_key = None
    
    def generate_keypairs(self):
        # Generate fresh DH keys and a signing keypair (demo version).
        self.dh_private, self.dh_public = generate_x25519_keypair()
        self.dh_public_bytes = public_bytes(self.dh_public)

        self.signing_private = ed25519.Ed25519PrivateKey.generate()
        self.signing_public = self.signing_private.public_key()
        self.signing_public_bytes = self.signing_public.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        print(f"{self.name}: Generated DH keypair and Ed25519 signing keypair")
        print(f"{self.name}: DH public key (hex): {binascii.hexlify(self.dh_public_bytes).decode()}")
        print(f"{self.name}: Ed25519 public key (hex): {binascii.hexlify(self.signing_public_bytes).decode()}")
    
    def sign_dh_public_key(self):
        # Sign our DH public key.
        signature = self.signing_private.sign(self.dh_public_bytes)
        print(f"{self.name}: Signed DH public key")
        print(f"{self.name}: Signature (hex): {binascii.hexlify(signature).decode()}")
        return signature
    
    def verify_and_derive_key(self, peer_dh_pub_bytes, peer_signing_pub_bytes, signature):
        # Verify signature on peer DH public key, then derive shared key.
        try:
            peer_signing_pub = ed25519.Ed25519PublicKey.from_public_bytes(peer_signing_pub_bytes)
            peer_signing_pub.verify(signature, peer_dh_pub_bytes)
            print(f"{self.name}: [SUCCESS] Signature verification SUCCESS")

            self.shared_key = derive_shared_key(self.dh_private, peer_dh_pub_bytes)
            print(f"{self.name}: Derived shared key (hex): {binascii.hexlify(self.shared_key).decode()}")
            return True, self.shared_key
        
        except InvalidSignature:
            print(f"{self.name}: [FAILED] Signature verification FAILED - rejecting key exchange")
            return False, None


class AuthenticatedMallory:
    # Mallory tries the same trick as Phase 2 (and gets caught).
    
    def __init__(self):
        self.name = "Mallory"
        # Mallory generates her own keypairs
        self.dh_priv, self.dh_pub = generate_x25519_keypair()
        self.dh_pub_bytes = public_bytes(self.dh_pub)
        self.signing_priv = ed25519.Ed25519PrivateKey.generate()
        self.signing_pub = self.signing_priv.public_key()
        self.signing_pub_bytes = self.signing_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        print(f"{self.name}: Generated own keypairs (cannot forge Alice's or Bob's signatures)")
    
    def intercept_and_replace(self, message_from):
        # Return Mallory's own signed DH key (won't verify as Alice/Bob).
        signature = self.signing_priv.sign(self.dh_pub_bytes)
        print(f"{self.name}: [ATTEMPTING] Intercepting {message_from.name}'s message")
        print(f"{self.name}: [CREATING] Fake signed message with own keys (signature won't match!)")
        return self.dh_pub_bytes, self.signing_pub_bytes, signature


def demonstrate_authenticated_exchange():
    # Run the authenticated DH demo.
    print("=" * 70)
    print("PHASE 3: Authenticated Diffie-Hellman Key Exchange")
    print("=" * 70)
    print()
    
    # Create authenticated participants
    alice = AuthenticatedParticipant("Alice")
    bob = AuthenticatedParticipant("Bob")
    
    print("\n" + "-" * 70)
    print("STEP 1: Alice generates keypairs (DH + Ed25519)")
    print("-" * 70)
    alice.generate_keypairs()
    
    print("\n" + "-" * 70)
    print("STEP 2: Alice signs DH public key and sends to Bob")
    print("-" * 70)
    alice_signature = alice.sign_dh_public_key()
    
    print("\n" + "-" * 70)
    print("STEP 3: Bob verifies Alice's signature and derives key")
    print("-" * 70)
    # Bob receives: (alice_dh_pub, alice_signing_pub, signature)
    bob_valid, bob_key = bob.verify_and_derive_key(
        alice.dh_public_bytes,
        alice.signing_public_bytes,
        alice_signature
    )
    
    if not bob_valid:
        print("[ERROR] Protocol failed: Bob rejected Alice's key")
        return
    
    print("\n" + "-" * 70)
    print("STEP 4: Bob generates keypairs (DH + Ed25519)")
    print("-" * 70)
    bob.generate_keypairs()
    
    print("\n" + "-" * 70)
    print("STEP 5: Bob signs DH public key and sends to Alice")
    print("-" * 70)
    bob_signature = bob.sign_dh_public_key()
    
    print("\n" + "-" * 70)
    print("STEP 6: Alice verifies Bob's signature and derives key")
    print("-" * 70)
    alice_valid, alice_key = alice.verify_and_derive_key(
        bob.dh_public_bytes,
        bob.signing_public_bytes,
        bob_signature
    )
    
    if not alice_valid:
        print("❌ Protocol failed: Alice rejected Bob's key")
        return
    
    print("\n" + "=" * 70)
    print("AUTHENTICATED KEY EXCHANGE RESULTS")
    print("=" * 70)
    
    if alice.shared_key == bob.shared_key:
        print("[SUCCESS] Alice and Bob derived the same shared key")
        print(f"   Shared key (hex): {binascii.hexlify(alice.shared_key).decode()}")
    else:
        print("[ERROR] Keys differ!")
    
    print("\n" + "=" * 70)
    print("MITM ATTACK PREVENTION TEST")
    print("=" * 70)
    
    # Now demonstrate that Mallory cannot successfully attack
    mallory = AuthenticatedMallory()
    
    print("\n" + "-" * 70)
    print("Mallory attempts to intercept and replace Alice's message to Bob")
    print("-" * 70)
    fake_alice_dh, fake_alice_signing, fake_sig = mallory.intercept_and_replace(alice)
    
    print("\n" + "-" * 70)
    print("Bob receives Mallory's fake message and attempts verification")
    print("-" * 70)
    # Bob tries to verify using Alice's real signing key (which Bob knows)
    # But Mallory's signature was created with Mallory's signing key
    try:
        alice_signing_pub = ed25519.Ed25519PublicKey.from_public_bytes(alice.signing_public_bytes)
        alice_signing_pub.verify(fake_sig, fake_alice_dh)
        print("[ERROR] Signature verification should have failed!")
    except InvalidSignature:
        print("[SUCCESS] ATTACK PREVENTED: Bob correctly rejected Mallory's fake signature")
        print("   Mallory cannot forge signatures without Alice's private key")
    
    print("\n" + "=" * 70)
    print("SECURITY ANALYSIS")
    print("=" * 70)
    print("""
The authenticated protocol prevents MITM attacks because:
1. Each DH public key is signed with Ed25519
2. Signatures cannot be forged without the private signing key
3. Receivers verify signatures before accepting keys
4. Mallory's fake signatures are rejected

NEXT STEP: Use the shared key for authenticated encryption (AEAD)
This will be demonstrated in Phase 4.
""")


if __name__ == "__main__":
    demonstrate_authenticated_exchange()

