from entity import Entity


class ClientA(Entity):
    def step1_initiate_auth(self, id_B):
        nonce_a = self.generate_nonce()
        self.nonces[id_B] = nonce_a

        print(f"Step 1: A-->B: {self.id} || {nonce_a}")
        return self.id, nonce_a

    def step3_process_kdc_response(self, encrypted_ticket_for_a, encrypted_ticket_for_b, nonce_b):
        # Process KDC response and extract session key
        decrypted_data = self.decrypt(self.key, encrypted_ticket_for_a).strip()
        parts = decrypted_data.split(b'||')

        id_b = parts[0].decode('utf-8')
        nonce_a_received = int(parts[1].decode('utf-8'))
        session_key_hex = parts[2].decode('utf-8')
        session_key = bytes.fromhex(session_key_hex)  # Convert hex string to bytes
        timestamp_b = int(parts[3].decode('utf-8'))

        # Verify nonce
        if nonce_a_received != self.nonces[id_b]:
            raise ValueError("Nonce verification failed!")

        self.session_keys[id_b] = session_key
        self.timestamps[id_b] = timestamp_b

        print(f"Step 3: A received and processed KDC response")
        return encrypted_ticket_for_b, self.encrypt(session_key, str(nonce_b).encode('utf-8'))

    def future_comm_step1(self, id_B):
        # Retrieve existing ticket and generate new nonce
        encrypted_ticket = self.nonces.get(f"{id_B}_ticket")
        new_nonce_a = self.generate_nonce()
        self.nonces[f"{id_B}_future"] = new_nonce_a

        print(f"Future Communication Step 1: A-->B: [Ticket] || {new_nonce_a}")
        return encrypted_ticket, new_nonce_a

    def future_comm_step3(self, id_B, encrypted_nonce_b):
        session_key = self.session_keys[id_B]
        nonce_b = int(self.decrypt(session_key, encrypted_nonce_b).strip())

        # Encrypt nonce_b with session key
        encrypted_response = self.encrypt(session_key, str(nonce_b).encode('utf-8'))

        print(f"Future Communication Step 3: A-->B: EKs[{nonce_b}]")
        return encrypted_response
