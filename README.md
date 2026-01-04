# Secure Channel Demo

Cryptography course assignment (University of Macedonia).

The goal of this assignment is to show—step by step—how you go from “two people exchanging keys” to something that looks like a real secure channel:
- what Diffie-Hellman gives you (and what it *doesn’t*)
- how a man-in-the-middle breaks unauthenticated key exchange
- how signatures bind a key to an identity
- how AEAD gives you encrypted messages that also detect tampering

I built it as a small interactive demo (web UI + Python scripts). You can run each phase on its own, see the keys/messages change, and see exactly where Mallory succeeds/fails.

This repo is a small “build-up” demo of a secure channel:
- start with plain Diffie-Hellman
- break it with a MITM
- fix it with signatures
- add AEAD for encrypted messages
- add a Solana-style key registry + show why it helps

### Quick start (recommended)

- **macOS / Linux**:

```bash
bash run.sh
```

- **Windows**:
  - Double-click `run.bat`
  - or run `scripts\run.bat`
  - or run `scripts\run.ps1`

The launcher will:
- create a local virtual environment at `.venv/`
- install dependencies into it (first run only)
- start the Flask backend + open the UI in your browser
- choose a free port automatically (5000, 5001, 5002, …)

### What you’ll see (phases)

- **Phase 1 (X25519 DH)**: Alice/Bob derive the same symmetric key
- **Phase 2 (MITM)**: Mallory swaps keys; Alice and Bob do *not* share a key with each other
- **Phase 3 (Authenticated DH)**: Ed25519 signatures stop the MITM
- **Phase 4 (Secure channel)**: ChaCha20-Poly1305 encrypts messages + detects tampering
- **Phase 5 (Blockchain registry demo)**: a “key registry” idea using Solana-style identities
- **Phase 6 (Blockchain attack attempts)**: Mallory tries a few tricks; registry checks catch them

### Running without the UI (CLI)

Once your `.venv` exists:

```bash
. .venv/bin/activate
python phases/phase1_dh/dh_exchange.py
python phases/phase2_mitm/mallory_attack.py
python phases/phase3_auth/authenticated_dh.py
python phases/phase4_aead/secure_channel.py
python phases/phase5_solana/solana_registry_client.py
python phases/phase6_blockchain_attack/blockchain_mitm_attack.py
```

Run the full walkthrough:

```bash
. .venv/bin/activate
python scripts/demo_all_phases.py
```

### Project layout

- **`backend/`**: Flask server (`backend/app.py`)
- **`frontend/`**: HTML/CSS/JS UI
- **`phases/`**: the phase scripts (1–6)
- **`scripts/`**: launchers + helpers

### Troubleshooting

- **Port in use**: the launcher will auto-pick a free port. If you want a specific one:

```bash
PORT=5050 bash run.sh
```

- **Dependencies**: delete `.venv/` and re-run the launcher to rebuild it.

