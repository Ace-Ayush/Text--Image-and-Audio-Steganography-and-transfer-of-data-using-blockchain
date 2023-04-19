from PIL import Image
import wave
import struct

def encode_text(text, message):
    """
    Encodes a message into a text string by replacing the least significant bit of each character's ASCII code with a bit from the message.
    
    Parameters:
    text (str): The text string to encode the message into.
    message (str): The message to encode into the text string.
    
    Returns:
    str: The encoded text string.
    """
    
    # Convert the message to binary
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    
    # Check if the message is too long to fit in the text string
    if len(binary_message) > len(text)*8:
        raise Exception('Message is too long to encode in the text string.')
    
    # Encode the binary message into the text string
    encoded_text = ''
    index = 0
    for c in text:
        if index < len(binary_message):
            binary_char = format(ord(c), '08b')
            binary_char_new = binary_char[:-1] + binary_message[index]
            encoded_text += chr(int(binary_char_new, 2))
            index += 1
        else:
            encoded_text += c
    
    return encoded_text

def decode_text(text):
    """
    Decodes a message from an encoded text string by extracting the least significant bit of each character's ASCII code.
    
    Parameters:
    text (str): The encoded text string.
    
    Returns:
    str: The decoded message.
    """
    
    # Decode the binary message from the text string
    binary_message = ''
    for c in text:
        binary_char = format(ord(c), '08b')
        binary_message += binary_char[-1]
    
    # Convert the binary message to text
    message = ''
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
    
    return message

def encode_image(image_path, message):
    """
    Encodes a message into an image by replacing the least significant bit of each color channel's pixel value with a bit from the message.
    
    Parameters:
    image_path (str): The path to the image file to encode the message into.
    message (str): The message to encode into the image.
    
    Returns:
    PIL.Image.Image: The encoded image.
    """
    
    # Open the image file
    image = Image.open(image_path)
    
    # Check if the message is too long to fit in the image
    if len(message) > image.size[0]*image.size[1]*3:
        raise Exception('Message is too long to encode in the image.')
    
    # Encode the message into the image
    pixels = image.load()
    index = 0
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]
            if index < len(message):
                r_new = r - (r % 2) + int(message[index])
                index += 1
            else:
                r_new = r - (r % 2)
            if index < len(message):
                g_new = g - (g % 2) + int(message[index])
                index += 1
            else:
                g_new = g - (g % 2)
            if index < len(message):
                b_new = b - (b % 2) + int(message[index])
                index += 1
            else:
                b_new = b
            pixels[i, j] = (r_new, g_new, b_new)
    
    return image

def decode_image(image_path):
    """
    Decodes a message from an encoded image by extracting the least significant bit of each color channel's pixel value.
    
    Parameters:
    image_path (str): The path to the image file to decode the message from.
    
    Returns:
    str: The decoded message.
    """
    
    # Open the image file
    image = Image.open(image_path)
    
    # Decode the message from the image
    pixels = image.load()
    binary_message = ''
    for i in range(image.size[0]):
        for j in range(image.size[1]):
            r, g, b = pixels[i, j]
            binary_message += str(r % 2)
            binary_message += str(g % 2)
            binary_message += str(b % 2)
    
    # Convert the binary message to text
    message = ''
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
    
    return message

def encode_audio(audio_path, message):
    """
    Encodes a message into an audio file by replacing the least significant bit of each sample with a bit from the message.
    
    Parameters:
    audio_path (str): The path to the audio file to encode the message into.
    message (str): The message to encode into the audio file.
    
    Returns:
    None
    """
    
    # Open the audio file
    with wave.open(audio_path, 'rb') as wave_file:
        # Get the sample rate and sample width
        sample_rate = wave_file.getframerate()
        sample_width = wave_file.getsampwidth()
        # Read the audio data
        audio_data = wave_file.readframes(wave_file.getnframes())
    
    # Check if the message is too long to fit in the audio file
    if len(message) > len(audio_data)*8//sample_width:
        raise Exception('Message is too long to encode in the audio file.')
    
    # Encode the message into the audio data
    binary_message = ''.join(format(ord(c), '08b') for c in message)
    audio_data_new = b''
    index = 0
    for i in range(0, len(audio_data), sample_width):
        if index < len(binary_message):
            sample = audio_data[i:i+sample_width]
            sample_new = struct.pack('<h', struct.unpack('<h', sample)[0] - (struct.unpack('<h', sample)[0] % 2) + int(binary_message[index]))
            audio_data_new += sample_new
            index += 1
        else:
            audio_data_new += audio_data[i:i+sample_width]
    
    # Write the encoded audio data to a new file
    with wave.open('encoded_audio.wav', 'wb') as wave_file:
        wave_file.setframerate(sample_rate)
        wave_file.setsampwidth(sample_width)
        wave_file.setnchannels(1)
        wave_file.writeframes(audio_data_new)

def decode_audio(audio_path):
    """
    Decodes a message from an encoded audio file by extracting the least significant bit of each sample.
    
    Parameters:
    audio_path (str): The path to the audio file to decode the message from.
    
    Returns:
    str: The decoded message.
    """
    
    # Open the audio file
    with wave.open(audio_path, 'rb') as wave_file:
        # Get the sample rate and sample width
        sample_rate = wave_file.getframerate()
        sample_width =5000
        # Read the audio data
        audio_data = wave_file.readframes(wave_file.getnframes())
    
    # Decode the message from the audio data
    binary_message = ''
    for i in range(0, len(audio_data), sample_width):
        sample = audio_data[i:i+sample_width]
        binary_message += str(struct.unpack('<h', sample)[0] % 2)
    
    # Convert the binary message to text
    message = ''
    for i in range(0, len(binary_message), 8):
        message += chr(int(binary_message[i:i+8], 2))
    
    return message

def merge(image_path, audio_path, text_path):
    """
    Merges an encoded image, an encoded audio file, and an encoded text file into a single file.
    
    Parameters:
    image_path (str): The path to the encoded image file.
    audio_path (str): The path to the encoded audio file.
    text_path (str): The path to the encoded text file.
    
    Returns:
    None
    """
    
    # Open the encoded image file
    encoded_image = Image.open(image_path)
    
    # Open the encoded audio file
    with wave.open(audio_path, 'rb') as wave_file:
        encoded_audio_data = wave_file.readframes(wave_file.getnframes())
        encoded_audio_sample_rate = wave_file.getframerate()
        encoded_audio_sample_width = wave_file.getsampwidth()
    
    # Open the encoded text file
    with open(text_path, 'rb') as text_file:
        encoded_text = text_file.read()
    
    # Create a new file to store the merged data
    with open('merged_data.bin', 'wb') as merged_file:
        # Write the encoded image data to the file
        encoded_image_data = encoded_image.tobytes()
        merged_file.write(struct.pack('<I', len(encoded_image_data)))
        merged_file.write(encoded_image_data)
        # Write the encoded audio data to the file
        merged_file.write(struct.pack('<I', len(encoded_audio_data)))
        merged_file.write(encoded_audio_data)
        merged_file.write(struct.pack('<I', encoded_audio_sample_rate))
        merged_file.write(struct.pack('<I', encoded_audio_sample_width))
        # Write the encoded text data to the file
        merged_file.write(struct.pack('<I', len(encoded_text)))
        merged_file.write(encoded_text)

def unmerge(merged_path):
    """
    Extracts the encoded image, encoded audio file, and encoded text file from a merged file.
    
    Parameters:
    merged_path (str): The path to the merged file to extract the data from.
    
    Returns:
    None
    """
    
    # Open the merged file
    with open(merged_path, 'rb') as merged_file:
        # Read the encoded image data from the file
        encoded_image_data_length = struct.unpack('<I', merged_file.read(4))[0]
        encoded_image_data = merged_file.read(encoded_image_data_length)
        encoded_image = Image.frombytes('RGB', (100, 100), encoded_image_data)
        # Read the encoded audio data from the file
        encoded_audio_data_length = struct.unpack('<I', merged_file.read(4))[0]
        encoded_audio_data = merged_file.read(encoded_audio_data_length)
        encoded_audio_sample_rate = struct.unpack('<I', merged_file.read(4))[0]
        encoded_audio_sample_width = struct.unpack('<I', merged_file.read(4))[0]
        # Read the encoded text data from the file
        encoded_text_length = struct.unpack('<I', merged_file.read(4))[0]
        encoded_text = merged
        _file.read(encoded_text_length)
    
    # Save the extracted files
    encoded_image.save('unmerged_image.png')
    with wave.open('unmerged_audio.wav', 'wb') as wave_file:
        wave_file.setnchannels(1)
        wave_file.setframerate(encoded_audio_sample_rate)
        wave_file.setsampwidth(encoded_audio_sample_width)
        wave_file.writeframes(encoded_audio_data)
    with open('unmerged_text.txt', 'wb') as text_file:
        text_file.write(encoded_text)

# Example usage
image_path = 'encoded_image.png'
audio_path = 'encoded_audio.wav'
text_path = 'encoded_text.txt'
merge(image_path, audio_path, text_path)
unmerge('merged_data.bin')


"""This code defines three functions: encode_image, encode_audio, and encode_text, for encoding a message into an image file, an audio file, and a text file, respectively. It also defines three corresponding decoding functions: decode_image, decode_audio, and decode_text.

Additionally, it defines a merge function that takes the paths to the encoded image, encoded audio, and encoded text files as arguments, and merges them into a single binary file. This function writes the length of each encoded data block, followed by the actual data, to the merged file.

Finally, it an unmerge function that takes the path to the merged file as an argument, and extracts the encoded image, encoded audio, and encoded text files from the merged file. This function reads the length of each encoded data block, followed by the actual data, from the merged file, and saves each block to a separate file"""