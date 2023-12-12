import imgui
import torch

from gui_utils import imgui_utils, gl_utils
import numpy as np
import matplotlib.pyplot as plt
import os
os.environ['KMP_DUPLICATE_LIB_OK']='True'

class VisualizeWidget:
    def __init__(self, viz):
        self.viz = viz
        self.disabled_time = 0
        self.show_value = "current"
        self.texture_obj = None
        self.tex_img = None
        self.w1 = None
        self.w2 = None
        self.w = None
        self.w_diff = None
        self.image_array = None
        self.previous = None
        self.started = False
        self.started_previous = False
        self.w_index = 0
        self.w_index_previous = 0
        self.histogram_texture_object = None
        self.histogram = None
        self.plt = None
        self.times_minus_one = False
        self.step_scale = 1

    def __call__(self, show=True):
        viz = self.viz
        if show:
            with imgui_utils.grayed_out(self.disabled_time != 0):
                imgui.text("Visualize")
                imgui.same_line(viz.label_w)

                if imgui_utils.button("Current W", width=viz.button_w, enabled='image' in viz.result):
                    self.show_value = "current"
                    print("show current")

                imgui.same_line()
                if imgui_utils.button("Current W1", width=viz.button_w, enabled='image' in viz.result):
                    self.show_value = "W1"
                    print("show w1")
                imgui.text(' ')
                imgui.same_line(viz.label_w)
                if imgui_utils.button("Current W2", width=viz.button_w, enabled='image' in viz.result):
                    self.show_value = "W2"
                    print("show w2")

                imgui.same_line()
                if imgui_utils.button("Diff w1, w2", width=viz.button_w, enabled='image' in viz.result):
                    self.show_value = "diff"
                    print("show diff")




                imgui.text(' ')
                imgui.same_line(viz.label_w)
                with imgui_utils.item_width(viz.font_size * 6):
                    changed, self.w_index = imgui.input_int('W index', self.w_index)


                imgui.text(' ')
                imgui.same_line(viz.label_w)
                if imgui_utils.button("show plot",width=viz.button_w,enabled='image' in viz.result):
                    # self.plt.ion()
                    self.plt.show()


                imgui.text(' ')
                imgui.same_line(viz.label_w)
                if imgui_utils.button("w * -1",width=viz.button_w,enabled='image' in viz.result):
                    # self.plt.ion()
                    self.times_minus_one = True


                imgui.text(' ')
                imgui.same_line(viz.label_w)
                with imgui_utils.item_width(viz.font_size * 6):
                    changed, self.step_scale = imgui.input_int('Step Scale', self.step_scale)



            if self.previous == self.show_value and not (self.started and not self.started_previous) and self.w_index == self.w_index_previous:
                l = self.image_array
            else:
                l = self._create_image()
            self.image_array = l
            if not l == []:
                self.tex_img = np.array(l, np.uint8)
                self.texture_obj = gl_utils.Texture(image=self.tex_img, bilinear=False, mipmap=False)
                self.texture_obj.draw(pos=[600, 850], zoom=[10.0, 10.0], align=0.5, rint=True)
                if self.show_value == "diff":
                    w = self.w_diff
                if self.show_value == "W2":
                    w = self.w2
                if self.show_value == "W1":
                    w = self.w1
                if self.show_value == "current":
                    w = self.w
                w = w.cpu().numpy()[0]
                if w is not None:
                    if self.previous == self.show_value and not (
                            self.started and not self.started_previous) and self.w_index == self.w_index_previous:
                        histogram = self.histogram
                    elif self.w_index < len(w):

                        if len(w.shape) == 1:
                            w = np.array([w])
                        histogram = self.plot_histogram(np.array(w[self.w_index]).flatten())


                    # self.histogram_texture_object = gl_utils.Texture(image=histogram, bilinear=False, mipmap=False)
                    # self.histogram_texture_object.draw(pos=[1600, 150], zoom=[1.0, 1.0], align=0.5, rint=True)

                    self.histogram = histogram

        self.disabled_time = max(self.disabled_time - viz.frame_delta, 0)
        self.previous = self.show_value
        self.started_previous = self.started
        self.w_index_previous = self.w_index

    def _create_image(self):
        l = []
        if self.show_value == "diff":
            w = self.w_diff
        if self.show_value == "W2":
            w = self.w2
        if self.show_value == "W1":
            w = self.w1
        if self.show_value == "current":
            w = self.w

        if w is None:
            return []
        w = w.cpu().numpy()[0]

        if len(w.shape) == 1:
            w = np.array([w])

        if len(w) <= self.w_index:
            return []
        w_row = w[self.w_index]


        maxi = np.max(w_row)
        mini = np.min(w_row)
        print("maximum: ", maxi)
        print("minimum: ", mini)

        for height in range(0,16):

            l1 = []
            for width in range(0,32):
                y_var = w_row[height + width*16]
                if y_var > 0:
                    l1.append([round(y_var / maxi * 255), 0, 0, 255])
                elif y_var == 0:
                    l1.append([255, 255, 0, 255])
                else:
                    l1.append([0, round(y_var / mini * 255), 0, 255])
            l.append(l1)
            # l.append([[0,0,0,255]]*len(l1))

        # for x in w:
        #     l1 = []
        #     for y in x:
        #         if y > 0:
        #             l1.append([round(y / maxi * 255), 0, 0, 255])
        #         elif y == 0:
        #             l1.append([255, 255, 0, 255])
        #         else:
        #             l1.append([0, round(y / mini * 255), 0, 255])
        #     l.append(l1)
        #     l.append([[0,0,0,255]]*len(l1))
        return l




    def plot_histogram(self, array, num_buckets=100):
        # Create histogram buckets
        counts, edges = np.histogram(array, bins=num_buckets)

        # Plot the bar graph
        plt.bar(edges[:-1], counts, width=np.diff(edges), align="edge", color="blue")

        # Add labels and title
        plt.xlabel("Value")
        plt.ylabel("Frequency")
        plt.title("Histogram of Values")



        # Show the plot

        fig = plt.gcf()
        fig.canvas.draw()
        temp1 = fig.canvas.tostring_rgb()
        img_data = np.frombuffer(temp1, dtype=np.uint8)
        print(len(img_data))
        temp2 = fig.canvas.get_width_height()
        print(temp2)
        print(fig.get_size_inches()*fig.dpi)
        temp2 = fig.get_size_inches()*fig.dpi
        print(temp2[0])
        temp2 = (round(temp2[0]), round(temp2[1]))
        print(temp2)
        img_data = img_data.reshape(temp2[::-1] + (3,))
        self.plt = plt
        return img_data