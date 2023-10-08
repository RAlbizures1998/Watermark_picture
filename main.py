import streamlit as st
from io import BytesIO
from PIL import Image,ImageColor
import numpy as np


def add_watermark(image_path, watermark_path, position, reshape_factor, transparent_factor,recolor,rotate,main_image_rotation):
	# OPEN IMAGE AND WATERMARK
	layer1 = Image.open(image_path).convert('RGBA')
	layer2 = Image.open(watermark_path).convert('RGBA')
	# SET NEW SIZE FOR WATERMARK USING MULTIPLYING FACTOR
	layer1 = layer1.rotate(float(main_image_rotation),expand=True)
	layer2_new_size = (int(layer2.size[0]*reshape_factor), int(layer2.size[1]*reshape_factor))
	layer2_reshape = layer2.resize(layer2_new_size)

	# SAVE INTO LIST SIZES OF IMAGE AND WATERMARK
	shapes = [layer1.size, layer2_reshape.size]
	# GIVEN WATERMARK POSITION, CALCULATE THE LOCATION IN THE MAIN IMAGE
	coordinates = (0, 0)
	if position == "ul":
		coordinates = (0, 0)
	elif position == "ur":
		coordinates = (shapes[0][0]-shapes[1][0], 0)
	elif position == "uc":
		coordinates = (int(shapes[0][0]/2)-int(shapes[1][0]/2), 0)
	elif position == "ll":
		coordinates = (0, shapes[0][1]-shapes[1][1])
	elif position == "lc":
		coordinates = (shapes[0][0]-shapes[1][0], int(shapes[0][1]/2)-int(shapes[1][1]/2))
	elif position == "lr":
		coordinates = (shapes[0][0]-shapes[1][0], shapes[0][1]-shapes[1][1])
	elif position == "c":
		coordinates = (int(shapes[0][0]/2)-int(shapes[1][0]/2), int(shapes[0][1]/2)-int(shapes[1][1]/2))

	layer2_reshape = layer2_reshape.rotate(rotate, expand=True)
	if recolor:
		# Get the size of the image
		width, height = layer2_reshape.size
		# Iterate over each pixel in the image
		for x in range(width):
			for y in range(height):
				# Get the RGB values of the current pixel
				pixel_color = layer2_reshape.getpixel((x, y))

				# Check if all RGB values are greater than 10
				if any(value >= 10 for value in pixel_color):
					# Replace the color with the new color
					layer2_reshape.putpixel((x, y), new_color)
	# CREATE CANVAS FROM IMAGE
	# Make all opaque pixels into semi-opaque
	a = layer2_reshape.getchannel('A')
	new_a = a.point(lambda i: int(255*transparent_factor) if i > 1 else 0)
	layer2_reshape.putalpha(new_a)
	canvas = Image.new("RGBA", layer1.size)
	# INSERT INTO CANVAS WATERMARK AT DESIRED POSITION
	canvas.paste(layer2_reshape, coordinates, layer2_reshape)
	# INSERT INTO IMAGE THE WATERMARK
	layer1.paste(canvas, (0, 0), mask=canvas)
	st.write("Image preview")
	return layer1
pos = {
	'upper left corner': 'ul',
	'upper right corner': 'ur',
	'center': 'c',
	'lower left corner': 'll',
	'lower right corner': 'lr'
}
st.title("Watermark adder")
photo = st.file_uploader("Insert picture",accept_multiple_files=False)
watermark = st.file_uploader("Insert the watermark")
n1,n2 = st.columns(2)
if watermark is not None:
	with n1:
		reshape_factor = st.text_input("Image reshape factor",1)
		transparent_factor = st.select_slider("Transparency factor",np.arange(0.05,1.05,0.05).round(2),1)
		main_image_rotation = st.selectbox("Set a degree rotation for the main image",[0,90,180,270])
		watermark_rotation = st.select_slider("Angle to rotate 🔄",range(0,380,10))
	with n2:
		position = st.selectbox("In which position do you want the watermark?",['lower left corner','lower right corner','center','upper left corner','upper right corner'])
		location = pos[position]
		recolor = st.selectbox("Keep original watermark color?",['Yes','No, I want to choose a new color (feature recommended for monochromatic image)'])
		if recolor != 'Yes':
			recolor=True
			new_color = st.color_picker("New color")
			new_color = ImageColor.getcolor(new_color, "RGB")
		else:
			recolor=False

try:
	reshape_factor = float(reshape_factor)
	transparent_factor = float(transparent_factor)
except:
	st.warning("Values not valid")
if photo is not None and watermark is not None:
	if st.button("Generate"):
		new_image = add_watermark(photo,watermark_path=watermark,position=location,reshape_factor=reshape_factor,transparent_factor=transparent_factor,recolor=recolor,rotate=int(watermark_rotation),main_image_rotation=360-main_image_rotation)
		st.image(new_image)
		buf = BytesIO()
		new_image = new_image.convert('RGB')
		new_image.save(buf, format="JPEG")
		byte_im = buf.getvalue()
		btn = st.download_button(
				label="Download Image",
				data=byte_im,
				file_name=photo.name[:-4]+"_watermark.jpg",
				mime="image/jpeg",
		)
