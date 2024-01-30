import numpy as np
from PIL import Image
from scipy.ndimage import convolve

def grayscale_image(image, return_array=False):
    """
    Convert an image to grayscale.
    
    Args:
        image (PIL.Image.Image): The input image.
        return_array (bool): Whether to return a numpy array or a PIL image.
        
    Returns:
        PIL.Image.Image or numpy.ndarray: The grayscale image.
    """
    image_array = np.array(image)

    grayscale_image = np.dot(image_array, [0.2989, 0.5870, 0.1140])

    grayscale_image = grayscale_image.astype(np.uint8)

    if return_array:
        return grayscale_image
    else:
        rgb_image_gray = np.stack((grayscale_image,) * 3, axis=-1)

        return Image.fromarray(rgb_image_gray, 'RGB')

def horizontal_derivative(image):
    """
    Apply a horizontal derivative to an image.
    
    Args:
        image_array (PIL.Image.Image): The input image.
        
    Returns:
        PIL.Image.Image: The image with a horizontal derivative applied.
    """
    matrix = np.array([[-1, 0, 1]])

    image_array = grayscale_image(image, return_array=True)

    result_image = np.zeros_like(image_array.astype(np.int16))

    for image_row in range(image_array.shape[0]):
        for image_col in range( 1 , image_array.shape[1] - 1):
            region = image_array[image_row, image_col - 1 : image_col + 2]

            convolved_value = np.sum(region * matrix)

            result_image[image_row, image_col] = convolved_value

    return image_to_rb(result_image)

def vertical_derivative(image):
    """
    Apply a vertical derivative to an image.
    
    Args:
        image_array (PIL.Image.Image): The input image.
        
    Returns:
        PIL.Image.Image: The image with a vertical derivative applied.
    """
    matrix = np.array([[-1], [0], [1]])

    image_array = grayscale_image(image, return_array=True)

    result_image = np.zeros_like(image_array.astype(np.int16))

    for image_row in range(1, image_array.shape[0] - 1):
        for image_col in range(image_array.shape[1]):
            region = image_array[image_row - 1 : image_row + 2, image_col].reshape(3, 1)

            convolved_value = np.sum(region * matrix)

            result_image[image_row, image_col] = convolved_value

    return image_to_rb(result_image)

def image_to_rb(image_array):

    result_image = np.stack((np.zeros_like(image_array),) * 3, axis=-1)

    for row in range(result_image.shape[0]):
        for col in range(result_image.shape[1]):
            if image_array[row][col] < 0:
                result_image[row, col, 2] = -image_array[row][col] ** 2
            else:
                result_image[row, col, 0] = image_array[row][col] ** 2

    return Image.fromarray(result_image.astype('uint8'), 'RGB')

def blur_image(image, blur_amount):
    """
    Apply a Gaussian blur to an image.
    
    Args:
        image_array (PIL.Image.Image): The input image.
        blur_amount (int): The amount of blur to apply.
        
    Returns:
        PIL.Image.Image: The blurred image.
    """
    blur_matrix = guassian_blur(blur_amount)
    blurred_array = matrix_multiply(image, blur_matrix)
    return Image.fromarray(blurred_array)
    
def guassian_blur(blur_amount):
    """
    Generate a Gaussian blur matrix.
    
    Args:
        blur_amount (int): The amount of blur to apply.
        
    Returns:
        numpy.ndarray: The Gaussian blur matrix.
    """
    blur_matrix = np.ones((blur_amount * 2 + 1, blur_amount * 2 + 1))
    for i in range(blur_matrix.shape[0]):
        for j in range(blur_matrix.shape[1]):
            x = min(i, blur_amount * 2 - i)
            y = min(j, blur_amount * 2 - j)
            blur_matrix[i, j] = 2 ** (x + y)  
    return blur_matrix
            
def matrix_multiply(image, matrix, correct_matrix=True):
    """
    Apply matrix multiplication to an image.
    
    Args:
        image (PIL.Image.Image): The input image.
        matrix (numpy.ndarray): The matrix to multiply with.
        
    Returns:
        numpy.ndarray: The result of the matrix multiplication.
    """
    image_array = np.array(image)
    result_image = np.zeros_like(image_array)

    half_matrix = matrix.shape[0] // 2
    for color in range(image_array.shape[2]):
        for image_row in range(image_array.shape[0]):
            for image_col in range(image_array.shape[1]):
                region = image_array[max(image_row - half_matrix, 0): min(image_row + half_matrix + 1, image_array.shape[0]),
                               max(image_col - half_matrix, 0): min(image_col + half_matrix + 1, image_array.shape[1]), color]
                new_matrix = matrix
                if region.shape[0] != matrix.shape[0]:
                    if (x := image_row - half_matrix) < 0:
                        new_matrix = matrix[-x:, :]
                    else:
                        x = image_row + half_matrix + 1 - image_array.shape[0]
                        new_matrix = matrix[:-x, :]
                if region.shape[1] != matrix.shape[1]:
                    if (y := image_col - half_matrix) < 0:
                        new_matrix = new_matrix[:, -y:]
                    else:
                        y = image_col + half_matrix + 1 - image_array.shape[1]
                        new_matrix = new_matrix[:, :-y]  

                if correct_matrix:
                    new_matrix = new_matrix / np.sum(new_matrix)

                convolved_value = np.sum(region * new_matrix)
                result_image[image_row, image_col, color] = convolved_value
    return result_image

def brightness_image(image, brightness_amount):
    """
    Adjust the brightness of an image.
    
    Args:
        image (PIL.Image.Image): The input image.
        brightness_amount (int): The amount of brightness to apply.
        
    Returns:
        PIL.Image.Image: The brightness-adjusted image.
    """

    brightness_amount = brightness_amount ** 2 / 100
    
    image_array = np.array(image)

    corected_image = np.clip( image_array * brightness_amount, 0, 255)

    return Image.fromarray(corected_image.astype('uint8'))

def sobel_derivative(image):
    """
    Apply a Sobel filter to an image.
    
    Args:
        image (PIL.Image.Image): The input image.
        
    Returns:
        PIL.Image.Image: The Sobel-filtered image.
    """
    if image.mode != 'L':
        image = image.convert('L')
    
    image_array = np.array(image)
    
    horizontal_kernel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    vertical_kernel = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])

    gradient_magnitude = np.zeros_like(image_array)
    
    padded_image = np.pad(image_array, 1, mode='edge')
    
    for i in range(1, padded_image.shape[0] - 1):
        for j in range(1, padded_image.shape[1] - 1):
            region = padded_image[i-1:i+2, j-1:j+2]
            horizontal_response = np.sum(horizontal_kernel * region)
            vertical_response = np.sum(vertical_kernel * region)
            gradient_magnitude[i-1, j-1] = np.sqrt(horizontal_response**2 + vertical_response**2)
    
    gradient_magnitude = (gradient_magnitude / gradient_magnitude.max()) * 255
    
    result_image = gradient_magnitude.astype(np.uint8)
    
    return Image.fromarray(result_image)