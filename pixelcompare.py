# from PIL import Image
#
# from pixelmatch.contrib.PIL import pixelmatch
#
# img_a = Image.open("image1.png")
# pixel_a = img_a.load()
# img_b = Image.open("image2.png")
# pixel_b = img_b.load()
# img_diff = Image.new("RGBA", img_a.size)
#
#
# (width, height) = img_a.size
#
# output_image = Image.new("RGBA", (width, height), color="black")
# pixel_output = output_image.load()
#
# # note how there is no need to specify dimensions
# # mismatch = pixelmatch(img_a, img_b, img_diff, includeAA=True, alpha=0)
# # print(pixel_a - pixel_b)
# # print(type(mismatch))
# # print(mismatch)
#
# for x in range(0, width):
#     for y in range(0, height):
#         a = pixel_a[x,y]
#         b = pixel_b[x,y]
#         change = pow(pow(b[0] - a[0], 2) + pow(b[1] - a[1], 2) + pow(b[2] - a[2], 2), 0.5)
#         if change > 0:
#             pixel_output[x,y] = (0,0,round(change))
#         else:
#             pixel_output[x,y] = (round(change),0,0)
#
#
# img_diff.save("diff.png")
# output_image.save("manual_diff.png")
# output_image.show()

import matplotlib.pyplot as plt
import numpy as np

def plot_histogram(array, num_buckets=10):
    # Create histogram buckets
    counts, edges = np.histogram(array, bins=num_buckets)

    # Plot the bar graph
    plt.bar(edges[:-1], counts, width=np.diff(edges), align="edge")

    # Add labels and title
    plt.xlabel("Value")
    plt.ylabel("Frequency")
    plt.title("Histogram of Values")

    # Show the plot
    plt.show()

input_array = np.random.randn(1000)  # Replace this with your input array
plot_histogram(input_array)