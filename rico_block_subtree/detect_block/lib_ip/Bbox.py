import numpy as np
import cv2
import lib_ip.ip_draw as draw


class Bbox:
    def __init__(self, col_min, row_min, col_max, row_max):
        self.col_min = col_min
        self.row_min = row_min
        self.col_max = col_max
        self.row_max = row_max

        self.width = col_max - col_min
        self.height = row_max - row_min
        self.box_area = self.width * self.height

    def put_bbox(self):
        return self.col_min, self.row_min, self.col_max, self.row_max

    def bbox_cal_area(self):
        self.box_area = self.width * self.height
        return self.box_area

    def bbox_relation(self, bbox_b):
        """
        :return: -1 : a in b
                 0  : a, b are not intersected
                 1  : b in a
                 2  : a, b are identical or intersected
        """
        col_min_a, row_min_a, col_max_a, row_max_a = self.put_bbox()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.put_bbox()

        # if a is in b
        if col_min_a > col_min_b and row_min_a > row_min_b and col_max_a < col_max_b and row_max_a < row_max_b:
            return -1
        # if b is in a
        elif col_min_a < col_min_b and row_min_a < row_min_b and col_max_a > col_max_b and row_max_a > row_max_b:
            return 1
        # a and b are non-intersect
        elif (col_min_a > col_max_b or row_min_a > row_max_b) or (col_min_b > col_max_a or row_min_b > row_max_a):
            return 0
        # intersection
        else:
            return 2

    def bbox_relation_nms(self, bbox_b, bias=0):
        '''
        Calculate the relation between two rectangles by nms
       :return: -1 : a in b
         0  : a, b are not intersected
         1  : b in a
         2  : a, b are intersected
         3  : a, b are same
       '''
        col_min_a, row_min_a, col_max_a, row_max_a = self.put_bbox()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.put_bbox()

        # get the intersected area
        col_min_s = max(col_min_a - bias, col_min_b - bias)
        row_min_s = max(row_min_a - bias, row_min_b - bias)
        col_max_s = min(col_max_a + bias, col_max_b + bias)
        row_max_s = min(row_max_a + bias, row_max_b + bias)
        w = np.maximum(0, col_max_s - col_min_s)
        h = np.maximum(0, row_max_s - row_min_s)
        inter = w * h
        area_a = (col_max_a - col_min_a) * (row_max_a - row_min_a)
        area_b = (col_max_b - col_min_b) * (row_max_b - row_min_b)
        iou = inter / (area_a + area_b - inter)
        ioa = inter / self.box_area
        iob = inter / bbox_b.box_area

        # print('IoU:%.3f, IoA:%.3f, IoB:%.3f' % (iou, ioa, iob))

        # not intersected with each other
        if iou == 0:
            return 0
        # a and b are same
        if iou >= 0.8 and ioa >= 0.85 and iob >= 0.85 and abs(ioa - iob) < 0.08:
            return 3
        # contained by b
        if ioa >= 0.9:
            return -1
        # contains b
        if iob >= 0.9:
            return 1
        # intersected
        return 2

    def bbox_cvt_relative_position(self, col_min_base, row_min_base):
        '''
        Convert to relative position based on base coordinator
        '''
        self.col_min += col_min_base
        self.col_max += col_min_base
        self.row_min += row_min_base
        self.row_max += row_min_base

    def bbox_merge(self, bbox_b):
        '''
        Merge two intersected bboxes
        '''
        col_min_a, row_min_a, col_max_a, row_max_a = self.put_bbox()
        col_min_b, row_min_b, col_max_b, row_max_b = bbox_b.put_bbox()
        col_min = min(col_min_a, col_min_b)
        col_max = max(col_max_a, col_max_b)
        row_min = min(row_min_a, row_min_b)
        row_max = max(row_max_a, row_max_b)
        new_bbox = Bbox(col_min, row_min, col_max, row_max)
        return new_bbox

    def bbox_padding(self, image_shape, pad):
        row, col = image_shape[:2]
        self.col_min = max(self.col_min - pad, 0)
        self.col_max = min(self.col_max + pad, col)
        self.row_min = max(self.row_min - pad, 0)
        self.row_max = min(self.row_max + pad, row)

    def bbox_fill_box(self, img, color, pad=0):
        cv2.rectangle(img, (self.col_min - pad, self.row_min - pad), (self.col_max + pad, self.row_max + pad), color, -1)