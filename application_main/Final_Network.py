import cv2
import numpy as np
from matplotlib import pyplot as plt
from neural_network import make_predictions


def preprocess_mobile_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (28, 28), interpolation=cv2.INTER_LINEAR)
    img_resized = cv2.bitwise_not(img_resized)
    img_normalized = img_resized / 255.0
    img_flattened = img_normalized.flatten()
    return img_flattened


def load_parameters(path="saved_parameters.npz"):
    loaded_params = np.load(path)
    return (
        loaded_params["W1"],
        loaded_params["b1"],
        loaded_params["W2"],
        loaded_params["b2"],
    )


def image_loader(path, output_path):
    W1, b1, W2, b2 = load_parameters()
    mobile_image_path = path
    mobile_input = preprocess_mobile_image(mobile_image_path)
    mobile_input = mobile_input.reshape((784, 1))
    predicted_output = make_predictions(mobile_input, W1, b1, W2, b2)
    plt.imshow(mobile_input.reshape((28, 28)), cmap="gray", extent=[0, 28, 28, 0])
    plt.axis("off")
    plt.savefig(output_path+ str(predicted_output))
