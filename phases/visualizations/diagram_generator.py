# Generate the project diagrams (one image per phase).

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, ConnectionPatch
import matplotlib.patheffects as path_effects


def create_dh_exchange_diagram():
    # Create a diagram showing basic DH key exchange between Alice and Bob
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    
    # Alice and Bob boxes
    alice_box = FancyBboxPatch((0.5, 2), 2, 2, boxstyle="round,pad=0.1", 
                                facecolor='lightblue', edgecolor='blue', linewidth=2)
    bob_box = FancyBboxPatch((7.5, 2), 2, 2, boxstyle="round,pad=0.1", 
                              facecolor='lightgreen', edgecolor='green', linewidth=2)
    ax.add_patch(alice_box)
    ax.add_patch(bob_box)
    
    # Labels
    ax.text(1.5, 4.5, 'Alice', ha='center', va='center', fontsize=14, weight='bold')
    ax.text(8.5, 4.5, 'Bob', ha='center', va='center', fontsize=14, weight='bold')
    
    # Public keys
    ax.text(1.5, 3.5, 'g^a (pub)', ha='center', va='center', fontsize=10)
    ax.text(8.5, 3.5, 'g^b (pub)', ha='center', va='center', fontsize=10)
    
    # Arrows showing key exchange
    arrow1 = FancyArrowPatch((2.5, 3), (7.5, 3.8), 
                             arrowstyle='->', mutation_scale=20, 
                             color='blue', linewidth=2, label='Alice → Bob: g^a')
    arrow2 = FancyArrowPatch((7.5, 2.2), (2.5, 3), 
                             arrowstyle='->', mutation_scale=20, 
                             color='green', linewidth=2, label='Bob → Alice: g^b')
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    
    # Shared key
    ax.text(5, 1, 'Shared Key: g^(ab)', ha='center', va='center', 
            fontsize=12, weight='bold', style='italic',
            bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    ax.set_title('Phase 1: Basic Diffie-Hellman Key Exchange', fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/dh_exchange.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: visualizations/dh_exchange.png")


def create_mitm_attack_diagram():
    # Create a diagram showing MITM attack
    fig, ax = plt.subplots(1, 1, figsize=(14, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Alice, Mallory, and Bob boxes
    alice_box = FancyBboxPatch((0.5, 5), 2, 2, boxstyle="round,pad=0.1", 
                                facecolor='lightblue', edgecolor='blue', linewidth=2)
    mallory_box = FancyBboxPatch((4.5, 2), 3, 2, boxstyle="round,pad=0.1", 
                                 facecolor='lightcoral', edgecolor='red', linewidth=2)
    bob_box = FancyBboxPatch((9.5, 5), 2, 2, boxstyle="round,pad=0.1", 
                             facecolor='lightgreen', edgecolor='green', linewidth=2)
    ax.add_patch(alice_box)
    ax.add_patch(mallory_box)
    ax.add_patch(bob_box)
    
    # Labels
    ax.text(1.5, 7, 'Alice', ha='center', va='center', fontsize=14, weight='bold')
    ax.text(6, 3.5, 'Mallory\n(Attacker)', ha='center', va='center', fontsize=12, weight='bold', color='darkred')
    ax.text(10.5, 7, 'Bob', ha='center', va='center', fontsize=14, weight='bold')
    
    # Attack arrows
    arrow1 = FancyArrowPatch((2.5, 6), (4.5, 3.5), arrowstyle='->', mutation_scale=20, 
                             color='blue', linewidth=2)
    arrow2 = FancyArrowPatch((4.5, 3.5), (9.5, 6.2), arrowstyle='->', mutation_scale=20, 
                             color='red', linewidth=2, linestyle='--')
    arrow3 = FancyArrowPatch((9.5, 5.8), (4.5, 2.5), arrowstyle='->', mutation_scale=20, 
                             color='green', linewidth=2)
    arrow4 = FancyArrowPatch((4.5, 2.5), (2.5, 6), arrowstyle='->', mutation_scale=20, 
                             color='red', linewidth=2, linestyle='--')
    
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    ax.add_patch(arrow3)
    ax.add_patch(arrow4)
    
    # Labels on arrows
    ax.text(3.5, 5.5, 'g^a', ha='center', fontsize=10, color='blue')
    ax.text(7, 5, 'g^m', ha='center', fontsize=10, color='red', style='italic', weight='bold')
    ax.text(7, 3.5, 'g^b', ha='center', fontsize=10, color='green')
    ax.text(3.5, 3.5, 'g^m', ha='center', fontsize=10, color='red', style='italic', weight='bold')
    
    # Result boxes
    result1 = FancyBboxPatch((0.5, 0.5), 2, 1, boxstyle="round,pad=0.1", 
                             facecolor='yellow', edgecolor='orange', linewidth=1)
    result2 = FancyBboxPatch((9.5, 0.5), 2, 1, boxstyle="round,pad=0.1", 
                             facecolor='yellow', edgecolor='orange', linewidth=1)
    ax.add_patch(result1)
    ax.add_patch(result2)
    
    ax.text(1.5, 1, 'Key: g^(am)', ha='center', va='center', fontsize=10)
    ax.text(10.5, 1, 'Key: g^(bm)', ha='center', va='center', fontsize=10)
    
    # Warning
    ax.text(6, 0.5, '⚠️ MITM SUCCESS', ha='center', va='center', 
            fontsize=14, weight='bold', color='red',
            bbox=dict(boxstyle='round', facecolor='pink', alpha=0.8))
    
    ax.set_title('Phase 2: Man-in-the-Middle Attack', fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/mitm_attack.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: visualizations/mitm_attack.png")


def create_authenticated_flow_diagram():
    # Create a diagram showing authenticated DH with signatures
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Alice and Bob
    alice_box = FancyBboxPatch((0.5, 6), 2.5, 3, boxstyle="round,pad=0.1", 
                               facecolor='lightblue', edgecolor='blue', linewidth=2)
    bob_box = FancyBboxPatch((9, 6), 2.5, 3, boxstyle="round,pad=0.1", 
                             facecolor='lightgreen', edgecolor='green', linewidth=2)
    ax.add_patch(alice_box)
    ax.add_patch(bob_box)
    
    ax.text(1.75, 8.5, 'Alice', ha='center', va='center', fontsize=14, weight='bold')
    ax.text(10.25, 8.5, 'Bob', ha='center', va='center', fontsize=14, weight='bold')
    
    # Keys
    ax.text(1.75, 7.8, 'DH: g^a', ha='center', fontsize=10)
    ax.text(1.75, 7.3, 'Sign: Ed25519', ha='center', fontsize=10)
    ax.text(10.25, 7.8, 'DH: g^b', ha='center', fontsize=10)
    ax.text(10.25, 7.3, 'Sign: Ed25519', ha='center', fontsize=10)
    
    # Messages
    msg1 = FancyBboxPatch((3.5, 8), 3, 0.8, boxstyle="round,pad=0.05", 
                         facecolor='white', edgecolor='blue', linewidth=1.5)
    msg2 = FancyBboxPatch((6, 6.5), 3, 0.8, boxstyle="round,pad=0.05", 
                         facecolor='white', edgecolor='green', linewidth=1.5)
    ax.add_patch(msg1)
    ax.add_patch(msg2)
    
    ax.text(5, 8.4, '{g^a, sig_a(g^a)}', ha='center', fontsize=11, weight='bold')
    ax.text(7.5, 6.9, '{g^b, sig_b(g^b)}', ha='center', fontsize=11, weight='bold')
    
    # Arrows
    arrow1 = FancyArrowPatch((3, 8.4), (9, 8.4), arrowstyle='->', mutation_scale=20, 
                             color='blue', linewidth=2)
    arrow2 = FancyArrowPatch((9, 6.9), (3, 6.9), arrowstyle='->', mutation_scale=20, 
                             color='green', linewidth=2)
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    
    # Verification
    verify1 = FancyBboxPatch((4.5, 4.5), 3, 1, boxstyle="round,pad=0.1", 
                             facecolor='lightyellow', edgecolor='orange', linewidth=2)
    verify2 = FancyBboxPatch((4.5, 2.5), 3, 1, boxstyle="round,pad=0.1", 
                             facecolor='lightyellow', edgecolor='orange', linewidth=2)
    ax.add_patch(verify1)
    ax.add_patch(verify2)
    
    ax.text(6, 5, 'Bob verifies sig_a(g^a)', ha='center', va='center', fontsize=11)
    ax.text(6, 3, 'Alice verifies sig_b(g^b)', ha='center', va='center', fontsize=11)
    
    # Success
    ax.text(6, 0.5, '✅ Shared Key: g^(ab) (Verified)', ha='center', va='center', 
            fontsize=14, weight='bold', color='green',
            bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8))
    
    ax.set_title('Phase 3: Authenticated Diffie-Hellman (MITM Prevented)', 
                 fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/authenticated_flow.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: visualizations/authenticated_flow.png")


def create_secure_channel_diagram():
    # Create a diagram showing complete secure channel with AEAD
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Alice and Bob
    alice_box = FancyBboxPatch((0.5, 6), 3, 3, boxstyle="round,pad=0.1", 
                               facecolor='lightblue', edgecolor='blue', linewidth=2)
    bob_box = FancyBboxPatch((8.5, 6), 3, 3, boxstyle="round,pad=0.1", 
                             facecolor='lightgreen', edgecolor='green', linewidth=2)
    ax.add_patch(alice_box)
    ax.add_patch(bob_box)
    
    ax.text(2, 8.5, 'Alice', ha='center', fontsize=14, weight='bold')
    ax.text(10, 8.5, 'Bob', ha='center', fontsize=14, weight='bold')
    
    # Secure channel components
    ax.text(2, 7.8, 'Secure Channel', ha='center', fontsize=12, weight='bold')
    ax.text(2, 7.3, '• Authenticated DH', ha='center', fontsize=9)
    ax.text(2, 7, '• Shared Key', ha='center', fontsize=9)
    ax.text(2, 6.7, '• ChaCha20-Poly1305', ha='center', fontsize=9)
    
    ax.text(10, 7.8, 'Secure Channel', ha='center', fontsize=12, weight='bold')
    ax.text(10, 7.3, '• Authenticated DH', ha='center', fontsize=9)
    ax.text(10, 7, '• Shared Key', ha='center', fontsize=9)
    ax.text(10, 6.7, '• ChaCha20-Poly1305', ha='center', fontsize=9)
    
    # Messages
    msg_box1 = FancyBboxPatch((4, 7.5), 3.5, 1, boxstyle="round,pad=0.1", 
                             facecolor='white', edgecolor='purple', linewidth=2)
    msg_box2 = FancyBboxPatch((4.5, 5.5), 3.5, 1, boxstyle="round,pad=0.1", 
                             facecolor='white', edgecolor='purple', linewidth=2)
    ax.add_patch(msg_box1)
    ax.add_patch(msg_box2)
    
    ax.text(5.75, 8, 'Encrypted Message', ha='center', fontsize=11, weight='bold')
    ax.text(5.75, 7.7, '{ciphertext, nonce}', ha='center', fontsize=10, style='italic')
    ax.text(6.25, 6, 'Encrypted Response', ha='center', fontsize=11, weight='bold')
    ax.text(6.25, 5.7, '{ciphertext, nonce}', ha='center', fontsize=10, style='italic')
    
    # Arrows
    arrow1 = FancyArrowPatch((3.5, 8), (8.5, 8), arrowstyle='->', mutation_scale=20, 
                             color='purple', linewidth=2)
    arrow2 = FancyArrowPatch((8.5, 6), (3.5, 6), arrowstyle='->', mutation_scale=20, 
                             color='purple', linewidth=2)
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    
    # Security properties
    security_box = FancyBboxPatch((3, 2), 6, 2.5, boxstyle="round,pad=0.15", 
                                 facecolor='lightyellow', edgecolor='gold', linewidth=2)
    ax.add_patch(security_box)
    
    ax.text(6, 4, 'Security Properties', ha='center', fontsize=13, weight='bold')
    ax.text(4, 3.5, '✅ Confidentiality', ha='left', fontsize=11)
    ax.text(8, 3.5, '✅ Integrity', ha='left', fontsize=11)
    ax.text(4, 3, '✅ Authentication', ha='left', fontsize=11)
    ax.text(8, 3, '✅ Replay Protection', ha='left', fontsize=11)
    ax.text(6, 2.5, '✅ Forward Secrecy (via ephemeral DH)', ha='center', fontsize=10)
    
    ax.set_title('Phase 4: Secure Channel with AEAD Encryption', 
                 fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/secure_channel.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: visualizations/secure_channel.png")


def create_blockchain_diagram():
    # Create a diagram showing blockchain-integrated key verification
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Participants
    alice_box = FancyBboxPatch((1, 7), 2.5, 2, boxstyle="round,pad=0.1", 
                               facecolor='lightblue', edgecolor='blue', linewidth=2)
    bob_box = FancyBboxPatch((10.5, 7), 2.5, 2, boxstyle="round,pad=0.1", 
                             facecolor='lightgreen', edgecolor='green', linewidth=2)
    ax.add_patch(alice_box)
    ax.add_patch(bob_box)
    
    ax.text(2.25, 8.5, 'Alice', ha='center', fontsize=14, weight='bold')
    ax.text(11.75, 8.5, 'Bob', ha='center', fontsize=14, weight='bold')
    
    # Blockchain
    blockchain_box = FancyBboxPatch((4, 1), 6, 5, boxstyle="round,pad=0.2", 
                                    facecolor='lightgray', edgecolor='black', linewidth=3)
    ax.add_patch(blockchain_box)
    
    ax.text(7, 5.5, 'Solana Blockchain', ha='center', fontsize=16, weight='bold')
    
    # Registry entries
    entry1 = FancyBboxPatch((4.5, 4), 5.5, 0.8, boxstyle="round,pad=0.05", 
                           facecolor='white', edgecolor='blue', linewidth=1)
    entry2 = FancyBboxPatch((4.5, 2.5), 5.5, 0.8, boxstyle="round,pad=0.05", 
                           facecolor='white', edgecolor='green', linewidth=1)
    ax.add_patch(entry1)
    ax.add_patch(entry2)
    
    ax.text(7.25, 4.4, 'Alice: wallet_addr → Ed25519_pubkey', ha='center', fontsize=10)
    ax.text(7.25, 2.9, 'Bob: wallet_addr → Ed25519_pubkey', ha='center', fontsize=10)
    
    # Verification arrows
    arrow1 = FancyArrowPatch((3.5, 8), (5, 4.5), arrowstyle='->', mutation_scale=20, 
                             color='blue', linewidth=2, linestyle='--')
    arrow2 = FancyArrowPatch((11, 8), (9.5, 4.5), arrowstyle='->', mutation_scale=20, 
                             color='green', linewidth=2, linestyle='--')
    arrow3 = FancyArrowPatch((5, 3.5), (3.5, 8), arrowstyle='->', mutation_scale=20, 
                             color='purple', linewidth=2)
    arrow4 = FancyArrowPatch((9.5, 3.5), (11, 8), arrowstyle='->', mutation_scale=20, 
                             color='purple', linewidth=2)
    
    ax.add_patch(arrow1)
    ax.add_patch(arrow2)
    ax.add_patch(arrow3)
    ax.add_patch(arrow4)
    
    ax.text(4, 6.5, 'Register', ha='center', fontsize=10, color='blue', style='italic')
    ax.text(10, 6.5, 'Register', ha='center', fontsize=10, color='green', style='italic')
    ax.text(4, 5.5, 'Verify', ha='center', fontsize=10, color='purple', weight='bold')
    ax.text(10, 5.5, 'Verify', ha='center', fontsize=10, color='purple', weight='bold')
    
    # Key exchange
    msg_box = FancyBboxPatch((4.5, 7.5), 5, 0.6, boxstyle="round,pad=0.05", 
                            facecolor='yellow', edgecolor='orange', linewidth=2)
    ax.add_patch(msg_box)
    ax.text(7, 7.8, 'Key Exchange with Verified Keys', ha='center', fontsize=11, weight='bold')
    
    # Benefits
    benefits_box = FancyBboxPatch((1, 0.5), 12, 0.8, boxstyle="round,pad=0.1", 
                                  facecolor='lightyellow', edgecolor='gold', linewidth=2)
    ax.add_patch(benefits_box)
    ax.text(7, 0.9, 'Decentralized Trust • No Certificate Authorities • Immutable Registry', 
            ha='center', fontsize=11, weight='bold')
    
    ax.set_title('Phase 5: Blockchain-Integrated Key Verification', 
                 fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/blockchain_integration.png', dpi=300, bbox_inches='tight')
    print("✅ Saved: visualizations/blockchain_integration.png")


def generate_all_diagrams():
    # Generate all visualization diagrams
    import os
    os.makedirs('visualizations', exist_ok=True)
    
    print("Generating visualization diagrams...")
    print("-" * 50)
    
    create_dh_exchange_diagram()
    create_mitm_attack_diagram()
    create_authenticated_flow_diagram()
    create_secure_channel_diagram()
    create_blockchain_diagram()
    
    print("-" * 50)
    print("✅ All diagrams generated successfully!")


if __name__ == "__main__":
    generate_all_diagrams()



