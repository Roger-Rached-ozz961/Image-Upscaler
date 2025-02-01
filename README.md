# Image Upscaler for OSINT Investigation

This Python tool enhances blurry images using upscaling and sharpening techniques, then extracts any readable text via OCR (Optical Character Recognition). Processed images and extracted texts are saved in separate folders for easy access and further analysis.

---

## Features

- **Image Enhancement**: Upscales and sharpens images to make blurry text clearer.
- **OCR Text Extraction**: Uses Tesseract OCR to extract text from the images.
- **Automated Folder Monitoring**: Automatically scans the input folder every 10 seconds and processes any new images.

---

## Requirements

- Python 3.x
- The following Python libraries:
  - `colorama==0.4.6`
  - `numpy==2.2.2`
  - `opencv-python==4.11.0.86`
  - `packaging==24.2`
  - `pillow==11.1.0`
  - `pytesseract==0.3.13`

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Roger-Rached-ozz961/Image-Upscaler.git
   ```

2. Install the required Python libraries:
   ```bash
   pip install colorama==0.4.6 numpy==2.2.2 opencv-python==4.11.0.86 packaging==24.2 pillow==11.1.0 pytesseract==0.3.13
   ```

3. Install Tesseract OCR:
   - For Windows: Download and install from [Tesseract GitHub](https://github.com/tesseract-ocr/tesseract) and set the path to `tesseract.exe` in the script.

---

## Usage

You can run the script in two ways:

1. **Command Line**:  
   Run the script using Python:
   ```bash
   python image-upscaler.py
   ```

2. **Windows (Batch File)**:  
   On Windows, you can double-click the `run.bat` file to run the script.

### Script Workflow:

* The script will continuously monitor the user images to upscale folder for any new images.
* It will upscale the images by a factor of 2, enhance them using a sharpening filter, and save them in the upscaled images folder.
* It will extract text from the upscaled images using Tesseract OCR and save the text in .txt files inside the extracted_texts folder.
* The script will prompt you every 10 seconds to manually trigger the scan or type 'exit' to quit the program.

Example Workflow:

* Place images in the folder user images to upscale.
* Run the script.
* Script processes the images and saves the upscaled images and extracted text in the respective folders.
* Repeat the process every 10 seconds or press 'Enter' to scan images manually.
* 
---

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

---

**Author**: Roger Rached
