import numpy as np

from os import walk

from sklearn.datasets import load_svmlight_file
from sklearn.linear_model import SGDClassifier, LogisticRegression
from sklearn.metrics import *
from sklearn.model_selection import cross_val_score

import time
import pickle

def main():
    folders = prepFiles('features/')
    modelfolder = 'models/'
    end = 'part-00000'
    n = len(folders)

    k = int(n * 0.7)
    s = n - k
    models = []
    # models.append(LogisticRegression(C=0.01, class_weight="balanced"))
    models.append(SGDClassifier(loss="log", alpha=0.0001))
    # models.append(DecisionTreeClassifier(max_depth=20))
    # models.append(MLPClassifier())
    # models.append(RandomForestClassifier())
    methods = ["KF45_TunedSVM", "NN", "RF"]

    file1 = folders[0] + end

    for a in range(len(models)):
        start = time.time()
        model = models[a]

        print "Start training using method: " + methods[a]
        for i in range(k):
            file = folders[i] + end
            if (i + 1) % 100 == 1:
                X, Y = load_svmlight_file(file)
                X = X.toarray()
            else:
                X_train, Y_train = load_svmlight_file(file)

                X_train = X_train.toarray()

                try:
                    X = np.vstack([X, X_train])
                    Y = np.append(Y, Y_train)

                    if (i + 1) % 100 == 0:
                        print "Finished combining X & Y"
                        model.fit(X, Y)
                        print "Finished CV training w/ %d files" % (i + 1)

                        modelfile = modelfolder + methods[a] + "_" + str(i+1) + ".sav"
                        pickle.dump(model, open(modelfile, "wb"))

                        if (i + 1) % 500 == 0 or i == k - 1:
                            accs = []
                            aucs = []
                            precs = []
                            recs = []
                            f1s = []
                            for j in range(k, n):
                                file = folders[j] + end
                                X_test, Y_test = load_svmlight_file(file)
                                Y_pred = model.predict(X_test)
                                accs.append(accuracy_score(Y_test, Y_pred))
                                aucs.append(roc_auc_score(Y_test, Y_pred))
                                precs.append(precision_score(Y_test, Y_pred))
                                recs.append(recall_score(Y_test, Y_pred))
                                f1s.append(f1_score(Y_test, Y_pred))
                                print methods[a] + " - Predicted file no. " + str(j+1) + " out of " + str(n)

                            acc = round(np.mean(accs), 4)
                            auc = round(np.mean(aucs), 4)
                            prec = round(np.mean(precs), 4)
                            rec = round(np.mean(recs), 4)
                            f1 = round(np.mean(f1s), 4)

                            with open("scores_" + methods[a] + ".txt", "a") as file:
                                file.write("\n")
                                file.write("______________________________________________\n")
                                file.write("Average scores of " + str(len(folders) - k) + " test files\n")
                                file.write("Classifier: " + methods[a] + " trained with " + str(i + 1) + " training file(s)\n")
                                file.write("Accuracy: " + str(acc) + "\n")
                                file.write("AUC: " + str(auc) + "\n")
                                file.write("Precision: " + str(prec) + "\n")
                                file.write("Recall: " + str(rec) + "\n")
                                file.write("F1-score: " + str(f1) + "\n")
                                file.write("______________________________________________\n")
                                file.write("\n")
                                endtime = time.time()
                                file.write("Time taken: " + str(endtime - start) + " seconds.\n")
                except:
                    with open("log.txt", "a") as log:
                        log.write("\n")
                        log.write("Exception on fold %d, therefore skipped." % ((i + 1) / 80))

def prepFiles(path):
    return [f[0] + '/' for f in walk(path)][1:]

if __name__ == "__main__":
    main()
