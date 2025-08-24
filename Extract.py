# imports pillow (PIL)
from PIL import Image
# import other file to get info
import convert 

# extract key and message (binary data) out of the image

def extraction(path):
    im = Image.open(path, 'r')  # opens image
    im = im.convert('RGB')       # pixels values to the RGB ones in that pixel
    pixels = list(im.getdata()) # gets all the pixels in the picture

    # get LSBs by loop through each pixel in the pic
    bits = ''
    for pixel in pixels:
        for channel in pixel:  # R,G,B
            bits += bin(channel)[-1]  # get the LSB

    # get actual binary for lengths
    key1_len_binary = bits[:16]
    mesg_len_binary = bits[16:48]

    key1_len = int(key1_len_binary, 2)
    message_len = int(mesg_len_binary, 2)

    print(f"Key 1 length: {key1_len} characters")
    print(f"Message length: {message_len} characters (original unencrypted)")
    
    # first 48bits are the lengths, key=16, message-32 so start at 48
    start = 48    

    # 48 + number of bits to read for key and message
    end_key1 = start + key1_len * 8     # each character is 8 bits
    end_msg = end_key1 + message_len * 8 # each character of original message is 8 bits

    # check if we have enough bits
    if len(bits) < end_msg:
        raise ValueError("Not enough hidden data in the image to extract the full message. Image might be corrupted or not properly encoded.")
    
    # gets the actual binary bits of key and message
    key1_bits = bits[start:end_key1]
    encrypted_msg_bits = bits[end_key1:end_msg] # This is the *encrypted* message in binary

    # turn the binary to string for key1 (access key)
    retrieved_key1 = convert.binary_stri(key1_bits)
    
    # returns key1 as string and the encrypted message as its binary string
    return retrieved_key1, encrypted_msg_bits

