from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

def design_battlecard(battlecard_data: dict) -> BytesIO:
    try:
        # Create a new image with a white background
        width, height = 800, 1200
        img = Image.new('RGB', (width, height), 'white')
        draw = ImageDraw.Draw(img)

        # Load fonts
        try:
            font_title = ImageFont.truetype("arial.ttf", 24)
            font_header = ImageFont.truetype("arial.ttf", 18)
            font_text = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            font_title = ImageFont.load_default()
            font_header = ImageFont.load_default()
            font_text = ImageFont.load_default()

        # Define margins and starting y position
        margin_x = 50
        y = 50

        # Title section
        title = "Battlecard"
        draw.text((margin_x, y), title, font=font_title, fill="black")
        y += 40

        # Competitors Section
        header_competitors = "Competitors"
        draw.text((margin_x, y), header_competitors, font=font_header, fill="black")
        y += 30

        # Competitors content
        for competitor in battlecard_data.get('competitors', []):
            draw.text((margin_x + 20, y), f"Name: {competitor.get('name', 'N/A')}", fill="black", font=font_text)
            y += 20
            draw.text((margin_x + 40, y), f"Strengths: {competitor.get('strengths', 'N/A')}", fill="black", font=font_text)
            y += 20
            draw.text((margin_x + 40, y), f"Weaknesses: {competitor.get('weaknesses', 'N/A')}", fill="black", font=font_text)
            y += 30

        # Product Information Section
        header_product_info = "Product Information"
        draw.text((margin_x, y), header_product_info, font=font_header, fill="black")
        y += 30

        product_info = battlecard_data.get('product_info', {}).get('comparison_text', 'N/A')
        draw.text((margin_x + 20, y), product_info, fill="black", font=font_text)
        y += 40

        # Draw a divider line
        draw.line([(margin_x, y), (width - margin_x, y)], fill="black", width=2)
        y += 20

        # Save the image to a BytesIO buffer as PDF
        buffer = BytesIO()
        img.save(buffer, format="PDF")
        buffer.seek(0)  # Reset the buffer pointer to the beginning

        return buffer

    except Exception as e:
        print(f"Error in design_battlecard: {e}")
        raise e
