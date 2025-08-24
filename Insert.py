# imports pillow (PIL)
from PIL import Image
# import other file to get info
import convert
from encode_decode import lfsr_encrypt_decrypt 

# Insertion

# open the image using PIL
# save and show new picture
def put_in_pic(image_path, key1, message, key2, output_path='encoded_image.png'):
    # open the image
    im = Image.open(image_path)
    # convert to RGB 
    im = im.convert('RGB')
    pixels = im.load()
    # gets length of image
    width, height = im.size

    # convert key1 to binary
    key1_bin = convert.stri_binary(key1)
    
    # encrypt message using LFSR with key2
    message_binary_unencrypted = convert.stri_binary(message)
    key2_binary = convert.stri_binary(key2) # Convert key2 to binary for LFSR
    
    encrypted_message_bin = lfsr_encrypt_decrypt(message_binary_unencrypted, key2_binary)

    # lengths to binary
    key1_len_bin = convert.int_binary(len(key1), bits=16) # length of original key1
    msg_len_bin = convert.int_binary(len(message), bits=32) 
    
    # full data is key1 length, message length, key1, message
    full_data = key1_len_bin + msg_len_bin + key1_bin + encrypted_message_bin

    total_bits = len(full_data)
    max_capacity = width * height * 3
    if total_bits > max_capacity:
        raise ValueError(f"Message ({total_bits} bits) is too large to hide in this image (capacity: {max_capacity} bits).")
    
    print(f"Encoding {len(full_data)} bits into image...")
    LSB_encoding(full_data, total_bits, im, pixels)

    # save and show the new image
    im.save(output_path)
    im.show() #automatically opens image
    print(f"Message encoded and image saved as {output_path}")
    return f"Encoding Complete. Encrypted message hidden in '{output_path}'"

# put key length + key message length + message in picture 
def LSB_encoding (full_data, total_bits, im, pixels):
    # gets length of image
    width, height = im.size
    
    data_index = 0
    for y in range(height):
        for x in range(width):
            if data_index >= total_bits:
                break

            r, g, b = pixels[x, y]
            # changes R, G, B channels with data bits if bits left
            r_bin = format(r, '08b')
            g_bin = format(g, '08b')
            b_bin = format(b, '08b')

            # data into LSB of each color channel
            if data_index < total_bits:
                r_bin = r_bin[:-1] + full_data[data_index]
                data_index += 1
            if data_index < total_bits:
                g_bin = g_bin[:-1] + full_data[data_index]
                data_index += 1
            if data_index < total_bits:
                b_bin = b_bin[:-1] + full_data[data_index]
                data_index += 1

            pixels[x, y] = (int(r_bin, 2), int(g_bin, 2), int(b_bin, 2))

        if data_index >= total_bits:
            break



