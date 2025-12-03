from PIL import Image, ImageDraw, ImageFont

def draw_bounding_boxes(image: Image.Image, items: list) -> Image.Image:
    """
    Draws bounding boxes and labels on the image.
    Expects items to have 'bbox' in [ymin, xmin, ymax, xmax] normalized (0-1000) format.
    """
    # Create a copy so we don't mutate the original
    img_copy = image.copy()
    draw = ImageDraw.Draw(img_copy)
    width, height = img_copy.size

    # Colors for different items
    colors = ["#FF0000", "#00FF00", "#0000FF", "#FFA500", "#800080"]

    for i, item in enumerate(items):
        name = item.get("name", "Unknown")
        bbox = item.get("bbox", [])
        
        if len(bbox) == 4:
            # Unpack normalized coordinates
            ymin, xmin, ymax, xmax = bbox
            
            # Convert to pixels
            left = (xmin / 1000) * width
            top = (ymin / 1000) * height
            right = (xmax / 1000) * width
            bottom = (ymax / 1000) * height

            color = colors[i % len(colors)]
            
            # Draw the box
            draw.rectangle([left, top, right, bottom], outline=color, width=4)
            
            # Draw the label background
            text_w = len(name) * 10 # Approx width
            draw.rectangle([left, top, left + text_w + 10, top + 20], fill=color)
            
            # Draw the text
            draw.text((left + 5, top + 2), name, fill="white")

    return img_copy