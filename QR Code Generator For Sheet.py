import pandas as pd
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

def find_csv_file():
    for file in os.listdir():
        if file.endswith(".csv"):
            return file
    raise FileNotFoundError("No CSV file found in the current directory.")

# Define the directory to save QR codes
output_dir = "qr_codes"
os.makedirs(output_dir, exist_ok=True)

def generate_qr_code_with_text(data, name, output_path):
    qr = qrcode.QRCode(
        version=1,  # Controls the size of the QR code
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    qr_img = qr.make_image(fill_color="black", back_color="white")

    # Convert QR image to RGB to ensure compatibility with paste
    qr_img = qr_img.convert("RGB")

    # Add text to the QR code image
    qr_width, qr_height = qr_img.size
    img_with_text = Image.new("RGB", (qr_width, qr_height + 50), "white")
    img_with_text.paste(qr_img, (0, 50))

    draw = ImageDraw.Draw(img_with_text)

    # Dynamically adjust font size to fit the text within the image width
    font_size = 20
    font = ImageFont.truetype("arial.ttf", font_size)
    text_width, _ = draw.textbbox((0, 0), name, font=font)[2:]
    while text_width > qr_width and font_size > 10:  # Ensure font size doesn't go below 10
        font_size -= 1
        font = ImageFont.truetype("arial.ttf", font_size)
        text_width, _ = draw.textbbox((0, 0), name, font=font)[2:]

    text_position = ((qr_width - text_width) // 2, 10)  # Center the text at the top
    draw.text(text_position, name, fill="black", font=font)

    img_with_text.save(output_path)

# Find the CSV file
csv_file = find_csv_file()

# Load the CSV file
df = pd.read_csv(csv_file)

# Ensure "QR Code" column exists
df["QR Code"] = ""

# Generate QR codes for each name
for index, row in df.iterrows():
    name = row["Name"]
    qr_code_path = os.path.join(output_dir, f"{name.replace(' ', '_')}_qr.png")
    generate_qr_code_with_text(name, name, qr_code_path)
    df.at[index, "QR Code"] = qr_code_path

# Save the updated CSV
df.to_csv("output.csv", index=False)

print("QR codes with names generated and CSV updated!")
