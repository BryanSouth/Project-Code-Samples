# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 14:26:16 2020

@author: Bryan
"""

import numpy as np
from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.pipeline import Pipeline
from tsfresh.transformers import RelevantFeatureAugmenter
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report


def init():
    #Importing the dataset and setting it up as a dataframe for tsfresh to use
    
    data = np.load('data_ts.npy')
    df_data = pd.DataFrame(data, columns = ['id','time', 'a', 'b', 'c', 'd'])
    
    return df_data

def main():
    #Creating the pipeline for feature extraction and input into the Random Forest for training and testing
    pipeline = Pipeline([('augmenter', RelevantFeatureAugmenter(column_id='id', column_sort='time')),
            ('classifier', RandomForestClassifier())])

    #Loading in the data
    df_data = init()
    
    #Separating x and y and classification training and testing set
    df_x_data = df_data.loc[:, df_data.columns != 'd']
    y = df_data.loc[:, df_data.columns == 'd']
    X = pd.DataFrame(index=y.index)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y)

    #Extracting statistical features and training
    pipeline.set_params(augmenter__timeseries_container=df_x_data)
    pipeline.fit(X_train, y_train)
    
    #Predicting on test set and outputting performance metrics
    y_pred = pipeline.predict(X_test)
    print(classification_report(y_test, y_pred))
        
if __name__ == "__main__":
    main()



