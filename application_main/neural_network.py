import numpy as np
import pandas as pd
import cv2
from matplotlib import pyplot as plt
import os

current_dir = os.getcwd()
data = pd.read_csv(current_dir + "\\train.csv")

data = np.array(data)
m, n = data.shape
np.random.shuffle(data)  # shuffle before splitting into dev and training sets

data_dev = data[0:1000].T
Y_dev = data_dev[0]
X_dev = data_dev[1:n]
X_dev = X_dev / 255.0

data_train = data[1000:m].T
Y_train = data_train[0]
X_train = data_train[1:n]
X_train = X_train / 255.0
_, m_train = X_train.shape


def init_params():
    w1 = np.random.rand(10, 784) - 0.5
    b1 = np.random.rand(10, 1) - 0.5
    w2 = np.random.rand(10, 10) - 0.5
    b2 = np.random.rand(10, 1) - 0.5
    return w1, b1, w2, b2


def ReLU(Z):
    return np.maximum(Z, 0)


def softmax(Z):
    return np.exp(Z) / sum(np.exp(Z))


def forward_prop(w1, b1, w2, b2, X):
    Z1 = w1.dot(X) + b1
    A1 = ReLU(Z1)
    Z2 = w2.dot(A1) + b2
    A2 = softmax(Z2)
    return Z1, A1, Z2, A2


def one_hot(Y):
    one_hot_Y = np.zeros((Y.size, Y.max() + 1))
    one_hot_Y[np.arange(Y.size), Y] = 1
    one_hot_Y = one_hot_Y.T
    return one_hot_Y


def deriv_ReLU(Z):
    return Z > 0


def backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y):
    m = Y.size
    one_hot_Y = one_hot(Y)
    dZ2 = A2 - one_hot_Y
    dW2 = 1 / m * dZ2.dot(A1.T)
    db2 = 1 / m * np.sum(dZ2)
    dZ1 = W2.T.dot(dZ2) * deriv_ReLU(Z1)
    dW1 = 1 / m * dZ1.dot(X.T)
    db1 = 1 / m * np.sum(dZ1)
    return dW1, db1, dW2, db2


def update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha):
    W1 = W1 - alpha * dW1
    b1 = b1 - alpha * db1
    W2 = W2 - alpha * dW2
    b2 = b2 - alpha * db2
    return W1, b1, W2, b2


def plot_cost(iterations, costs):
    plt.plot(iterations, costs)
    plt.title("Cost over Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Cost")
    plt.savefig("cost_plot.png")
    plt.show()


def plot_accuracy(iterations, accuracies):
    plt.plot(iterations, accuracies)
    plt.title("Accuracy over Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Accuracy")
    plt.savefig("accuracy_plot.png")
    plt.show()


def plot_weights_histogram(weights, layer_name):
    plt.figure(figsize=(8, 6))
    plt.hist(weights.flatten(), bins=50, color="skyblue", edgecolor="black")
    plt.title(f"{layer_name} Weights Distribution")
    plt.xlabel("Weight Value")
    plt.ylabel("Frequency")
    plt.savefig("weights_histogram.png")
    plt.show()


def plot_learning_rate(iterations, learning_rates):
    plt.plot(iterations, learning_rates)
    plt.title("Learning Rate over Iterations")
    plt.xlabel("Iterations")
    plt.ylabel("Learning Rate")
    plt.savefig("learning_rate_plot.png")
    plt.show()


def plot_confusion_matrix(y_true, y_pred, classes):
    from sklearn.metrics import confusion_matrix
    import seaborn as sns

    cm = confusion_matrix(y_true, y_pred)
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes, yticklabels=classes
    )
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.savefig("confusion_matrix.png")
    plt.show()


def get_predictions(A2):
    return np.argmax(A2, 0)


def get_accuracy(predictions, Y):
    return np.sum(predictions == Y) / Y.size


def gradient_descent(X, Y, alpha, iterations, decay_factor=0.95, decay_step=100):
    costs = []
    accuracies = []
    iteration_list = []
    learning_rates = []
    W1, b1, W2, b2 = init_params()

    for i in range(iterations):
        Z1, A1, Z2, A2 = forward_prop(W1, b1, W2, b2, X)
        dW1, db1, dW2, db2 = backward_prop(Z1, A1, Z2, A2, W1, W2, X, Y)
        W1, b1, W2, b2 = update_params(W1, b1, W2, b2, dW1, db1, dW2, db2, alpha)

        #         if i % decay_step == 0:
        #             alpha *= decay_factor

        if i % 50 == 0:
            print("Iteration: ", i)
            predictions = get_predictions(A2)
            print(get_accuracy(predictions, Y))
            accuracy = get_accuracy(predictions, Y)
            costs.append(
                -np.sum(one_hot(Y) * np.log(A2)) / m_train
            )  # Cross-entropy loss
            accuracies.append(accuracy)
            learning_rates.append(alpha)
            iteration_list.append(i)

    # plot_cost(iteration_list, costs)
    # plot_accuracy(iteration_list, accuracies)

    # dev_predictions = make_predictions(X_dev, W1, b1, W2, b2)
    # plot_confusion_matrix(Y_dev, dev_predictions, classes=np.unique(Y_train))
    #     plot_learning_rate(iteration_list, learning_rates)

    # plot_weights_histogram(W1, layer_name='First Layer')

    return W1, b1, W2, b2


# W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 0.1, 600)


def make_predictions(X, W1, b1, W2, b2):
    _, _, _, A2 = forward_prop(W1, b1, W2, b2, X)
    predictions = get_predictions(A2)
    return predictions


def test_prediction(index, W1, b1, W2, b2):
    current_image = X_train[:, index, None]
    prediction = make_predictions(X_train[:, index, None], W1, b1, W2, b2)
    label = Y_train[index]
    print("Prediction: ", prediction)
    print("Label: ", label)

    current_image = current_image.reshape((28, 28)) * 255
    plt.gray()
    plt.imshow(current_image, interpolation="nearest")
    plt.show()


def preprocess_mobile_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img_resized = cv2.resize(img, (28, 28))
    img_normalized = img_resized / 255.0
    img_flattened = img_normalized.flatten()
    return img_flattened


def save_parameters(W1, b1, W2, b2, path="saved_parameters.npz"):
    np.savez(path, W1=W1, b1=b1, W2=W2, b2=b2)
    print("Parameters saved successfully.")


# mobile_image_path = "8_3.jpg"
# mobile_input = preprocess_mobile_image(mobile_image_path)
# mobile_input = mobile_input.reshape((784, 1))

# Use the trained weights and biases to make predictions
# W1, b1, W2, b2 = gradient_descent(X_train, Y_train, 0.1, 700)
# save_parameters(W1, b1, W2, b2)
# dev_predictions = make_predictions(X_dev, W1, b1, W2, b2)
# get_accuracy(dev_predictions, Y_dev)
# mobile_prediction = make_predictions(mobile_input, W1, b1, W2, b2)
# print("Mobile Prediction:", mobile_prediction)
