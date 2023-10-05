# Watermark_picture
To add watermark into JPG photos in an automatized way
# How it works
0. Instal the PIL library using the requirements.txt (in case you don't)
1. Add the images and watermark into the origin directory. Make sure that there is only one watermark in the directory and that is a png (otherwise, you would only get the last png file orderd by name ascending) with no background and rename the pictures' extension to JPG
2. Go to watermark_merge.py to the last line and edit the position, reshape_factor and transparent_factor as you prefer. Try combinations to get something that you like
3. Execute the code
4. Check in the watermark directory the new pictures and enjoy :)

You can check some results that I left on the watermark directory. Try new parameter values

# Next Steps
1. To make the parameter position, reshape_factor and transparent_factor to accept arrays to have a different watermark per picture
2. Be able to rotate the pictures, in case you have horizontal or vertical alignment.
3. etc (Could add new features that I'm not thinking right now)
