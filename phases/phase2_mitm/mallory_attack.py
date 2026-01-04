# Mallory swaps public keys so Alice and Bob each end up sharing a key with Mallory.

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


class Participant:
    # Honest participant (Alice or Bob).
    
    def __init__(self, name):
        self.name = name
        self.private_key = None
        self.public_key = None
        self.public_key_bytes = None
        self.shared_key = None
    
    def generate_keypair(self):
        self.private_key, self.public_key = generate_x25519_keypair()
        self.public_key_bytes = public_bytes(self.public_key)
        print(f"{self.name}: Generated keypair")
        print(f"{self.name}: Public key (hex): {binascii.hexlify(self.public_key_bytes).decode()}")
    
    def derive_key(self, peer_public_bytes):
        # Derive the shared key from a peer's (unauthenticated) public key.
        self.shared_key = derive_shared_key(self.private_key, peer_public_bytes)
        print(f"{self.name}: Derived shared key (hex): {binascii.hexlify(self.shared_key).decode()}")


class Mallory:
    # MITM attacker: swaps DH public keys and sits in the middle.
    
    def __init__(self):
        self.name = "Mallory"
        self.alice_priv, self.alice_pub = generate_x25519_keypair()
        self.bob_priv, self.bob_pub = generate_x25519_keypair()
        self.alice_pub_bytes = public_bytes(self.alice_pub)  # sent to Bob
        self.bob_pub_bytes = public_bytes(self.bob_pub)      # sent to Alice

        self.key_with_alice = None
        self.key_with_bob = None
        
        print(f"{self.name}: Generated keypairs for attack")
        print(f"{self.name}: Public key for impersonating Alice (hex): {binascii.hexlify(self.alice_pub_bytes).decode()}")
        print(f"{self.name}: Public key for impersonating Bob (hex): {binascii.hexlify(self.bob_pub_bytes).decode()}")
    
    def intercept_and_replace(self, message_from, message_to):
        # Intercept a public key and forward Mallory's instead.
        real_pub_bytes = message_from.public_key_bytes
        
        # Handle the case where Alice is sending her key to Bob
        if message_from.name == "Alice":
            self.key_with_alice = derive_shared_key(
                self.bob_priv,
                real_pub_bytes
            )
            print(f"{self.name}: [INTERCEPTED] Alice's public key")
            print(f"{self.name}: Derived key with Alice (hex): {binascii.hexlify(self.key_with_alice).decode()}")
            print(f"{self.name}: [FORWARDING] Fake Bob's public key to Alice")
            return self.bob_pub_bytes
        
        # Handle the case where Bob is sending his key to Alice
        elif message_from.name == "Bob":
            self.key_with_bob = derive_shared_key(
                self.alice_priv,
                real_pub_bytes
            )
            print(f"{self.name}: [INTERCEPTED] Bob's public key")
            print(f"{self.name}: Derived key with Bob (hex): {binascii.hexlify(self.key_with_bob).decode()}")
            print(f"{self.name}: [FORWARDING] Fake Alice's public key to Bob")
            return self.alice_pub_bytes
    
    def can_decrypt(self, encrypted_message, sender):
        if sender == "Alice":
            return self.key_with_alice is not None
        elif sender == "Bob":
            return self.key_with_bob is not None
        return False


def demonstrate_mitm_attack():
    # Run the MITM demo and show who shares keys with whom.
    print("=" * 70)
    print("PHASE 2: Man-in-the-Middle Attack Demonstration")
    print("=" * 70)
    print()
    
    alice = Participant("Alice")
    bob = Participant("Bob")
    mallory = Mallory()

    print("\n" + "-" * 70)
    print("STEP 1: Alice generates keypair")
    print("-" * 70)
    alice.generate_keypair()

    print("\n" + "-" * 70)
    print("STEP 2: Alice sends public key to Bob (intercepted by Mallory)")
    print("-" * 70)
    fake_bob_key_for_alice = mallory.intercept_and_replace(alice, bob)

    print("\n" + "-" * 70)
    print("STEP 3: Bob generates keypair")
    print("-" * 70)
    bob.generate_keypair()

    print("\n" + "-" * 70)
    print("STEP 4: Bob sends public key to Alice (intercepted by Mallory)")
    print("-" * 70)
    fake_alice_key_for_bob = mallory.intercept_and_replace(bob, alice)

    print("\n" + "-" * 70)
    print("STEP 5: Alice receives fake 'Bob' key and derives shared key")
    print("-" * 70)
    alice.derive_key(fake_bob_key_for_alice)

    print("\n" + "-" * 70)
    print("STEP 6: Bob receives fake 'Alice' key and derives shared key")
    print("-" * 70)
    bob.derive_key(fake_alice_key_for_bob)
    
    print("\n" + "=" * 70)
    print("ATTACK RESULTS")
    print("=" * 70)
    
    print(f"\nAlice's shared key (hex): {binascii.hexlify(alice.shared_key).decode()}")
    print(f"Bob's shared key   (hex): {binascii.hexlify(bob.shared_key).decode()}")
    print(f"Mallory's key with Alice (hex): {binascii.hexlify(mallory.key_with_alice).decode()}")
    print(f"Mallory's key with Bob   (hex): {binascii.hexlify(mallory.key_with_bob).decode()}")
    
    # Verify the attack succeeded
    print("\n" + "-" * 70)
    if alice.shared_key == mallory.key_with_alice:
        print("[ATTACK SUCCESS] Alice shares a key with Mallory (not Bob)")
    else:
        print("[ERROR] Attack simulation failed")
    
    if bob.shared_key == mallory.key_with_bob:
        print("[ATTACK SUCCESS] Bob shares a key with Mallory (not Alice)")
    else:
        print("[ERROR] Attack simulation failed")
    
    if alice.shared_key != bob.shared_key:
        print("[CRITICAL] Alice and Bob have DIFFERENT keys!")
        print("   They cannot communicate securely. Mallory can decrypt everything.")
    else:
        print("[ERROR] Alice and Bob should have different keys after MITM attack")
    
    print("\n" + "=" * 70)
    print("SECURITY ANALYSIS")
    print("=" * 70)
    print("""
The MITM attack succeeded because:
1. The DH key exchange has NO authentication mechanism
2. Public keys are not bound to identities (Alice/Bob)
3. Mallory can impersonate either party without detection

SOLUTION: We need to add digital signatures (Ed25519) to authenticate
public keys. This will be demonstrated in Phase 3.
""")


if __name__ == "__main__":
    demonstrate_mitm_attack()

