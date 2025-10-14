from PIL import Image, ImageDraw, ImageFont
import os

def resize_and_crop_to_png(
    input_path: str,
    output_path: str,
    target_width: int,
    target_height: int,
    align_horizontal: str = "center",  # 'left', 'center', 'right'
    align_vertical: str = "center",    # 'top', 'center', 'bottom'
):
    """
    Resize a PNG or JPG image so that the smallest dimension fits exactly,
    then crop the other dimension to the target size.
    The result is saved as a PNG file.
    
    Parameters:
        input_path (str): Path to the source image (.png or .jpg)
        output_path (str): Path to save the resulting .png file
        target_width (int): Desired output width in pixels
        target_height (int): Desired output height in pixels
        align_horizontal (str): 'left', 'center', or 'right'
        align_vertical (str): 'top', 'center', or 'bottom'
    """
    # --- Load and prepare image ---
    img = Image.open(input_path).convert("RGBA")

    src_width, src_height = img.size
    target_ratio = target_width / target_height
    src_ratio = src_width / src_height

    # --- Resize so the smallest dimension fits exactly ---
    if src_ratio > target_ratio:
        # Source is wider than target → fit by height
        new_height = target_height
        new_width = int(src_ratio * target_height)
    else:
        # Source is taller → fit by width
        new_width = target_width
        new_height = int(target_width / src_ratio)

    resized = img.resize((new_width, new_height), Image.LANCZOS)

    # --- Determine cropping box based on alignment ---
    if align_horizontal == "left":
        left = 0
    elif align_horizontal == "right":
        left = new_width - target_width
    else:  # center
        left = (new_width - target_width) // 2

    if align_vertical == "top":
        top = 0
    elif align_vertical == "bottom":
        top = new_height - target_height
    else:  # center
        top = (new_height - target_height) // 2

    right = left + target_width
    bottom = top + target_height

    cropped = resized.crop((left, top, right, bottom))

    # --- Save as PNG ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cropped.save(output_path, format="PNG", optimize=True)

    return output_path

def overlay_png(base_path: str, overlay_path: str, output_path: str, opacity: float = 1.0):
    """
    Overlay one PNG image on top of another and save the result as a PNG.
    Both images must have the same dimensions.

    Parameters:
        base_path (str): Path to the bottom/base PNG image.
        overlay_path (str): Path to the top/overlay PNG image.
        output_path (str): Path to save the final composited PNG.
        opacity (float): Opacity of the overlay image (0.0 to 1.0).
    """
    # --- Load both images ---
    base = Image.open(base_path).convert("RGBA")
    overlay = Image.open(overlay_path).convert("RGBA")

    # --- Verify sizes match ---
    if base.size != overlay.size:
        raise ValueError(
            f"Image sizes do not match: base={base.size}, overlay={overlay.size}"
        )

    # --- Apply opacity to overlay (if < 1.0) ---
    if opacity < 1.0:
        # Split channels and adjust alpha
        r, g, b, a = overlay.split()
        a = a.point(lambda p: int(p * opacity))
        overlay = Image.merge("RGBA", (r, g, b, a))

    # --- Composite images ---
    combined = Image.alpha_composite(base, overlay)

    # --- Save result ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    combined.save(output_path, format="PNG", optimize=True)

    return output_path

def add_text_to_image(
    input_path: str,
    output_path: str,
    text: str,
    font_path: str,
    font_size: int = 40,
    position: tuple = (0, 0),
    color: tuple = (255, 255, 255),
    bold: bool = False,
    italic: bool = False,
    border_width: int = 0,
    border_color: tuple = (0, 0, 0),
    max_width: int = None,
    align: str = "left",  # 'left', 'center', 'right'
    treat_as_names: bool = False,
):
    """
    Adds text to an image with optional wrapping, alignment, and bullet-style name formatting.

    Parameters:
        input_path (str): Source image path.
        output_path (str): Destination path.
        text (str): Text or comma-separated list of names.
        font_path (str): Path to .ttf or .otf font file.
        font_size (int): Font size in points.
        position (tuple): (x, y) coordinates of upper-left corner.
        color (tuple): RGB color for text.
        bold (bool): Use bold variant if available.
        italic (bool): Use italic variant if available.
        border_width (int): Width of text outline.
        border_color (tuple): RGB color for outline.
        max_width (int): Max text width in pixels for wrapping.
        align (str): 'left', 'center', or 'right'.
        treat_as_names (bool): If True, interpret text as comma-separated names.
    """
    # --- Load image ---
    img = Image.open(input_path).convert("RGBA")
    draw = ImageDraw.Draw(img)

    # --- Choose font variant ---
    font_file = font_path
    if bold and "Bold" not in font_file and os.path.exists(font_path.replace(".ttf", "-Bold.ttf")):
        font_file = font_path.replace(".ttf", "-Bold.ttf")
    if italic and "Italic" not in font_file and os.path.exists(font_path.replace(".ttf", "-Italic.ttf")):
        font_file = font_path.replace(".ttf", "-Italic.ttf")

    try:
        font = ImageFont.truetype(font_file, font_size)
    except Exception as e:
        raise RuntimeError(f"Could not load font '{font_file}': {e}")

    x, y = position

    # --- Handle name list case ---
    if treat_as_names:
        # Split names, clean whitespace
        names = [name.strip() for name in text.split(",") if name.strip()]
        lines = []
        current_line = ""
        for i, name in enumerate(names):
            candidate = (current_line + " • " + name).strip(" •") if current_line else name
            width = draw.textlength(candidate, font=font)
            if max_width and width > max_width and current_line:
                lines.append(current_line.strip(" •"))
                current_line = name
            else:
                current_line = candidate
        if current_line:
            lines.append(current_line.strip(" •"))
    else:
        # --- Normal wrapping logic ---
        if max_width:
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                test_line = (current_line + " " + word).strip()
                width = draw.textlength(test_line, font=font)
                if width > max_width and current_line:
                    lines.append(current_line)
                    current_line = word
                else:
                    current_line = test_line
            if current_line:
                lines.append(current_line)
        else:
            lines = text.split("\n")

    # --- Draw lines ---
    line_height = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    for line in lines:
        line_width = draw.textlength(line, font=font)

        # Horizontal alignment
        if align == "center":
            line_x = x + (max_width - line_width) / 2 if max_width else x
        elif align == "right":
            line_x = x + (max_width - line_width) if max_width else x
        else:
            line_x = x

        # Draw border if requested
        if border_width > 0:
            for dx in range(-border_width, border_width + 1):
                for dy in range(-border_width, border_width + 1):
                    if dx != 0 or dy != 0:
                        draw.text((line_x + dx, y + dy), line, font=font, fill=border_color)

        # Draw main text
        draw.text((line_x, y), line, font=font, fill=color)
        y += line_height

    # --- Save output ---
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    img.save(output_path, format="PNG", optimize=True)
    return output_path
