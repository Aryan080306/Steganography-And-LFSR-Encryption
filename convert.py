# string to binary
def stri_binary(string):
    binary = ''
    for char in string:
        # convert each character to its 8-bit binary representation
        binary += format(ord(char), '08b')
    return binary


# binary (from pic) to string
def binary_stri(binary):
    chars = []
    for i in range(0, len(binary), 8):         # move through the binary in chunks of 8
        byte = binary[i:i+8]                   #  slices 8 bits at a time
        chars.append(chr(int(byte, 2)))        # int() converts to an integer
    return ''.join(chars)                      # merges the chars list into one string 



# interger to binary 
def int_binary(n, bits = 8):
    return format(n, f'0{bits}b')

