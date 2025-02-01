import os
import cv2
import sys
import time
import numpy as np
import pytesseract
from colorama import init, Fore

# Initialize Colorama for color printing in terminal
init(autoreset=True)

# Define Bright Colors for Console Output
BRIGHT_GREEN = Fore.LIGHTGREEN_EX
BRIGHT_RED = Fore.LIGHTRED_EX
BRIGHT_CYAN = Fore.LIGHTCYAN_EX  # Cyan for informational text
BRIGHT_YELLOW = Fore.LIGHTYELLOW_EX
BRIGHT_PURPLE = Fore.LIGHTMAGENTA_EX
RESET_COLOR = Fore.RESET

# Define the input folder (where original images are placed) and output folder (where processed images and text will be saved)
INPUT_FOLDER = "user images to upscale"
OUTPUT_FOLDER = "upscaled images"
TEXT_OUTPUT_FOLDER = "extracted_texts"  # Folder for saving extracted text files
PROCESSED_FILES = set()  # Set to track processed files to avoid reprocessing

# Set the path to the Tesseract executable
# For Windows: Update with the correct path to your tesseract.exe
# For Linux/macOS, you typically don’t need to change this if Tesseract is installed globally
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'  # Update with your Tesseract path

def print_banner():
    """
    This function prints the welcome banner to the console to explain the script's purpose.
    """
    banner = """
    ============================================
           Image Upscaler for OSINT Investigation
    ============================================
    Author: Roger Rached
    Description: Clears blurry text in images for OSINT analysis using upscaling and sharpening.
    ============================================
    Usage Instructions:
    1. Place the images you want to process in the folder named 'user images to upscale'.
    2. Run the script, and it will automatically upscale and enhance the images.
    3. The upscaled images will be saved in the 'upscaled images' folder.
    4. Extracted text from images will be saved as text files in the 'extracted_texts' folder.
    5. The program will automatically check for new images every 10 seconds. Press 'Enter' to manually trigger the scan, or type 'exit' to quit the program.
    ============================================
    """
    print(f"{BRIGHT_PURPLE}{banner}{RESET_COLOR}")

def upscaling_image(image_path, scale_factor=2):
    """
    This function upscales and sharpens an image to make blurry text clearer.
    It resizes the image and applies a sharpening kernel.
    """
    image = cv2.imread(image_path)

    if image is None:
        print(f"{BRIGHT_RED}[ERROR] Image not found: {image_path}{RESET_COLOR}")
        return None

    # Resize the image by the given scale factor
    width = int(image.shape[1] * scale_factor)
    height = int(image.shape[0] * scale_factor)
    dim = (width, height)
    
    resized_image = cv2.resize(image, dim, interpolation=cv2.INTER_CUBIC)

    # Apply sharpening kernel to enhance image quality
    sharpening_kernel = np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(resized_image, -1, sharpening_kernel)

    return sharpened_image

def extract_text(image_path):
    """
    This function extracts text from an image using OCR (Optical Character Recognition).
    """
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text.strip()

def process_images():
    """
    This function processes all images in the input folder, upscales them, and extracts text.
    The results (upscaled images and text) are saved to the corresponding output folders.
    """
    print(f"{BRIGHT_CYAN}[INFO] Checking for images in '{INPUT_FOLDER}'...{RESET_COLOR}")

    # Ensure that all required directories exist
    for folder in [OUTPUT_FOLDER, TEXT_OUTPUT_FOLDER, INPUT_FOLDER]:
        if not os.path.exists(folder):
            print(f"{BRIGHT_YELLOW}[INFO] Folder '{folder}' does not exist. Creating it...{RESET_COLOR}")
            os.makedirs(folder)

    # Get all images with supported extensions in the input folder
    images = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not images:
        print(f"{BRIGHT_YELLOW}[INFO] No images found in '{INPUT_FOLDER}'.{RESET_COLOR}")
        return
    
    print(f"{BRIGHT_CYAN}[INFO] Found {len(images)} image(s) to process.{RESET_COLOR}")
    
    for image_name in images:
        try:
            input_path = os.path.join(INPUT_FOLDER, image_name)
            output_path = os.path.join(OUTPUT_FOLDER, image_name)
            
            if os.path.exists(output_path):
                print(f"{BRIGHT_YELLOW}[INFO] Skipping already processed image: {image_name}{RESET_COLOR}")
                continue
            
            print(f"{BRIGHT_CYAN}[INFO] Processing: {image_name}{RESET_COLOR}")
            upscaled_image = upscaling_image(input_path)
            
            if upscaled_image is not None:
                # Save the upscaled image
                cv2.imwrite(output_path, upscaled_image)
                print(f"{BRIGHT_GREEN}[SUCCESS] Saved upscaled image: {output_path}{RESET_COLOR}")
                
                # Extract text and save it to a text file
                extracted_text = extract_text(output_path)
                if extracted_text:
                    # Create and save the extracted text to a .txt file
                    text_file_path = os.path.join(TEXT_OUTPUT_FOLDER, f"{os.path.splitext(image_name)[0]}.txt")
                    with open(text_file_path, 'w') as text_file:
                        text_file.write(extracted_text)
                    print(f"{BRIGHT_GREEN}[INFO] Saved extracted text to: {text_file_path}{RESET_COLOR}")
                else:
                    print(f"{BRIGHT_YELLOW}[INFO] No text extracted from: {image_name}{RESET_COLOR}")
            else:
                print(f"{BRIGHT_RED}[ERROR] Image could not be upscaled: {image_name}{RESET_COLOR}")
        except Exception as e:
            print(f"{BRIGHT_RED}[ERROR] Failed to process image {image_name}: {str(e)}{RESET_COLOR}")

def main():
    """
    This is the main function that will be run when the script is executed.
    It continuously processes images and handles user inputs.
    """
    print_banner()
    try:
        print(f"{BRIGHT_CYAN}[INFO] Starting the script...{RESET_COLOR}")
        
        while True:
            # Ask the user if they want to continue or exit
            user_input = input(f"{BRIGHT_CYAN}[INFO] Press Enter to scan images or type 'exit' to quit: {RESET_COLOR}").strip().lower()
            
            if user_input == "exit":
                print(f"{BRIGHT_PURPLE}[INFO] Exiting program gracefully...{RESET_COLOR}")
                sys.exit(0)
            
            print(f"{BRIGHT_CYAN}[INFO] Scanning for images in '{INPUT_FOLDER}'...{RESET_COLOR}")
            process_images()  # Process all images in the folder
            print(f"{BRIGHT_YELLOW}[INFO] Sleeping for 10 seconds before rescanning...{RESET_COLOR}")
            time.sleep(10)  # Sleep for 10 seconds before rescanning the folder
    
    except KeyboardInterrupt:
        print(f"\n{BRIGHT_PURPLE}[INFO] Program interrupted by user. Exiting gracefully...{RESET_COLOR}")
        sys.exit(0)
    except Exception as e:
        print(f"{BRIGHT_RED}[ERROR] An unexpected error occurred: {str(e)}{RESET_COLOR}")
        sys.exit(1)

if __name__ == "__main__":
    main()
