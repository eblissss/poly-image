# Poly Image

### Creates a binary poly-image from an input image.

- Works best with binary images as input.

<br>

#### Samples the image at a specified interval and runs a simple marching squares algorithm to link points together.

<br>

### Examples:

<img src="images/worldmap.png" alt="Worldmap" width=300 /> <img src="images/polyworldmap.png" alt="Poly Worldmap" width=300 />

<img src="images/leopard.png" alt="Leopard" width=300 /> <img src="images/polyleopard.png" alt="Poly Leopard" width=300 />

### To run:

- Run `pip install -r requirements.txt`
- Run `./polimage.py [filename] (X samples) (Y samples)`
- Output colors can be tweaked in the file
