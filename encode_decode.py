import convert

def lfsr_encrypt_decrypt(data_binary, key2_binary):
    """
    encrypts and decrypts binary data using a LSFR. 
    Since LFSR-based stream ciphers are symmetric, the same function can be used for
    both encryption and decryption.

    Args:
        data_binary (str): The binary string to be encrypted/decrypted.
        key2_binary (str): The binary string representing the LFSR key (seed).

    Returns:
        str: The encrypted/decrypted binary string.
    """
    if not key2_binary:
        raise ValueError("LFSR key (key2) cannot be empty.")

    # converts key2 to a list of integers (0 or 1)
    # key will be the begining state of the LFSR
    lfsr_state = [int(bit) for bit in key2_binary]
    
    # length of the LFSR (equal to the key length)
    lfsr_length = len(lfsr_state)


    # define the taps for the LFSR 
    taps = {}
    if lfsr_length == 8:
        taps = {8: 1} # x^8 + x^4 + x^3 + x^2 + 1 (8-bit LFSR) is x^8 + x^4 + x^3 + x^2 + x^0
        taps = {8: 1, 4:1, 3:1, 2:1} # x^8 + x^4 + x^3 + x^2 + 1
    elif lfsr_length == 16:
        taps = {16: 1, 15: 1, 13: 1, 4: 1} # x^16 + x^15 + x^13 + x^4 + 1
    elif lfsr_length == 32:
        taps = {32: 1, 22: 1, 2: 1, 1: 1} # x^32 + x^22 + x^2 + x^1 + 1 (32-bit)
    elif lfsr_length == 64:
        taps = {64: 1, 63: 1, 61: 1, 60: 1} # x^64 + x^63 + x^61 + x^60 + 1 (64-bit)
    else:
        # if the key length isn't covered, it will use a default or raise an error
        if lfsr_length > 1:
            taps = {lfsr_length: 1, 1: 1} # x^n + x^1 + 1 
        else:
            raise ValueError("LFSR key (key2) is too short. Minimum length is 2 bits.")

    keystream = []
    # keystream bits for the length of the data
    for _ in range(len(data_binary)):
        # gets the output bit (the last bit in state)
        output_bit = lfsr_state[-1]
        keystream.append(str(output_bit))

        # calculate new feedback bit
        feedback_bit = 0
        for tap_pos in taps:
            if tap_pos <= lfsr_length: # tap position is within the LFSR state
                feedback_bit ^= lfsr_state[lfsr_length - tap_pos] # XOR sum of tapped bits
        
        # shift the LFSR state
        lfsr_state = [feedback_bit] + lfsr_state[:-1]

    # XOR the data with the keystream
    encrypted_decrypted_binary = ""
    for i in range(len(data_binary)):
        encrypted_decrypted_binary += str(int(data_binary[i]) ^ int(keystream[i]))

    return encrypted_decrypted_binary


