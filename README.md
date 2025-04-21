<h2 align="center">Networks Security</h2>
<h3 align="center">Needham-Schroeder Protocol Documentation</h3>

## Table of Contents

1. [Project Overview](#project-overview)
2. [Protocol Implementation](#protocol-implementation)
3. [Project Structure](#project-structure)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Implementation Details](#implementation-details)
   - [Entity Base Class](#entity-base-class)
   - [Client A](#client-a)
   - [Client B](#client-b)
   - [Key Distribution Center (KDC)](#key-distribution-center-(kdc))
7. [Future Improvements](#future-improvements)
8. [References](#references)

# About The Project

This project implements the Needham-Schroeder symmetric key authentication protocol in Python. The code is structured in a modular way to make each component of the protocol clear and understandable.

The Needham-Schroeder protocol allows two parties (Alice and Bob) who each share a secret key with a trusted third party (KDC) to establish a secure session between themselves. The protocol consists of the following steps:

# Protocol implementation

### Initial Authentication

1. **A --> B: IDA || Na**
   Alice sends her identity and a fresh nonce (random number) to Bob.

2. **B --> KDC: IDB || Nb || EKb[IDA || Na || Tb]**
   Bob forwards Alice's request to the KDC with his own identity, a fresh nonce, and an encrypted ticket containing Alice's identity, her nonce, and a timestamp.

3. **KDC --> A: EKa[IDB || Na || Ks || Tb] || EKb[IDA || Ks || Tb] || Nb**
   
   The KDC generates a session key (Ks) and sends to Alice:
   
   - A ticket encrypted with Alice's key containing Bob's identity, Alice's nonce, the session key, and the timestamp
   - A ticket encrypted with Bob's key containing Alice's identity, the session key, and the timestamp
   - Bob's nonce

4. **A --> B: EKb[IDA || Ks || Tb] || EKs[Nb]**
   Alice forwards Bob's ticket to him along with Bob's nonce encrypted with the session key to prove she knows the session key.

### Future Communication

Once authenticated, Alice and Bob can use their established session key for subsequent communication:

1. **A --> B: EKb[IDA || Ks || Tb], N'a**
   Alice reuses the encrypted ticket and sends a new nonce.
2. **B --> A: N'b, EKs[N'a]**
   Bob responds with his own new nonce and Alice's nonce encrypted with the session key.
3. **A --> B: EKs[N'b]**
   Alice completes the exchange by encrypting Bob's nonce with the session key.

## Project Structure

The implementation is organized into the following files:

- `entity.py`: Base class with the encryption/decryption functionality
- `client_a.py`: Implementation of Client A (Alice, the initiator)
- `client_b.py`: Implementation of Client B (Bob, the responder)
- `kdc.py`: Implementation of the Key Distribution Center
- `main.py`: Main script to run the demonstration
- `requirements.txt`: Dependencies required for the project

## Installation

### Prerequisites

- Python 3 or higher
- pip package manager

### Setup

1. Clone the repository and enter the directory:
   
   ```bash
   git clone https://github.com/ahmeddwalid/Needham-Schroeder-protocol.git
   cd Needham-Schroeder-protocol
   ```

2. Install the required dependencies:
   
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the demonstration script to see the protocol in action:

```
python main.py
```

This will execute the Two-Way authentication of the Needham-Schroeder protocol, showing both the initial authentication and a future communication exchange.

#### Runing `main.py`

1. Sets up Alice, Bob, and the KDC with appropriate keys
2. Steps through the initial authentication protocol
3. Demonstrates subsequent authenticated communication
4. Verifies successful completion at each step

### Output

```
=== NEEDHAM-SCHROEDER PROTOCOL ===

Step 1: A→B: Alice || 5905722
Step 2: B→KDC: Bob || 3370553 || [Encrypted Ticket]
KDC processed authentication request and generated session key
Step 3: A received and processed KDC response
Step 4: B authenticated A successfully

=== MUTUAL AUTHENTICATION SUCCESSFUL! ===


=== FUTURE COMMUNICATION ===

Future Communication Step 1: A→B: [Ticket] || 1603302
Future Communication Step 2: B→A: 3951118 || EKs[1603302]
Future Communication Step 3: A→B: EKs[1603302]

=== FUTURE COMMUNICATION COMPLETED SUCCESSFULLY! ===
```

## Implementation Details

### Entity Base Class

The **Entity** class in `entity.py` provides fundamental cryptographic operations and utilities used by all participants in the protocol:

- **Encryption**: AES-256 in CBC mode with proper padding
- **Decryption**: Handling of encrypted data with IV extraction and padding verification
- **Nonce Generation**: Creation of random values for challenge-response
- **Timestamp Generation**: For freshness verification

### Client A

- **step1_initiate_auth**: Initiates authentication by generating a nonce
- **step3_process_kdc_response**: Processes the KDC's response, verifies nonces, and extracts the session key
- **future_comm_step1**: Initiates future communication using the stored ticket
- **future_comm_step3**: Completes the future communication by responding to Bob's challenge

### Client B

- **step2_respond_to_a**: Responds to Alice's authentication request by creating a ticket for the KDC
- **step4_verify_a**: Verifies Alice's authentication message, extracts the session key
- **future_comm_step2**: Responds to Alice's future communication request with a challenge

### Key Distribution Center (KDC)

- **register_entity**: Registers entities and their secret keys
- **process_auth_request**: Processes authentication requests, generates session keys, and creates encrypted tickets

## Future Improvements

1. **Enhanced Error Handling**: More robust error handling for network failures, malformed messages, etc.
2. **Logging**: Better logging for debugging and audit purposes
3. **Improved Security**: Additional security measures like:
   - More secure nonce generation
   - Advanced replay attack prevention
   - Public key cryptography variant (Needham-Schroeder-Lowe protocol)
4. **Realistic Network Simulation**: Currently communication is run in memory
5. **Unit Tests**: Comprehensive test suite to verify protocol correctness
6. **GUI Interface**: A graphical representation of the protocol steps

## References

1. Needham, R. M., & Schroeder, M. D. (1978). "Using encryption for authentication in large networks of computers." Communications of the ACM, 21(12), 993-999.
2. Anderson, R. (2020). "Security Engineering: A Guide to Building Dependable Distributed Systems." 3rd Edition.
3. Ferguson, N., Schneier, B., & Kohno, T. (2010). "Cryptography Engineering: Design Principles and Practical Applications."
4. Menezes, A. J., Van Oorschot, P. C., & Vanstone, S. A. (1996). "**Handbook of Applied Cryptography.**"
5. [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/en/latest/)

# License

This project is distributed under the [Apache 2.0 license](https://choosealicense.com/licenses/apache-2.0/). See
[```LICENSE.txt```](/LICENSE) for more information.

<p align="right">(<a href="#top">back to top</a>)</p>
