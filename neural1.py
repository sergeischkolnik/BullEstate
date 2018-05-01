from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix
import scipy
import models

print("loading data")
props = models.readVentaDpto()
print("Loaded " + str(len(props)) + " propiedades")
#cancer = load_breast_cancer()

y=[]
X=[]
print("converting data")
for prop in props:
    temp = []
    if prop.minMet=='-' or prop.maxMet=='-' or prop.lat=='-' or prop.lon=='-' or prop.dorms=='-' or prop.banios=='-':
        continue
    y.append(prop.precio)
    temp.append(prop.minMet)
    temp.append(prop.maxMet)
    temp.append(prop.lat)
    temp.append(prop.lon)
    temp.append(prop.dorms)
    temp.append(prop.banios)
    X.append(temp)

#X = cancer['data']
#y = cancer['target']

print("splitting data")

X_train, X_test, y_train, y_test = train_test_split(X, y)

scaler = StandardScaler()
# Fit only to the training data
scaler.fit(X_train)

# Now apply the transformations to the data:
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

print("runing nn")
mlp = MLPClassifier(hidden_layer_sizes=(30,30,30),verbose=True,max_iter=1000, tol=0.000001)

mlp.fit(X_train,y_train)

print("done")
predictions = mlp.predict(X_test)

#print(confusion_matrix(y_test,predictions))
#print(classification_report(y_test,predictions))

sumaDelta = 0
for i in range(0,len(predictions)-1):
    diff = predictions[i]-y_test[i]
    #print(str(diff))
    diffPos = abs(diff)
    sumaDelta += diffPos

promedio = sumaDelta/len(predictions)
print("prom:"+str(promedio))
