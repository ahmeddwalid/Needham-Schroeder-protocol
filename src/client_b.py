from entity import Entity


class ClientB(Entity):
    def step2_respond_to_a(self, id_a, nonce_a):
        nonce_b = self.generate_nonce()
        self.nonces[id_a] = nonce_b
        timestamp_b = self.get_timestamp()

        # Create and encrypt ticket part
        ticket_data = f"{id_a}||{nonce_a}||{timestamp_b}".encode('utf-8')
        encrypted_ticket = self.encrypt(self.key, ticket_data)

        print(f"Step 2: B-->KDC: {self.id} || {nonce_b} || [Encrypted Ticket]")
        return self.id, nonce_b, encrypted_ticket

    def step4_verify_a(self, encrypted_ticket, encrypted_nonce):
        # Decrypt ticket to extract session key
        decrypted_ticket = self.decrypt(self.key, encrypted_ticket).strip()
        parts = decrypted_ticket.split(b'||')

        id_a = parts[0].decode('utf-8')
        session_key_hex = parts[1].decode('utf-8')
        session_key = bytes.fromhex(session_key_hex)  # Convert hex string to bytes
        timestamp = int(parts[2].decode('utf-8'))

        # Verify timestamp is within acceptable range
        current_time = self.get_timestamp()
        if current_time - timestamp > 300:  # 5 minutes
            raise ValueError("Timestamp expired!")

        # Store session key
        self.session_keys[id_a] = session_key

        # Decrypt and verify nonce
        decrypted_nonce = int(self.decrypt(session_key, encrypted_nonce).strip())
        if decrypted_nonce != self.nonces[id_a]:
            raise ValueError("Nonce verification failed!")

        print(f"Step 4: B authenticated A successfully")
        return True

    def future_comm_step2(self, encrypted_ticket, nonce_a):
        # Decrypt ticket to extract session key (this is just for verification)
        decrypted_ticket = self.decrypt(self.key, encrypted_ticket).strip()
        parts = decrypted_ticket.split(b'||')

        id_a = parts[0].decode('utf-8')
        session_key_hex = parts[1].decode('utf-8')
        session_key = bytes.fromhex(session_key_hex)  # Convert hex string to bytes
        timestamp = int(parts[2].decode('utf-8'))

        # Verify timestamp is within acceptable range
        current_time = self.get_timestamp()
        if current_time - timestamp > 300:  # 5 minutes
            raise ValueError("Timestamp expired!")

        # Generate new nonce and encrypt the received nonce
        new_nonce_b = self.generate_nonce()
        self.nonces[f"{id_a}_future"] = new_nonce_b

        encrypted_nonce_a = self.encrypt(session_key, str(nonce_a).encode('utf-8'))

        print(f"Future Communication Step 2: B-->A: {new_nonce_b} || EKs[{nonce_a}]")
        return new_nonce_b, encrypted_nonce_a
