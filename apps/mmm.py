import numpy as np  # linear algebra
import math
import cv2
from scipy.signal import argrelmin


def createKernel(kernelSize, sigma, theta):
    "create anisotropic filter kernel according to given parameters"
    assert kernelSize % 2  # must be odd size
    halfSize = kernelSize // 2  # get integer-valued resize of division

    kernel = np.zeros([kernelSize, kernelSize])  # kernel
    sigmaX = sigma  # scale factor for X dimension
    sigmaY = sigma * theta  # theta - multiplication factor = sigmaX/sigmaY

    for i in range(kernelSize):
        for j in range(kernelSize):
            x = i - halfSize
            y = j - halfSize

            expTerm = np.exp(-x ** 2 / (2 * sigmaX) - y ** 2 / (2 * sigmaY))
            xTerm = (x ** 2 - sigmaX ** 2) / (2 * math.pi * sigmaX ** 5 * sigmaY)
            yTerm = (y ** 2 - sigmaY ** 2) / (2 * math.pi * sigmaY ** 5 * sigmaX)

            kernel[i, j] = (xTerm + yTerm) * expTerm

    kernel = kernel / np.sum(kernel)
    return kernel


def lineSegmentation(img, kernelSize=25, sigma=11, theta=7):
    """Scale space technique for lines segmentation proposed by R. Manmatha:
	http://ciir.cs.umass.edu/pubfiles/mm-27.pdf
    Args:
		img: image of the text to be segmented on lines.
        kernelSize: size of filter kernel, must be an odd integer.
		sigma: standard deviation of Gaussian function used for filter kernel.
		theta: approximated width/height ratio of words, filter function is distorted by this factor.
		minArea: ignore word candidates smaller than specified area.
	Returns:
		List of lines (segmented input img)
	"""

    img_tmp = np.transpose(prepareTextImg(img))  # image to be segmented (un-normalized)
    img_tmp_norm = normalize(img_tmp)
    k = createKernel(kernelSize, sigma, theta)
    imgFiltered = cv2.filter2D(img_tmp_norm, -1, k, borderType=cv2.BORDER_REPLICATE)
    img_tmp1 = normalize(imgFiltered)
    # Make summ elements in columns to get function of pixels value for each column
    summ_pix = np.sum(img_tmp1, axis=0)
    smoothed = smooth(summ_pix, 35)
    mins = np.array(argrelmin(smoothed, order=2))
    found_lines = transpose_lines(crop_text_to_lines(img_tmp, mins[0]))
    return found_lines


def prepareTextImg(img):
    """ Convert given text image to grayscale image (if needed) and return it. """
    assert img.ndim in (2, 3)
    if img.ndim == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return (img)


def normalize(img):
    """ Normalize input image:
    img = (img[][]-mean)/ stddev
    using function: cv2.meanStdDev(src[, mean[, stddev[, mask]]]), returns: mean, stddev
    where: mean & stddev - numpy.ndarray[][] """
    (m, s) = cv2.meanStdDev(img)
    m = m[0][0]
    s = s[0][0]
    img = img - m
    img = img / s if s > 0 else img
    return img


def smooth(x, window_len=11, window='hanning'):
    """ Image smoothing is achieved by convolving the image with a low-pass filter kernel.
    Such low pass filters as: ['flat', 'hanning', 'hamming', 'bartlett', 'blackman'] can be used
    It is useful for removing noise. It actually removes high frequency content
    (e.g: noise, edges) from the image resulting in edges being blurred when this is filter is applied."""
    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")
    if window_len < 3:
        return x
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError("Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")
    s = np.r_[x[window_len - 1:0:-1], x, x[-2:-window_len - 1:-1]]

    if window == 'flat':  # moving average
        w = np.ones(window_len, 'd')
    else:
        w = eval('np.' + window + '(window_len)')

    y = np.convolve(w / w.sum(), s, mode='valid')
    return y


def crop_text_to_lines(text, blanks):
    """ Splits the image with text into lines, according to the markup obtained from the created algorithm.
     Very first"""
    x1 = 0
    y = 0
    lines = []
    for i, blank in enumerate(blanks):
        x2 = blank
        line = text[:, x1:x2]
        lines.append(line)
        x1 = blank
    print("Lines found: {0}".format(len(lines)))
    return lines


def transpose_lines(lines):
    res = []
    for l in lines:
        line = np.transpose(l)
        res.append(line)
    return res

if __name__ == '__main__':

    image = cv2.imread('/media/fulvio/Data/Docs/handwritten-text-2.jpg')
    for i, x in enumerate(lineSegmentation(image)):
        cv2.imwrite(f"line{i}.png", x)
