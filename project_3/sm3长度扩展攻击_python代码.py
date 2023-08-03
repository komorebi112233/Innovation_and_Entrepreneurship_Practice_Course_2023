import struct
import hashlib

def sm3_padding(data):
    ml = len(data) * 8
    padding = b'\x80'
    padding += b'\x00' * ((56 - (len(data) + 1) % 64) % 64)
    padding += struct.pack('>Q', ml)
    return padding

def sm3_hash(message):
    hash = hashlib.new('sm3')
    hash.update(message)
    return hash.digest()

def sm3_length_extension_attack(original_message, original_hash, extension_data):
    padding = sm3_padding(original_message)
    ml = len(original_message) * 8
    state = struct.unpack('>IIIIIIII', original_hash)

    # Update the internal state with the padding and length of the original message
    hash = hashlib.new('sm3')
    hash.update(padding)
    state = list(struct.unpack('>IIIIIIII', hash.digest()))
    state[0] = state[0] ^ 0x7380166f
    state[1] = state[1] ^ 0x4914b2b9
    state[2] = state[2] ^ 0x172442d7
    state[3] = state[3] ^ 0xda8a0600
    state[4] = state[4] ^ 0xa96f30bc
    state[5] = state[5] ^ 0x163138aa
    state[6] = state[6] ^ 0xe38dee4d
    state[7] = state[7] ^ 0xb0fb0e4e

    # Update the internal state with the extension data
    hash = hashlib.new('sm3')
    hash.update(extension_data)
    state_extension = list(struct.unpack('>IIIIIIII', hash.digest()))

    # Calculate the new hash value
    new_hash = struct.pack('>IIIIIIII', state[0] ^ state_extension[0],
                           state[1] ^ state_extension[1],
                           state[2] ^ state_extension[2],
                           state[3] ^ state_extension[3],
                           state[4] ^ state_extension[4],
                           state[5] ^ state_extension[5],
                           state[6] ^ state_extension[6],
                           state[7] ^ state_extension[7])

    return new_hash

# Original message and its hash
original_message = b'Original Message'
original_hash = sm3_hash(original_message)

# Extension data
extension_data = b'Extension Data'

# Perform the length extension attack
new_hash = sm3_length_extension_attack(original_message, original_hash, extension_data)

print("Original Hash:", original_hash.hex())
print("New Hash:", new_hash.hex())
