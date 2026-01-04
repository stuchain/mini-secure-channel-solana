# Run all phases in order (interactive demo runner).

import sys
import os

def print_separator(title=""):
    # Print a simple banner.
    print("\n" + "=" * 80)
    if title:
        print(f"  {title}")
        print("=" * 80)
    print()


def run_phase(phase_num, phase_name, script_path):
    # Run a phase script (keep going if it fails).
    print_separator(f"PHASE {phase_num}: {phase_name}")
    
    try:
        # Make the phase script's folder importable (for local imports)
        script_dir = os.path.dirname(os.path.abspath(script_path))
        if script_dir not in sys.path:
            sys.path.insert(0, script_dir)

        with open(script_path, 'r') as f:
            script_code = f.read()

        compiled_code = compile(script_code, script_path, 'exec')

        exec(compiled_code, {'__name__': '__main__'})
        
        print(f"\n[SUCCESS] Phase {phase_num} completed successfully")
        
    except FileNotFoundError:
        print(f"[WARNING] Script not found at {script_path}")
        print("   Skipping this phase...")
        
    except Exception as e:
        print(f"[ERROR] Error in Phase {phase_num}: {e}")
        print("   Continuing to next phase...")
        import traceback
        traceback.print_exc()


def main():
    # Run phases 1–6 with pauses in between.
    
    print_separator("MINI SECURE CHANNEL - COMPLETE DEMONSTRATION")
    print("""
This demo will run all phases of the secure channel implementation:
  1. Basic Diffie-Hellman Key Exchange
     - Shows how two parties can establish a shared secret
     - No authentication - vulnerable to MITM
  
  2. MITM Attack Demonstration
     - Shows how Mallory can intercept and manipulate the key exchange
     - Demonstrates the vulnerability of unauthenticated protocols
  
  3. Authenticated Diffie-Hellman (MITM Prevention)
     - Adds Ed25519 digital signatures to authenticate public keys
     - Shows how authentication prevents MITM attacks
  
  4. Secure Channel with AEAD Encryption
     - Uses ChaCha20-Poly1305 for authenticated encryption
     - Provides confidentiality, integrity, and authentication
  
  5. Blockchain Integration (Solana)
     - Uses Solana blockchain as a decentralized key registry
     - Adds an additional trust layer for key verification
  
  6. Blockchain Attack Prevention
     - Demonstrates Mallory's attacks on blockchain-integrated system
     - Shows how blockchain prevents all attack attempts
    
Press Enter to start, or Ctrl+C to cancel...
    """)
    
    # Wait for user confirmation before starting
    try:
        input()
    except KeyboardInterrupt:
        print("\nDemo cancelled.")
        return
    
    run_phase(1, "Basic Diffie-Hellman Key Exchange", 
              "phases/phase1_dh/dh_exchange.py")
    
    input("\nPress Enter to continue to Phase 2...")
    
    run_phase(2, "Man-in-the-Middle Attack", 
              "phases/phase2_mitm/mallory_attack.py")
    
    input("\nPress Enter to continue to Phase 3...")
    
    run_phase(3, "Authenticated Diffie-Hellman", 
              "phases/phase3_auth/authenticated_dh.py")
    
    input("\nPress Enter to continue to Phase 4...")
    
    run_phase(4, "Secure Channel with AEAD Encryption", 
              "phases/phase4_aead/secure_channel.py")
    
    input("\nPress Enter to continue to Phase 5...")
    
    run_phase(5, "Blockchain Integration (Solana)", 
              "phases/phase5_solana/solana_registry_client.py")
    
    input("\nPress Enter to continue to Phase 6...")
    
    run_phase(6, "Blockchain Attack Prevention", 
              "phases/phase6_blockchain_attack/blockchain_mitm_attack.py")

    print_separator("DEMONSTRATION COMPLETE")
    print("""
All phases have been demonstrated. Key takeaways:

1. [SUCCESS] Diffie-Hellman enables secure key exchange
   - Two parties can establish a shared secret over an insecure channel
   - Based on the discrete logarithm problem

2. [WARNING] Unauthenticated DH is vulnerable to MITM attacks
   - Without authentication, attackers can intercept and replace keys
   - This is why authentication is critical in secure protocols

3. [SUCCESS] Digital signatures (Ed25519) prevent MITM attacks
   - Signatures bind public keys to identities
   - Cannot be forged without the private key

4. [SUCCESS] AEAD encryption provides confidentiality + integrity
   - ChaCha20-Poly1305 encrypts messages and detects tampering
   - Provides all security properties needed for secure communication

5. [SUCCESS] Blockchain adds decentralized trust layer
   - Solana blockchain provides immutable key registry
   - Eliminates need for centralized certificate authorities

6. [SUCCESS] Blockchain prevents all MITM attack attempts
   - Wallet ownership requirement prevents impersonation
   - On-chain verification catches key mismatches
   - All 4 attack strategies fail due to blockchain security

For detailed explanations and code, see individual phase files.
For visualizations, run: python visualizations/diagram_generator.py
    """)


if __name__ == "__main__":
    main()


