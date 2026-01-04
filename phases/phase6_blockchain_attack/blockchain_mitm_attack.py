# Mallory tries a few key-swapping tricks; the registry checks stop them.

from cryptography.hazmat.primitives.asymmetric import x25519, ed25519
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature
import binascii
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phase3_auth'))
from authenticated_dh import AuthenticatedParticipant

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'phase5_solana'))
from solana_registry_client import SolanaKeyRegistryClient


class BlockchainRegistry:
    # Tiny in-memory stand-in for an on-chain key registry.
    
    def __init__(self):
        # Map wallet address -> Ed25519 public key bytes.
        self.registry = {}
        print("Blockchain Registry initialized (simulated)")
    
    def register_key(self, wallet_address: str, wallet_keypair, ed25519_public_key: bytes) -> bool:
        # Register a key if the keypair matches the address (simulated ownership check).
        wallet_pubkey = str(wallet_keypair.pubkey())
        
        if wallet_pubkey != wallet_address:
            print(f"[BLOCKCHAIN] Registration REJECTED: Wallet address mismatch")
            print(f"   Provided address: {wallet_address}")
            print(f"   Keypair address: {wallet_pubkey}")
            return False
        
        self.registry[wallet_address] = ed25519_public_key
        print(f"[BLOCKCHAIN] Key registered successfully")
        print(f"   Wallet address: {wallet_address}")
        print(f"   Ed25519 key (hex): {binascii.hexlify(ed25519_public_key).decode()}")
        return True
    
    def verify_key(self, wallet_address: str, ed25519_public_key: bytes) -> bool:
        # Check whether a key matches the registry entry for an address.
        if wallet_address not in self.registry:
            print(f"[BLOCKCHAIN] Verification FAILED: No key registered for address")
            print(f"   Address: {wallet_address}")
            return False
        
        registered_key = self.registry[wallet_address]
        
        if registered_key == ed25519_public_key:
            print(f"[BLOCKCHAIN] Verification SUCCESS: Key matches registry")
            print(f"   Address: {wallet_address}")
            print(f"   Key (hex): {binascii.hexlify(ed25519_public_key).decode()[:32]}...")
            return True
        else:
            print(f"[BLOCKCHAIN] Verification FAILED: Key mismatch")
            print(f"   Address: {wallet_address}")
            print(f"   Expected (hex): {binascii.hexlify(registered_key).decode()[:32]}...")
            print(f"   Received (hex): {binascii.hexlify(ed25519_public_key).decode()[:32]}...")
            print(f"   [WARNING] Possible MITM attack or key compromise!")
            return False


class BlockchainMallory:
    # Mallory tries to mess with registration/verification.
    
    def __init__(self, registry: BlockchainRegistry):
        self.name = "Mallory"
        self.registry = registry
        
        self.dh_priv, self.dh_pub = x25519.X25519PrivateKey.generate(), None
        self.dh_pub = self.dh_priv.public_key()
        self.signing_priv = ed25519.Ed25519PrivateKey.generate()
        self.signing_pub = self.signing_priv.public_key()
        self.signing_pub_bytes = self.signing_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        )
        
        # Mallory's "wallet" (mock)
        self.mallory_wallet_address = "Mallory1111111111111111111111111111111111"
        self.mallory_wallet_keypair = type('MockKeypair', (), {
            'pubkey': lambda: type('MockPubkey', (), {'__str__': lambda: self.mallory_wallet_address})()
        })()
        
        print(f"{self.name}: Initialized with own keypairs and wallet")
        print(f"{self.name}: Wallet address: {self.mallory_wallet_address}")
    
    def attack_1_register_alice_key_with_alice_address(self, alice_address: str, alice_signing_pub_bytes: bytes):
        # Attack 1: try to register Alice's key under Alice's address (should fail).
        print("\n" + "=" * 70)
        print("ATTACK 1: Mallory tries to register Alice's key with Alice's address")
        print("=" * 70)
        print(f"{self.name}: Intercepted Alice's signing public key")
        print(f"{self.name}: Attempting to register it for Alice's address...")
        
        success = self.registry.register_key(
            alice_address,
            self.mallory_wallet_keypair,  # Mallory's wallet (WRONG!)
            alice_signing_pub_bytes
        )
        
        if not success:
            print(f"[SUCCESS] Attack 1 PREVENTED: Mallory cannot register keys for addresses she doesn't own")
            print("   Blockchain requires wallet owner to sign registration transaction")
            print("   Mallory doesn't have Alice's wallet private key")
        else:
            print(f"[ERROR] Attack 1 SUCCEEDED (UNEXPECTED): Registration should have failed!")
        
        return not success  # Attack prevented = True
    
    def attack_2_register_own_key_with_alice_address(self, alice_address: str):
        # Attack 2: try to register Mallory's key under Alice's address (should fail).
        print("\n" + "=" * 70)
        print("ATTACK 2: Mallory tries to register her own key with Alice's address")
        print("=" * 70)
        print(f"{self.name}: Attempting to register my own key for Alice's address...")
        print(f"{self.name}: If this works, Bob will think my key is Alice's!")
        
        # Mallory tries to register her own key for Alice's address
        success = self.registry.register_key(
            alice_address,
            self.mallory_wallet_keypair,  # Mallory's wallet (WRONG!)
            self.signing_pub_bytes
        )
        
        if not success:
            print(f"[SUCCESS] Attack 2 PREVENTED: Mallory cannot register keys for addresses she doesn't own")
            print("   Blockchain enforces: only wallet owner can register keys")
            print("   Mallory's wallet address doesn't match Alice's address")
        else:
            print(f"[ERROR] Attack 2 SUCCEEDED (UNEXPECTED): Registration should have failed!")
        
        return not success  # Attack prevented = True
    
    def attack_3_use_alice_key_with_own_address(self, alice_address: str, alice_signing_pub_bytes: bytes):
        # Attack 3: replay Alice's key while claiming a different address (should fail).
        print("\n" + "=" * 70)
        print("ATTACK 3: Mallory intercepts Alice's key and uses it with own address")
        print("=" * 70)
        print(f"{self.name}: Intercepted Alice's signing public key during key exchange")
        print(f"{self.name}: Attempting to use it, claiming it's registered for my address...")
        
        print(f"{self.name}: Registering my own key for my own address (this should work)...")
        self.registry.register_key(
            self.mallory_wallet_address,
            self.mallory_wallet_keypair,
            self.signing_pub_bytes
        )
        
        print(f"\n{self.name}: Sending intercepted Alice's key to Bob...")
        print(f"{self.name}: Bob will verify: Is this key registered for Alice's address?")
        
        # Bob verifies the key on-chain for Alice's address
        verification_result = self.registry.verify_key(alice_address, alice_signing_pub_bytes)
        
        if verification_result:
            print(f"[ERROR] Attack 3 SUCCEEDED (UNEXPECTED): Verification should have failed!")
            print("   Bob should reject keys that don't match on-chain registry")
        else:
            print(f"[SUCCESS] Attack 3 PREVENTED: Bob verified key on-chain")
            print("   Bob checked: Is this key registered for Alice's address?")
            print("   Result: Key mismatch - possible MITM attack detected!")
            print("   Bob correctly rejects the key exchange")
        
        return not verification_result  # Attack prevented = True
    
    def attack_4_register_fake_key_for_own_address(self):
        # Attack 4: register Mallory's key under Mallory's address (works, but doesn't help).
        print("\n" + "=" * 70)
        print("ATTACK 4: Mallory registers fake key for her own address")
        print("=" * 70)
        print(f"{self.name}: Registering my own key for my own address...")
        print(f"{self.name}: This should work (I own my wallet)...")
        
        success = self.registry.register_key(
            self.mallory_wallet_address,
            self.mallory_wallet_keypair,
            self.signing_pub_bytes
        )
        
        if success:
            print(f"[INFO] Attack 4: Registration succeeded (expected - Mallory owns her wallet)")
            print(f"   But this is USELESS for attacking Alice-Bob communication!")
            print(f"   When Bob verifies, he checks Alice's address, not Mallory's")
            print(f"   Bob will verify: Is Mallory's key registered for Alice's address?")
            print(f"   Answer: NO - Attack fails!")
            
            print(f"\n   Simulating Bob's verification...")
            bob_verification = self.registry.verify_key(
                "Alice1111111111111111111111111111111111",  # Alice's address
                self.signing_pub_bytes  # Mallory's key
            )
            
            if not bob_verification:
                print(f"   [SUCCESS] Bob correctly rejects Mallory's key")
                print(f"   Bob checks Alice's address, finds different key")
                print(f"   Attack prevented!")
        else:
            print(f"[ERROR] Registration failed (unexpected)")
        
        return True  # Attack prevented (registration works but is useless)


def demonstrate_blockchain_mitm_attack():
    #
    # Demonstrate Mallory's attacks on blockchain-integrated secure channel.
    #
    # This shows how blockchain prevents various MITM attack strategies by:
    # 1. Requiring wallet ownership to register keys
    # 2. Binding identities to wallet addresses
    # 3. Providing verifiable, immutable key registry
    #
    print("=" * 70)
    print("PHASE 6: Mallory's Attack on Blockchain-Integrated Secure Channel")
    print("=" * 70)
    print()
    print("This phase demonstrates how blockchain prevents MITM attacks")
    print("by requiring wallet ownership and providing verifiable key registry.")
    print()
    
    # Initialize blockchain registry
    registry = BlockchainRegistry()
    
    # Create legitimate participants
    alice = AuthenticatedParticipant("Alice")
    bob = AuthenticatedParticipant("Bob")
    
    # Generate keypairs
    print("\n" + "-" * 70)
    print("STEP 1: Alice and Bob generate keypairs")
    print("-" * 70)
    alice.generate_keypairs()
    bob.generate_keypairs()
    
    # Register legitimate keys on blockchain
    print("\n" + "-" * 70)
    print("STEP 2: Alice and Bob register keys on blockchain")
    print("-" * 70)
    alice_address = "Alice1111111111111111111111111111111111"
    bob_address = "Bob11111111111111111111111111111111111111"
    
    # Mock wallet keypairs (in real implementation, these would be Solana Keypairs)
    alice_wallet = type('MockKeypair', (), {
        'pubkey': lambda: type('MockPubkey', (), {'__str__': lambda: alice_address})()
    })()
    bob_wallet = type('MockKeypair', (), {
        'pubkey': lambda: type('MockPubkey', (), {'__str__': lambda: bob_address})()
    })()
    
    # Register Alice's key
    registry.register_key(alice_address, alice_wallet, alice.signing_public_bytes)
    
    # Register Bob's key
    registry.register_key(bob_address, bob_wallet, bob.signing_public_bytes)
    
    # Create Mallory
    print("\n" + "-" * 70)
    print("STEP 3: Mallory prepares for attack")
    print("-" * 70)
    mallory = BlockchainMallory(registry)
    
    # Execute attacks
    print("\n" + "=" * 70)
    print("MALLORY'S ATTACK ATTEMPTS")
    print("=" * 70)
    
    attack1_prevented = mallory.attack_1_register_alice_key_with_alice_address(
        alice_address,
        alice.signing_public_bytes
    )
    
    attack2_prevented = mallory.attack_2_register_own_key_with_alice_address(
        alice_address
    )
    
    attack3_prevented = mallory.attack_3_use_alice_key_with_own_address(
        alice_address,
        alice.signing_public_bytes
    )
    
    attack4_prevented = mallory.attack_4_register_fake_key_for_own_address()
    
    # Summary
    print("\n" + "=" * 70)
    print("ATTACK SUMMARY")
    print("=" * 70)
    print(f"""
Attack 1 (Register Alice's key with Alice's address): {'PREVENTED' if attack1_prevented else 'SUCCEEDED'}
   Reason: Blockchain requires wallet owner to sign transaction
   
Attack 2 (Register own key with Alice's address): {'PREVENTED' if attack2_prevented else 'SUCCEEDED'}
   Reason: Only wallet owner can register keys for their address
   
Attack 3 (Use Alice's key with own address): {'PREVENTED' if attack3_prevented else 'SUCCEEDED'}
   Reason: Bob verifies key on-chain for Alice's address, finds mismatch
   
Attack 4 (Register fake key for own address): {'PREVENTED' if attack4_prevented else 'SUCCEEDED'}
   Reason: Registration works but is useless - Bob verifies against Alice's address

Total Attacks Prevented: {sum([attack1_prevented, attack2_prevented, attack3_prevented, attack4_prevented])}/4
    """)
    
    print("\n" + "=" * 70)
    print("SECURITY ANALYSIS")
    print("=" * 70)
    print("""
The blockchain-integrated secure channel prevents MITM attacks through:

1. ✅ Wallet Ownership Requirement
   - Only wallet owner can register keys for their address
   - Mallory cannot register keys for Alice's address without Alice's wallet

2. ✅ Identity Binding
   - Solana wallet addresses are bound to Ed25519 signing keys
   - Keys are permanently associated with wallet addresses on-chain

3. ✅ Verifiable Registry
   - Anyone can verify keys on-chain
   - Bob checks: Is this key registered for Alice's address?
   - Mismatch = possible attack, key exchange rejected

4. ✅ Immutability
   - Once registered, keys are on-chain permanently
   - Cannot be retrospectively modified without wallet owner's signature

5. ✅ Decentralized Trust
   - No single point of failure
   - No need to trust centralized certificate authorities
   - Blockchain provides global, verifiable key registry

CONCLUSION: Blockchain adds a strong security layer that prevents
impersonation attacks by requiring wallet ownership and providing
verifiable, immutable key registry.
    """)


if __name__ == "__main__":
    demonstrate_blockchain_mitm_attack()

