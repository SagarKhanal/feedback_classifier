

#Importing Datasets Offline
import sklearn.datasets as skd

# Positive and Negative Category
categories = ['com.positive','com.negative']

# Training Datas of Feedback
feedback_train = skd.load_files('feedback/train',categories=categories,encoding='ISO-8859-1')

#Testing Datas of Feedback
feedback_test = skd.load_files('feedback/test',categories=categories,encoding='ISO-8859-1')

# Train and Test are formed in dict files

## feedback_test.keys()          
## feedback_train.target_names

# => ['com.negative','com.positive']

#Word Count Vectorizer 
from sklearn.feature_extraction.text import CountVectorizer
count_vect = CountVectorizer()

X_train_tf = count_vect.fit_transform(feedback_train.data)
# X_train_tf.shape

#Tfidf Transformer (Term Frequency)
from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer()

X_train_tfidf = tfidf_transformer.fit_transform(X_train_tf)

#X_train_tfidf.shape


# MultinomialNB used for the features with discrete values like word count 1,2,3.
from sklearn.naive_bayes import MultinomialNB
clf = MultinomialNB().fit(X_train_tfidf,feedback_train.target)


#Count Vectorizer and TfiDF for Test data
X_test_tf = count_vect.transform(feedback_test.data)
X_test_idf = tfidf_transformer.transform(X_test_tf)

#prediction value for test data
predicted = clf.predict(X_test_idf)

#Checking Accuracy by comparing test target and predicted value
from sklearn import metrics
from sklearn.metrics import accuracy_score

# print("Accuracy:",accuracy_score(feedback_test.target,predicted))

# Classification for New Feedbacks

new_feedback = ['I am not satisfied']
#Count Vectorization
X_new_counts = count_vect.transform(new_feedback)
#TFIDF (Term Frequency)
X_new_tfidf= tfidf_transformer.transform(X_new_counts)

predicted=clf.predict(X_new_tfidf)

#Gives the array value of predicted classification
print(predicted)

classified_value = ''

if(1 in predicted):
    classified_value="Positive"
else:
    classified_value="Negative"

# classified_value


#START OF API

from flask import  Flask, request
from flask_restful import  Resource, Api
# from json import  dumps
from flask import jsonify

app = Flask(__name__)
api = Api(app)

class Classfier(Resource):
    def get(self):
        result = {'classification':[ classified_value]}
        return jsonify(result)


api.add_resource(Classfier,'/classify') #Route 1

if __name__ == '__main__':
    app.run(port='5002')


#END OF API











