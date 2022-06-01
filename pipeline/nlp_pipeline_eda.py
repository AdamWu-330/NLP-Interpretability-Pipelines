# -*- coding: utf-8 -*-
"""nlp_pipeline_EDA.py

The module for Exploratory Data Analysis(EDA)
"""

import pandas as pd
import re
import nltk
import numpy as np
from nltk.tokenize import WordPunctTokenizer
from nltk.stem import WordNetLemmatizer
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import RandomOverSampler

class EDA:
  def __init__(self, raw_data, label_col=None):
    # the raw data is a csv file by default
    self.raw_data = raw_data

    # read the raw data into a DataFrame
    self.__original_data = pd.read_csv(self.raw_data, error_bad_lines=False, engine='python', encoding='utf-8')

    #if label_col is None, unsupervised task
    self.__label_col = label_col 

  # read from the stored data object into csv/array, etc. To be implemented later
  def __unpack_data(self):
    return None

  # convert the cleaned data into a data object. To be implemented later
  def __pack_data(self):
    return None
  
  def __display_original_data(self, num_samples=5):
    print("Displaying the first {} samples of the dataset: ".format(num_samples))
    print(self.__original_data.head(num_samples))
  
  def __preprocess_text(self, text_index, to_lowercase, remove_html_tags=True, remove_html_list=['<br />'], remove_nonword_chars=True, remove_stopwords=True, stowords_language='english', 
                        customized_stopwords=None, lemmatize=False):
    print('\n')
    print('Start text preprocessing: ')
    text_lst = self.__original_data[text_index].tolist()
    if to_lowercase:
      print('--------------------------')
      print('Converting to lowercase...')
      for i in range(len(text_lst)):
        text_lst[i] = text_lst[i].strip().lower()

    if remove_html_tags:
      print('--------------------------')
      print('Removing html tags...')
      for i in range(len(text_lst)):
        text_lst[i] = re.sub(r'<br />', '', text_lst[i])

    if remove_nonword_chars:
      print('--------------------------')
      print('Removing nonword characters...')
      for i in range(len(text_lst)):
        text_lst[i] = re.sub(r'[\W]', ' ', text_lst[i])
    
    if remove_stopwords:
      print('--------------------------')
      print('Removing stopwords...')
      if customized_stopwords==None:
        nltk.download('stopwords')
        nltk.download('wordnet')
        stop_words = nltk.corpus.stopwords.words(stowords_language)
      else:
        stop_words = customized_stopwords
      for i in range(len(text_lst)):
        tokens = WordPunctTokenizer().tokenize(text_lst[i])
        tokens_cleaned = [i for i in tokens if i not in stop_words]
        text_lst[i] = ' '.join(tokens_cleaned)
      
    text_df = pd.DataFrame(text_lst, columns=[text_index])
    self.__original_data[text_index] = text_df
    
    print('Text preprocessing completed.')
    print('\n')

  def __encode_label(self, label_encoding_dict=None):
    if label_encoding_dict==None:
      le = LabelEncoder()
      self.__original_data[self.__label_col] = le.fit_transform(self.__original_data[self.__label_col].values)
    else:
      self.__original_data[self.__label_col] = self.__original_data[self.__label_col].replace(label_encoding_dict)

  def __oversampling(self):
    feature_col_lst = self.__original_data.columns.tolist()
    feature_col_lst.remove(self.__label_col)

    ros = RandomOverSampler(random_state=0)
    features_resampled, label_resampled = ros.fit_resample(self.__original_data.drop(columns=[self.__label_col], axis=1), 
                                                           self.__original_data.drop(columns=feature_col_lst, axis=1))

    self.__original_data = pd.concat([features_resampled, label_resampled], axis=1)

  # display the original data
  def display_original_data(self, num_samples=5):
    return self.__display_original_data(num_samples)

  # retrieve the DataFrame object for the data
  def get_data(self):
    return self.__original_data

  # retrieve the lable column name
  def get_lable_column(self):
    return self.__label_col

  # delete the last n samples in the data
  def delete_samples_from_data(self, number=100):
    self.__original_data = self.__original_data.head(-number)

  # preprocess the given text, usually by specifying the column name
  def preprocess_text(self, text_index, to_lowercase=True, remove_html_tags=True, remove_html_list=['<br />'], remove_nonword_chars=True, remove_stopwords=True, stowords_language='english', 
                         customized_stopwords=None, lemmatize=False):
    return self.__preprocess_text(text_index, to_lowercase, remove_html_tags, remove_html_list, remove_nonword_chars, remove_stopwords, stowords_language,
                                  customized_stopwords, lemmatize)
    
  # encode the label
  # label_encoding_dict: a dictionaray for encoding the label
  # if given, encode the label as it is; if not given, encode the label using LabelEncoder by default
  def encode_label(self, label_encoding_dict=None):
    return self.__encode_label(label_encoding_dict)

  # class balancing, use oversampling by default
  def balance_class(self, balance_method='oversampling'):
    return self.__oversampling()
