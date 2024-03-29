from tqdm import tqdm
from tqdm import trange
import numpy as np
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

import cnn_builder

def generate_model(X, y):

    # scaler = preprocessing.StandardScaler().fit(X)
    # X_scaled = scaler.fit_transform(X)
    # pca = PCA(n_components= 0.999).fit(X_scaled)
    # X = pca.transform(X_scaled)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 初始化三种分类器
    svm_classifier = LinearSVC(dual='auto', max_iter= 10000, tol=1e-3)
    
    logistic_classifier = LogisticRegression(max_iter=10000, solver='newton-cg')
    
    bayes_classifier = GaussianNB()
    # cnn = cnn_builder.train_cnn_model(X_train, y_train)

    
    # 训练并测试SVM模型
    svm_classifier.fit(X_train, y_train)
    svm_pred = svm_classifier.predict(X_test)
    svm_accuracy = accuracy_score(y_test, svm_pred)
    print("svm finished")
    # 训练并测试Logistic回归模型
    logistic_classifier.fit(X_train, y_train)
    logistic_pred = logistic_classifier.predict(X_test)
    logistic_accuracy = accuracy_score(y_test, logistic_pred)
    print("log finished")
    # 训练并测试贝叶斯分类器
    bayes_classifier.fit(X_train, y_train)
    bayes_pred = bayes_classifier.predict(X_test)
    bayes_accuracy = accuracy_score(y_test, bayes_pred)
    print("NB finished")
    # cnn.fit(X_train, np.asarray(y_train, dtype=np.int64))
    # cnn_pred = cnn.predict(X_test)
    # cnn_accuracy = accuracy_score(y_test, cnn_pred)

    # 找出准确率最高的模型
    best_model = None
    best_accuracy = 0.0
    if svm_accuracy > best_accuracy:
        best_accuracy = svm_accuracy
        best_model = svm_classifier
    if logistic_accuracy > best_accuracy:
        best_accuracy = logistic_accuracy
        best_model = logistic_classifier
    if bayes_accuracy > best_accuracy:
        best_accuracy = bayes_accuracy
        best_model = bayes_classifier
    # if cnn_accuracy > best_accuracy:
    #     best_accuracy = cnn_accuracy
    #     best_model = cnn

    # 输出准确率并返回最佳模型
    print("SVM:", svm_accuracy)
    print("Logistic:", logistic_accuracy)
    print("Naive Bayes:", bayes_accuracy)
    # print("CNN:", cnn_accuracy)
    return best_model    



def int_model(X, pca_model, W_model, REM_model, N_model, model_12, model_34):
    len = X.shape[0]
    # Y_pred = np.zeros(len)
    Y_pred = []

    X = pca_model.transform(X)

    for i in trange(len):
        x = X[i:]
        y_pred = W_model.predict(x)
        if y_pred[0] == 0:
            Y_pred.append(0)
            continue
        y_pred = REM_model.predict(x)
        if y_pred[0] == 1:
            Y_pred.append(5)
            continue
        y_pred = N_model.predict(x)
        if y_pred[0] == 0:
            y_pred = model_12.predict(x)
            if y_pred[0] == 0:
                Y_pred.append(1)
            else:
                Y_pred.append(2)
        else:
            y_pred = model_34.predict(x)
            if y_pred[0] == 0:
                Y_pred.append(3)
            else:
                Y_pred.append(4)            
    return np.array(Y_pred)