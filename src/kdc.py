import os
from entity import Entity


class KDC(Entity):
    def __init__(self):
        self.entity_keys = {}  # Dictionary to store each entity's key

    def register_entity(self, entity_id, key):
        self.entity_keys[entity_id] = key

    def process_auth_request(self, id_b, nonce_b, encrypted_ticket):
        key_b = self.entity_keys[id_b]

        # Decrypt the ticket
        decrypted_ticket = self.decrypt(key_b, encrypted_ticket).strip()
        parts = decrypted_ticket.split(b'||')

        id_a = parts[0].decode('utf-8')
        nonce_a = int(parts[1].decode('utf-8'))
        timestamp_b = int(parts[2].decode('utf-8'))

        # Get A's key
        key_a = self.entity_keys[id_a]

        # Generate session key
        session_key = os.urandom(32)  # 256-bit key
        session_key_hex = session_key.hex()  # Convert to hex string for transmission

        # Create ticket for A
        ticket_a_data = f"{id_b}||{nonce_a}||{session_key_hex}||{timestamp_b}".encode('utf-8')
        encrypted_ticket_a = self.encrypt(key_a, ticket_a_data)

        # Create ticket for B
        ticket_b_data = f"{id_a}||{session_key_hex}||{timestamp_b}".encode('utf-8')
        encrypted_ticket_b = self.encrypt(key_b, ticket_b_data)

        print(f"KDC processed authentication request and generated session key")
        return encrypted_ticket_a, encrypted_ticket_b, nonce_b
