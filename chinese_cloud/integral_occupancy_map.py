from query_integral_image import query_integral_image
import numpy


class IntegralOccupancyMap(object):

    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.integral = numpy.zeros((height, width), dtype=numpy.uint32)

    def sample_position(self, size_x, size_y, random_state):
        return query_integral_image(self.integral, size_x, size_y, random_state)

    def update(self, img_array, pos_x, pos_y):
        partial_integral = numpy.cumsum(numpy.cumsum(img_array[pos_x:, pos_y:], axis=1), axis=0)
        if pos_x > 0:
            if pos_y > 0:
                partial_integral += (self.integral[pos_x - 1, pos_y:]
                                     - self.integral[pos_x - 1, pos_y - 1])
            else:
                partial_integral += self.integral[pos_x - 1, pos_y:]
        if pos_y > 0:
            partial_integral += self.integral[pos_x:, pos_y - 1][:, numpy.newaxis]

        self.integral[pos_x:, pos_y:] = partial_integral
