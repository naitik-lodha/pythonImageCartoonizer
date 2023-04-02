import cv2
import numpy as np
import os


def read_image(filename):
    img = cv2.imread(filename)
    return img


def detect_edges(img, line_width, blur):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray_blur = cv2.medianBlur(gray, blur)
    edges = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
                                  cv2.THRESH_BINARY, line_width, blur)

    return edges


def quantize_colors(img, total_colors):
    image_data = np.float32(img).reshape((-1, 3))
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 0.001)
    ret, label, cluster_centers = cv2.kmeans(image_data, total_colors, None,
                                              criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    cluster_centers = np.uint8(cluster_centers)
    quantized = cluster_centers[label.flatten()]
    quantized = quantized.reshape(img.shape)
    return quantized


def apply_cartoon_filter(img, edges):
    blurred = cv2.bilateralFilter(img, d=7, sigmaColor=200, sigmaSpace=200)
    cartoon = cv2.bitwise_and(blurred, blurred, mask=edges)
    return cartoon


def cartoonize_image(input_file):
    base_name = os.path.splitext(os.path.basename(input_file))[0]
    ext = '.jpg'
    output_file = base_name + '_cartoon' + ext
    line_width = 7
    blur = 5
    total_colors = 5
    img = read_image(input_file)
    edges = detect_edges(img, line_width, blur)
    quantized = quantize_colors(img, total_colors)
    cartoon = apply_cartoon_filter(quantized, edges)
    cv2.imwrite(output_file, cartoon)

    return output_file
