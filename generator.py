from PIL import Image
import cv2
from math import floor
from sys import stdout
from os.path import splitext


def check_video_dimensions(frame_count, width):
    # Check that its not longer than 10 mins
    if frame_count > 54000:
        print("Sorry, this video is too long, try again with a video under 30 minutes in length")
        quit()  # TODO: find a more elegant way to do this

    # Check that its not too short
    if frame_count < width:
        print('Sorry, this video is too short (or possibly too high res)')
        quit()


def write_column(column, width, height, image, final_image):
    for row in range(height):
        # 1. get enumerated list of the rows colours
        im_colours = Image.fromarray(image[row].reshape(1, width, 3)).getcolors(width)

        # 2. get most dominant colour in row
        most_freq = im_colours[0]
        for count, colour in im_colours:
            if count > most_freq[0]:
                most_freq = (count, colour)

        # 3. write pixel to final image
        final_image[row][column - 1] = most_freq[1]


def convert_filename(filename):
    return splitext(filename)[0] + '.png'


def generate_barcode(video_file, debug=True):
    print('Generating a barcode')

    # Setup
    reader = cv2.VideoCapture(video_file)
    success, frame = reader.read()
    success = True
    frame_height = len(frame)
    frame_width = len(frame[0])
    result_array = frame
    frame_count = int(reader.get(cv2.CAP_PROP_FRAME_COUNT)) / 2
    queue_length = floor(frame_count / frame_width)  # NOTE: THIS CANNOT BE 0

    check_video_dimensions(frame_count, frame_width)

    queue_counter = 0
    num_processed_images = 0
    while success:
        queue_counter += 1
        success, frame = reader.read()
        if queue_counter == queue_length:
            queue_counter = 0
            num_processed_images += 1
            print('\rProgress: %.f%%' % (100 * num_processed_images / frame_width), end='\r')
            stdout.flush()
            write_column(num_processed_images, frame_width, frame_height, frame, result_array)

            # break if you reach the end of the image array
            if num_processed_images == frame_width:
                print('Finished processing image.')
                break

    final_image = Image.fromarray(result_array, 'RGB')

    if debug:
        print('length: {}'.format(frame_count))
        print('q_length: {}'.format(queue_length))
        print('counter: {}'.format(num_processed_images))
        print('width: {}'.format(frame_width))

    image_file = convert_filename(video_file)
    final_image.save(image_file)
    print(image_file)
    reader.release()
    return image_file


if __name__ == '__main__':
    generate_barcode('firestone.mp4')
    # generator.generate_barcode('sorryToBotherYou.mp4')
