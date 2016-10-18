import os
import json

from PIL import Image
from bs4 import BeautifulSoup


def main():
    """
    Please check the README file before running. It has instructions on how to use this script. 
    """
    arcss = os.path.dirname(os.path.abspath(__file__))
    hi = os.path.join(arcss, 'images', 'GalleryPhotos')
    low = os.path.join(hi, 'low')

    # Compare the files in the hi and low folders
    hi_list = list_files(arcss, hi)
    low_list = list_files(arcss, low)

    # If there are files in the hi folder that are not in the low folder, generate thumbnails and code
    new_images = set(hi_list).difference(low_list)
    for i in new_images:
        print("new image: " + i)

    # Start generating thumbnails inside of "low"
    with open('captions.json', 'r') as f:
        j = json.load(f)
        print("Generating thumbnails...")
        size = 200, 200
        for infile in hi_list:
            os.chdir(hi)
            # file, ext = os.path.splitext(infile)
            im = Image.open(infile)
            # Check if this image has a caption or not.
            if infile not in j:
                # If there's no caption entry, then show the image and ask user for a caption.
                im.show()
                print("Please provide a caption for the image shown:")
                caption = raw_input()
                j[infile] = caption
            # Create thumbnail image
            im.thumbnail(size)
            os.chdir(low)
            # Save the new thumbnail in the low folder
            im.save(infile)
            im.close()

    os.chdir(arcss)
    # Write out the new captions json data
    with open('captions.json', 'w+') as f:
        json.dump(j, f, indent=2)

    # Generate html code for new images
    add_new_html(hi_list, j)
    print("Complete!")

    return


def list_files(arcss, path):
    """
    Lists file(s) in given path of the X type. Rename all files into lowercase, for easier handling.
    :param path: (str) File extension that we are interested in.
    :return: (list of str) File name(s) to be worked on
    """
    ext = ['.jpg', '.jpeg', '.tiff', '.tif', '.png', '.gif', '.JPG', '.Jpg']
    file_list = []

    os.chdir(path)
    for file in os.listdir(path):
        new_file = file.lower().replace (" ", "_")
        if new_file != file:
            os.rename(file, new_file)

    for file in os.listdir(path):
        if file.endswith(tuple(ext)):
            file_list.append(file)
    os.chdir(arcss)
    return file_list


def add_new_html(l, captions):
    """
    Create HTML code for the new photos and thumbnails, and append it to the existing images.html file.
    :param l: (list) New images
    :param captions: (dict) Filename - caption
    :return: None
    """
    html_imgs = ""
    print("Creating HTML...")
    doc = open('gallery.html', 'r+')
    # Decode and create an object with our gallery.html
    soup = BeautifulSoup(doc, 'html.parser')
    # Find the DIV that holds the image code
    div = soup.find(id="bs4")
    # Clear out the old image code from the DIV
    div.clear()
    # Make a giant string of HTML code for all the images
    for name, cap in captions.items():
        # Add one string of image code to the giant string of image code
        html_imgs += html_line(name, cap)
    # Append the image code to the correct DIV in the html
    div.append(BeautifulSoup(html_imgs, 'html.parser'))

    # Close out the old HTML file
    doc.close()
    # Get some nice HTML formatting
    h = soup.prettify("utf-8")
    # Open up the HTML file again for writing out our new code
    with open('gallery.html', 'wb') as f:
        f.write(h)
    return


def html_line(filename, caption):
    """
    String together the HTML code for one image
    :param filename:
    :param caption:
    :return: (str) HTML code
    """
    one = '<a class="example-image-link" href="images/GalleryPhotos/' + filename
    two = '" data-lightbox="example-set" data-title="' + caption + '">'
    three = '<img class="example-image" src="images/GalleryPhotos/low/' + filename + '" alt="" /></a>\n\n'
    return one + two + three



main()
