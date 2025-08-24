import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from Insert import put_in_pic
from Extract import extraction
import convert 
from encode_decode import lfsr_encrypt_decrypt 

class SteganographyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Steganography Tool")
        self.root.geometry("600x600") 
        self.root.configure(bg='LightCyan3')
        self.image_path = ""
        self.encrypted_message_binary = "" # stores the encrypted binary message

        # image upload
        self.upload_btn = ttk.Button(root, text="Upload Image", command=self.upload_image)
        self.upload_btn.pack(pady=10) 

        self.image_label = ttk.Label(root, text="No image selected.")
        self.image_label.pack(pady=5)

        # message entry
        ttk.Label(root, text="Secret Message:").pack(pady=5)
        self.message_text = tk.Text(root, height=3, width=60)
        self.message_text.pack(pady=5)

        # keys entry 
        ttk.Label(root, text="Key 1 (Access Key):").pack(pady=5)
        self.key1_entry = ttk.Entry(root, show="*")
        self.key1_entry.pack(pady=5)

        ttk.Label(root, text="Key 2 (Encryption Key):").pack(pady=5)
        self.key2_entry = ttk.Entry(root, show="*")
        self.key2_entry.pack(pady=5)

        # buttons for encode/decode
        button_frame = ttk.Frame(root)
        button_frame.pack(pady=10)

        self.insert_btn = ttk.Button(button_frame, text="Hide Encrypted Message", command=self.insert_message_with_encryption)
        self.insert_btn.grid(row=0, column=0, padx=10)

        self.extract_btn = ttk.Button(button_frame, text="Extract and Decrypt Message", command=self.extract_and_decrypt_message)
        self.extract_btn.grid(row=0, column=1, padx=10)

        # buttons for encrypt/decrypt 
        encryption_button_frame = ttk.Frame(root)
        encryption_button_frame.pack(pady=10)

        self.encrypt_btn = ttk.Button(encryption_button_frame, text="Encrypt Message (Show Only)", command=self.encrypt_message_show)
        self.encrypt_btn.grid(row=0, column=0, padx=10)

        self.decrypt_btn = ttk.Button(encryption_button_frame, text="Decrypt Message (Show Only)", command=self.decrypt_message_show)
        self.decrypt_btn.grid(row=0, column=1, padx=10)


        # output area
        ttk.Label(root, text="Output:").pack(pady=5)
        self.output_text = tk.Text(root, height=5, width=60, state="disabled")
        self.output_text.pack(pady=5)

    def upload_image(self):
        path = filedialog.askopenfilename(filetypes=[("PNG Images", "*.png"), ("All Files", "*.*")])
        if path:
            self.image_path = path
            self.image_label.config(text=f"Image: {path.split('/')[-1]}")
        else:
            self.image_label.config(text="No image selected.")

    def show_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state="disabled")

    def encrypt_message_show(self):
        message = self.message_text.get("1.0", "end").strip()
        key2 = self.key2_entry.get().strip()

        if not message or not key2:
            self.show_output("Please enter both the message and Key 2 to encrypt.")
            return

        try:
            message_binary = convert.stri_binary(message)
            key2_binary = convert.stri_binary(key2)
            self.encrypted_message_binary = lfsr_encrypt_decrypt(message_binary, key2_binary)
            encrypted_message_text = convert.binary_stri(self.encrypted_message_binary)
            self.show_output(f"Original Message: {message}\nEncrypted (binary): {self.encrypted_message_binary}\nEncrypted (text preview): {encrypted_message_text}")
            messagebox.showinfo("Encryption Successful", "Message encrypted. Note: This only shows the encrypted text, it's not hidden in an image yet.")
        except Exception as e:
            self.show_output(f"Encryption Error: {str(e)}")


    def decrypt_message_show(self):
        # demonstrating decryption of an already encrypted message
        # for actual extraction, use extract_and_decrypt_message
        if not self.encrypted_message_binary:
            self.show_output("No encrypted message available to decrypt. Please encrypt one first.")
            return

        key2 = self.key2_entry.get().strip()
        if not key2:
            self.show_output("Please enter Key 2 to decrypt.")
            return

        try:
            key2_binary = convert.stri_binary(key2)
            decrypted_binary = lfsr_encrypt_decrypt(self.encrypted_message_binary, key2_binary)
            decrypted_message = convert.binary_stri(decrypted_binary)
            self.show_output(f"Encrypted (binary): {self.encrypted_message_binary}\nDecrypted Message: {decrypted_message}")
            messagebox.showinfo("Decryption Successful", "Message decrypted.")
        except Exception as e:
            self.show_output(f"Decryption Error: {str(e)}")


    def insert_message_with_encryption(self):
        if not self.image_path:
            self.show_output("Please upload an image first.")
            return

        key1 = self.key1_entry.get().strip()
        message = self.message_text.get("1.0", "end").strip()
        key2 = self.key2_entry.get().strip()

        if not key1 or not message or not key2:
            self.show_output("Please enter Key 1, the message, and Key 2.")
            return

        try:
            #encrypts the message using LFSR with key2
            message_binary = convert.stri_binary(message)
            key2_binary = convert.stri_binary(key2)
            encrypted_message_binary = lfsr_encrypt_decrypt(message_binary, key2_binary)

            # hide the encrypted message and key1 in the image
            result = put_in_pic(self.image_path, key1, message, key2) # key2 to put_in_pic
            self.show_output(result)
            messagebox.showinfo("Success", "Message encrypted and hidden!")
        except Exception as e:
            self.show_output(f"Error hiding message: {str(e)}")

    def extract_and_decrypt_message(self):
        if not self.image_path:
            self.show_output("Please upload an image first.")
            return

        entered_key1 = self.key1_entry.get().strip()
        entered_key2 = self.key2_entry.get().strip() # get key2 for decryption

        if not entered_key1 or not entered_key2:
            self.show_output("Please enter both Key 1 and Key 2 to extract and decrypt.")
            return
        
        try:
            # extracts key1 and the encrypted message from the image
            retrieved_key1, encrypted_message_binary_from_img = extraction(self.image_path)

            # check if Key 1 is right
            if retrieved_key1 != entered_key1:
                self.show_output("Wrong Key 1. Message cannot be retrieved.")
                messagebox.showerror("Error", "Wrong Key 1. Message cannot be retrieved.")
                return

            # decrypt the extracted message using LFSR with Key 2
            entered_key2_binary = convert.stri_binary(entered_key2)
            decrypted_message_binary = lfsr_encrypt_decrypt(encrypted_message_binary_from_img, entered_key2_binary)
            final_message = convert.binary_stri(decrypted_message_binary)

            self.show_output(f"Correct Key 1! Secret Message: {final_message}")
            messagebox.showinfo("Success", f"Message retrieved and decrypted: {final_message}")

        except ValueError as ve:
            self.show_output(f"Error during extraction or decryption: {str(ve)}")
            messagebox.showerror("Extraction/Decryption Error", str(ve))
        except Exception as e:
            self.show_output(f"An unexpected error occurred: {str(e)}")
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = SteganographyApp(root)
    root.mainloop()



