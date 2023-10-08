import streamlit as st
from io import BytesIO
from PIL import Image
from pathlib import Path

def add_watermark(image_path, watermark_path, position, reshape_factor, transparent_factor):
	# OPEN IMAGE AND WATERMARK
	layer1 = Image.open(image_path).convert('RGBA')
	layer2 = Image.open(watermark_path).convert('RGBA')

	# SET NEW SIZE FOR WATERMARK USING MULTIPLYING FACTOR
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

	# Make all opaque pixels into semi-opaque
	a = layer2_reshape.getchannel('A')
	new_a = a.point(lambda i: int(255*transparent_factor) if i > 100 else 0)
	layer2_reshape.putalpha(new_a)

	# CREATE CANVAS FROM IMAGE
	canvas = Image.new("RGBA", layer1.size)
	# INSERT INTO CANVAS WATERMARK AT DESIRED POSITION
	canvas.paste(layer2_reshape, coordinates, layer2_reshape)
	# INSERT INTO IMAGE THE WATERMARK
	layer1.paste(canvas, (0, 0), mask=canvas)
	return layer1

st.title("UI test")
photo = st.file_uploader("Insert picture")
if photo is not None:
	st.write(photo)
	st.write("Image preview")


	new_image = add_watermark(photo,watermark_path="C:\\Users\\Rodrigo\\Desktop\\COURSERA\\Watermark_picture\\original\\watermark_sign.png",position="c",reshape_factor=8,transparent_factor=0.5)
	st.image(new_image)
	buf = BytesIO()
	new_image = new_image.convert('RGB')
	new_image.save(buf, format="JPEG")
	byte_im = buf.getvalue()
	btn = st.download_button(
		label="Download Image",
		data=byte_im,
		file_name="imagename.png",
		mime="image/jpeg",
	)