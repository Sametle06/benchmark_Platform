# -*- coding: utf-8 -*-
"""
Created on Fri May 22 19:01:23 2020

@author: Sameitos
"""

import numpy as np

class ScalerNormalizer():
    """
    Description:This class has 5 methods in which normalizer stands to 
                           normalize the data. Others are for scaling
    
    
    Parameters
    ----------
        train: train feature matrix
        
    Return
    ------
        scaled_train: feature matrix which function was applied
        scaler: a model to scale other dataset like test datatest
        
    """
    def normalizer(self,train,norm = 'l2'):
        #normalizer for the data
        from sklearn.preprocessing import Normalizer
        
        scaler = Normalizer(norm = norm)
        scaled_train = scaler.fit_transform(train)
        return scaled_train,scaler
  

      
    def standard_scaler(self,train):
        #Standard scaler or z-score scaler on any data 
        from sklearn.preprocessing import StandardScaler
        
        scaler = StandardScaler()
        scaled_train = scaler.fit_transform(train)
        return scaled_train,scaler
        

        
    def maxabs_scaler(self,train):
        #for the sparse data
        from sklearn.preprocessing import MaxAbsScaler
        
        scaler = MaxAbsScaler()
        scaled_train = scaler.fit_transform(train)
        return scaled_train,scaler
        

    
    def minmax_scaler(self,train):
        #for the data has small std and is not gaussian dist
                      
        from sklearn.preprocessing import MinMaxScaler
        
        scaler = MinMaxScaler()
        scaled_train = scaler.fit_transform(train)
        return scaled_train,scaler 
        

    
    def robust_scaler(self,train):
        #for the data to eleminate outliers
        from sklearn.preprocessing import RobustScaler
        
        scaler = RobustScaler()
        scaled_train = scaler.fit_transform(train)
        return scaled_train,scaler 
        

def scale_methods(X_train,scale_type = 'Standard_Scaler'):
    
    s = ScalerNormalizer()

    scaler_ways = {'Normalizer':s.normalizer,'Standard_Scaler':s.standard_scaler,
                   'MaxAbs_Scaler':s.maxabs_scaler,'MinMax_Scaler': s.minmax_scaler,
                   'Robust Scaler': s.robust_scaler}
    
    X_train,scaler = scaler_ways[scale_type](X_train)
    
    return X_train,scaler
