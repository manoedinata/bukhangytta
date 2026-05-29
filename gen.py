import os, shutil
from PIL import Image, ImageDraw, ImageFont, JpegImagePlugin, ImageFilter
import json
import math
import re

def draw_text_with_shadow(base_img, text, position, font, text_color="#173679"):
    # 1. Canva Parameters
    angle_deg = -31
    offset_dist = 3  # Scaled down slightly so it doesn't fly off your canvas
    blur_radius = 3   # Pillow blur radius in pixels
    opacity = 35      # 0 to 100 scale
    
    # Calculate exact X and Y pixel offsets using trigonometry
    angle_rad = math.radians(angle_deg)
    # Pillow's Y-axis goes down, so we subtract the Y offset
    x_offset = int(offset_dist * math.cos(angle_rad))
    y_offset = int(offset_dist * math.sin(angle_rad))
    
    # 2. Create a blank transparent layer just for the shadow
    shadow_layer = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_layer)
    
    # Convert 41% opacity to a 0-255 Alpha value
    alpha = int((opacity / 100.0) * 255)
    shadow_color = (0, 0, 0, alpha)
    
    # Draw the shadow text shifted by our calculated offset
    shadow_pos = (position[0] + x_offset, position[1] - y_offset)
    # shadow_draw.text(shadow_pos, text, font=font, fill=shadow_color)
    shadow_draw.text(shadow_pos, text, font=font, fill=shadow_color, stroke_width=0.09, stroke_fill=shadow_color)

    # 3. Apply the Gaussian Blur to the shadow layer
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(blur_radius))
    
    # 4. Paste the blurred shadow onto the main image
    # The third argument acts as a transparency mask
    base_img.paste(shadow_layer, (0, 0), shadow_layer)
    
    # 5. Draw the crisp, main text exactly where it was requested
    main_draw = ImageDraw.Draw(base_img)
    # main_draw.text(position, text, font=font, fill=text_color)
    main_draw.text(position, text, font=font, fill=text_color, stroke_width=0.09, stroke_fill=text_color)

with open("data.json", "r") as f:
    data = json.load(f)
    
# Base coordinates for Student 1
coords = [
    [830, 230], # Nama
    [845, 295], # Nama Panggilan
    [680, 355], # NRP
    [930, 417], # Tempat, Tanggal Lahir
    [750, 483], # Asal Kota
]

global_mhs_idx = 0

def process_images_to_pdf(image_data, output_pdf_path):
    # Tell Python to use the variable defined outside the function
    global global_mhs_idx 
    
    images_for_pdf = []
    my_font = ImageFont.truetype("Montserrat-Regular.ttf", 28)

    for idx, img_path in enumerate(image_data):
        if not os.path.exists(img_path):
            continue
        
        print(f"Processing {img_path}...")

        img = Image.open(img_path)
        if idx > 0: # Skip the first image since it doesn't have text to overlay
            draw = ImageDraw.Draw(img)

            # Loop for the 3 students on this specific page
            for i in range(3):
                # Safety check: Stop if we run out of students in the JSON early
                if global_mhs_idx >= len(data):
                    break
                
                print(f"  Adding text for student {global_mhs_idx + 1} (NRP: {data[global_mhs_idx]['NRP']})")

                # X-Y Gap 
                block_x_offset = [0, 20, 55]
                block_y_offset = [0, 636, 1265]

                keys = ["Nama", "Nama Panggilan", "NRP", "Tempat, Tanggal Lahir", "Asal Kota"]
                
                for idx, text_key in enumerate(keys):
                    base_x = coords[idx][0]
                    base_y = coords[idx][1]
                    
                    # Apply the offset to the base Y coordinate safely
                    actual_x = base_x + block_x_offset[i]
                    actual_y = base_y + block_y_offset[i]

                    # draw.text((base_x, actual_y), data[global_mhs_idx][text_key], fill="#173679", font=my_font)
                    draw_text_with_shadow(
                        base_img=img, 
                        text=data[global_mhs_idx][text_key], 
                        position=(actual_x, actual_y), 
                        font=my_font
                    )

                # Move to the next student in the JSON
                global_mhs_idx += 1

            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')

        images_for_pdf.append(img)

    if images_for_pdf:
        images_for_pdf[0].save(
            output_pdf_path, 
            save_all=True, 
            append_images=images_for_pdf[1:]
        )
        print(f"Success! Created {output_pdf_path} with {len(images_for_pdf)} pages.")
    else:
        print("No images were successfully processed.")

# Copy img/ to processed_img/
# shutil.rmtree("processed_img", ignore_errors=True) 
# shutil.copytree("img", "processed_img", dirs_exist_ok=True)

def extract_number(filename):
    match = re.search(r'\d+', filename)
    return int(match.group()) if match else 0

dir_path = "img"
all_images = [
    os.path.join(dir_path, filename) 
    for filename in sorted(os.listdir(dir_path), key=extract_number) 
    if filename.lower().endswith(('.png', '.jpg', '.jpeg'))
]

process_images_to_pdf(all_images, "merged_output.pdf")