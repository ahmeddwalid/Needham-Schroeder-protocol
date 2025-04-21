import os
from client_a import ClientA
from client_b import ClientB
from kdc import KDC


def run_needham_schroeder():
    # Initialize KDC
    kdc = KDC()

    # Initialize entities with their secret keys
    key_a = os.urandom(32)  # 256-bit key
    key_b = os.urandom(32)  # 256-bit key

    alice = ClientA("Alice", key_a)
    bob = ClientB("Bob", key_b)

    # Register entities with KDC
    kdc.register_entity("Alice", key_a)
    kdc.register_entity("Bob", key_b)

    print("\n=== NEEDHAM-SCHROEDER PROTOCOL ===\n")

    # Step 1: A --> B: IDA || Na
    id_a, nonce_a = alice.step1_initiate_auth("Bob")

    # Step 2: B --> KDC: IDB || Nb || EKb[IDA ||Na||Tb]
    id_b, nonce_b, encrypted_ticket = bob.step2_respond_to_a(id_a, nonce_a)

    # Step 3: KDC --> A: EKa[IDB||Na||Ks||Tb] || EKb[IDA||Ks||Tb] ||Nb
    encrypted_ticket_a, encrypted_ticket_b, nonce_b = kdc.process_auth_request(id_b, nonce_b, encrypted_ticket)

    # Store the ticket for future communication
    alice.nonces["Bob_ticket"] = encrypted_ticket_b

    # Step 4: A --> B: EKb[IDA||Ks||Tb] || EKs[Nb]
    ticket_for_b, encrypted_nonce = alice.step3_process_kdc_response(encrypted_ticket_a, encrypted_ticket_b, nonce_b)

    # B verifies A's message
    auth_success = bob.step4_verify_a(ticket_for_b, encrypted_nonce)

    if auth_success:
        print("\n=== MUTUAL AUTHENTICATION SUCCESSFUL! ===\n")

        print("\n=== FUTURE COMMUNICATION ===\n")

        # Future Communication Step 1: A --> B: EKb[IDA||Ks||Tb], N'a
        ticket_for_b, new_nonce_a = alice.future_comm_step1("Bob")

        # Future Communication Step 2: B --> A: N'b, EKs[N'a]
        new_nonce_b, encrypted_nonce_a = bob.future_comm_step2(ticket_for_b, new_nonce_a)

        # Future Communication Step 3: A --> B: EKs[N'b]
        encrypted_nonce_b = alice.future_comm_step3("Bob", encrypted_nonce_a)

        print("\n=== FUTURE COMMUNICATION COMPLETED SUCCESSFULLY! ===\n")
    else:
        print("\n=== AUTHENTICATION FAILED! ===\n")


if __name__ == "__main__":
    run_needham_schroeder()
