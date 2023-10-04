import os
from PIL import Image
# bibliography:
# https://stackoverflow.com/questions/59585605/valueerror-images-do-not-match-when-blending-pictures-in-pil
# https://stackoverflow.com/questions/65320842/python-pil-reduce-alpha-level-but-do-not-change-transparent-background


def get_photos(directory_path="original", position="c", reshape_factor=8, transparent_factor=0.7):
	"""

	:param directory_path: Directory name where the images are located
	:param position: position to collocate the watermark
	:param reshape_factor: multiplier to increase/reduce watermark's original size
	:param transparent_factor: how translucent or opaque will be the watermark: 0(invisible) - 1 (opaque)
	:return: None
	"""
	image_list = []
	watermark_loc = ""
	images = os.listdir(directory_path)
	images = [(os.path.abspath(directory_path)+"\\"+i) for i in images]
	# images = [i.replace("\\", '/') for i in images]
	for i in images:
		if ".JPG" in image:
			image_list.append(str(i))
		else:
			watermark_loc = str(i)
	for i in image_list:
		add_watermark(i, watermark_loc, position, reshape_factor, transparent_factor)
	return None


def add_watermark(image_path, watermark_path, position="c", reshape_factor=8, transparent_factor=0.7):
	"""
	:param image_path: Path from the image to add watermark
	:param watermark_path: Path from the watermark
	:param position: where the watermark is going to be located. Values: c - Center, ul - Upper Left, ur - Upper Right, uc - Upper Center, ll - Lower Left, lr - Lower Right, lc - Lower Center,
	:param reshape_factor: multiplier to original size to increase/reduce
	:param transparent_factor: how translucent or opaque will be the watermark: 0(invisible) - 1 (opaque)
	:return: None
	"""
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
	# CREATE NEW IMAGE IN DESIRED LOCATION
	result_path = image_path.replace("original", "watermark").replace(".JPG", "_watermark.JPG")
	layer1.convert("RGB").save(result_path)
	return None

# MASTER FUNCTION TO LAUNCH
# get_photos(directory_path="original", position="c", reshape_factor=8, transparent_factor=0.65)

# TEST
image = 'C:/Users/Rodrigo/Desktop/COURSERA/Watermark_picture/original/1.JPG'
watermark = 'C:/Users/Rodrigo/Desktop/COURSERA/Watermark_picture/original/purple_watermark.png'
add_watermark(image, watermark, position="c", reshape_factor=8, transparent_factor=0.7)
