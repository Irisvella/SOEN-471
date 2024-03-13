# SOEN 471

## PROJECT SUMMARY

### Project definition and introduction

The main aim of this project is to create a Spark-based pipeline for anonymizing patient data to ensure that privacy and data protection laws are followed due to the sensitive nature of the information.

Furthermore, our objective extends to the development of an NLP model that predicts whether input data is anonymized or not. This model will look through the dataset and check if any names or otherwise identifying information were inadvertently inserted into the report from the radiologist.

## Model Design

### Dataset

Our dataset consists of two different types of data, the generated reports, and the MRI Dicom image. 

#### The Report
The reports contain the following feature vector (seven features):
- Age
- Location
- Ethnicity
- Study date
- PSA
	- PSA (Prostate-specific antigen)
- PI-RAD Score
	- A score indicating how likely an area is cancerous
- MR Model and Brand

#### The MRI Dicom Image
contains the MRI of the prostate, and patient metadata: name, sex, age, weight (kg), study date and time, study modality, study description, series date and time and series description and other metadata (around 100) that covers other information such as: manufacturer, software version and so on.


### Research Question

Given a set of input text, are we able to implement a robust anonymization pipeline, involving the anonymization of the data, and a classifier, to determine whether the data was successfully anonymized or not?

#### Data Anonymization
This step involves the anonymization of an input text.  The main tool we will be employing to anonymize the data is the spaCy open-source NLP library in conjunction with Presidio. Presidio is an open-source, Microsoft developed, data anonymization library that makes use of Regex, NLP, pattern validation and more to process and anonymize data. We will be using it with spaCy to anonymize the input text before it is passed to the classifier. 

##### Data Generation
Due to the sensitive nature of the information there is a limited-amount of data provided to us by the Rippen partner, therefore, we will be generating anonymized and unanonymized data and labelling it accordingly.

However, data generation can introduce heavy biases and we must therefore be careful to consider a variety of potential issues:

- The generated anonymized data cannot all contain blocked out values such as **** or ###. This is because the model would learn to identify these values rather than the identifying words.
- The variety of names, phone-numbers, locations, and other identifying information used in the process of generation. If we train the model on names that are only from one ethnicity it would most likely not work when presented with names from other ethnicities.

#### Classification Models 

##### NLP
The NLP classifier will function as an extra precaution measure in the data anonymization pipeline. It will take in an input text and determine whether or not it is anonymized. In other words, create a natural language processing (NLP) model that predicts whether input text is anonymized or not.
This classifier will be used in practice to verify that the data anonymization aspect of our work was successful. 

We will be making use of Named Entity Recognition (NER), a component of Natural Language Processing. NER will be used to tokenize words and classify them into two relevant groups (identifying: “name, location etc. '' or non-identifying). Two open source and free libraries will be used and compared : spaCy and Natural Language Toolkit (NLTK).

##### Naive Bayes
A traditional naive bayes classifier will also be trained on labelled data to classify identifying information. The NB classifier will be trained using Spark MLlib in order to take advantage of its distributed implementation.

#### Evaluation Method
To measure our models accuracy at labelling words, we can use precision, recall and f1 score regarding the labelling of the text output. A key observation when choosing the appropriate metric is the nature of the data, since this project deals with personal medical information then it is extremely important that the model has a high recall metric. In this scenario, recall would be a measure of how much data was successfully anonymized. However, it is also important to have a high precision score in order for the model to be remotely useful. The main evaluation metric will be the F1-Score. This will be useful since the dataset will likely contain a huge class imbalance (more non-identifying than identifying), highlighting the importance of f1. 

The performance of the NER and Naive Bayes classifiers will be weighed against each other based on the metrics discussed previously.


Appendix

Image 1 - Data Pipeline

![A diagram of a software company
Description automatically generated with medium confidence](file:///C:/Users/pablo/AppData/Local/Temp/msohtmlclip1/01/clip_image002.jpg)

Image 2 - Radiologist suggestion

![A screenshot of a medical report
Description automatically generated](file:///C:/Users/pablo/AppData/Local/Temp/msohtmlclip1/01/clip_image004.png)
