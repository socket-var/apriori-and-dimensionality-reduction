import part1_helpers
import algos


filenames = input("Enter the names of the files without .txt:")
algorithms = input("Enter the list of algorithms:")

files_list = [name.strip() for name in filenames.split(",")]
algos_list = [algo.strip().lower() for algo in algorithms.split(",")]

data_list = []

for filename in files_list:
    data = part1_helpers.import_txt(filename)

    data_list.append((data, filename))


for data, filename in data_list:
    X, y, unique_labels = data
    for algo in algos_list:
        if algo == "pca":
            new_X = algos.pca(X)
        if algo == "svd":
            new_X = algos.svd(X)
        if algo == "tsne":
            new_X = algos.tsne(X)

        part1_helpers.scatter(
            new_X[:, 0], new_X[:, 1], y, unique_labels, algo, filename)
