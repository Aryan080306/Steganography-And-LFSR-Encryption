# # PUT ALL IN TKINTER 
# from Insert import put_in_pic
# from Extract import extraction

# task = input("Would you like to encode or decode?\n>")
# path = input("Path to image: \n>")
# #inputs
# #normal path: C:\Users\student\Documents\Extra\mountain.png
# # encoded path: C:\Users\student\Documents\Stretch Project\encoded_image.png


# if task == "encode":
#     key1 = input("Key to hide in image: \n> ")
#     keya = input("Key to encrypt message\n> ")  # write it in a .txt file
#     message = input("Whats the secret message? \n> ")
#     # encode message (function)
#     print(put_in_pic(path, key1, message))
#     print("Message hidden!")

# elif task =="decode":
#     try_again = "T"
#     real = False
#     while real == False:
#         key2 = input("Key to get it out of image: \n>")
#         out = extraction(path)
#         key1 = out[0]
#         message = out[1]
#         if key1 != key2:
#             print("You get no secrets today")
#             try_again == input("Would you like to try again? (T/F) \n>")
#             if try_again == "F":
#                 break
#         else:
#             print(f"Extracted Message is: {message}")
#             print("Well done, key one is correct!")
#             # keyb = input("Key to decrypt it") # if it is:
#             # Decode the message (function(message)
#             # print out the secret message

            
            
#             real = True


    
