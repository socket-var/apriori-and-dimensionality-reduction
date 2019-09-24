import pandas as pd
import matplotlib.pyplot as plt


def import_txt(filename):
    data = pd.read_csv("input/{}.txt".format(filename), sep="\t", header=None)

    X = data.iloc[:, :-1]
    y = data.iloc[:, -1]

    unique_labels = list(set(y))

    return X, y, unique_labels


def scatter(X1, X2, labels, unique_labels, algo, filename):

    unique_encoded = [i for i in range(len(unique_labels))]

    colors = [plt.cm.jet(float(i)/max(unique_encoded))
              for i, u in enumerate(unique_labels)]

    plt.title("Algorithm: {} Dataset: {}".format(algo, filename))

    for i, u in enumerate(unique_labels):
        xi = [X1[j] for j in range(len(X1)) if labels[j] == u]
        yi = [X2[j] for j in range(len(X2)) if labels[j] == u]
        plt.scatter(xi, yi, c=colors[i], label=str(u))

    plt.legend()

    # plt.show()

    plt.savefig("results/{}_{}.png".format(algo, filename))
    plt.close()
