# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 01:00:05 2021

@author: Sameitos
"""

import os
import random
from ..utils import separator, regress_data_import, clssfy_data_import
from datetime import datetime 

class rgs_data_loader():
    
    def __init__(self,ratio,protein_feature ,set_type):
        self.ratio = ratio
        self.protein_feature = protein_feature
        self.set_type = set_type    
    
    def get_data(self,data_name):
        pPath = os.path.split(os.path.realpath(__file__))[0]
        file_path = pPath + '/dti_dataset/' + data_name
        
        if self.set_type not in ['random','compound','target','compound_target']:
         	raise AttributeError('Please enter correct set_type. Options are: "random, compound, target, compound_target"')
        if self.protein_feature not in ['paac', 'aac', 'eaac', 'gaac', 'ctdc','ctriad','socnumber']:
         	raise AttributeError('Please enter correct protein_feature. Options are: "paac, aac, eaac, gaac, ctdc, ctriad, socnumber"')

        file_x = file_path + '/feature_' + self.protein_feature + '.txt'
        file_y = file_path + '/label_' + self.protein_feature + '.txt'
        
        if self.set_type != 'random':
            indices_file = file_path + '/' + self.set_type + '_indices.txt'
            data_files = [file_x,file_y,self.indices_file]
            
            for i in data_files:
                if not os.path.isfile(i):
                    raise FileNotFoundError(f'The file {i} does not exist')
        
            X,y = regress_data_import(indices_file = indices_file,xf = file_x,yf = file_y)

        elif self.set_type == 'random':
            data_files = [file_x,file_y]
            
            for i in data_files:
                if not os.path.isfile(i):
                    raise FileNotFoundError(f'The file {i} does not exist')
        
            X,y = regress_data_import(xf = file_x,yf = file_y)

        if not self.ratio:
            return X,y
        else:
            try:
                return separator(ratio = self.ratio, X = X, y = y)
            except:
                raise AttributeError('Please enter ratio value in true type. Options: "float, List"')
    
class cls_data_loader():
    
    def __init__(self,ratio,protein_feature,main_set,set_type,label,pre_determined):
        self.ratio = ratio
        self.protein_feature = protein_feature
        self.set_type = set_type
        self.label = label
        self.pre_determined = pre_determined
        self.main_set = main_set
        
    def get_data(self,data_name):
        pPath = os.path.split(os.path.realpath(__file__))[0]
        file_path = pPath + '/' + self.main_set + '/' + data_name
        
        if self.set_type not in ['random','target']:
         	raise AttributeError('Please enter correct set_type. Options are: "random, target"')
        if self.protein_feature not in ['paac', 'aac', 'eaac', 'gaac', 'ctdc','ctriad','socnumber']:
         	raise AttributeError('Please enter correct protein_feature. Options are: "paac, aac, eaac, gaac, ctdc, ctriad, socnumber"')
        
        if not self.pre_determined:

            pos_file = file_path + '/' + self.set_type + '_positive_' + self.protein_feature + '.txt'
            neg_file = file_path + '/' + self.set_type + '_negative_' + self.protein_feature + '.txt'

            data_files = [neg_file,pos_file]
            for i in data_files:
                if not os.path.isfile(i):
                    if self.set_type == 'target':
                        raise FileNotFoundError(f'The file {i} has not been uploaded yet or data size is not enough')
                    else:
                        raise FileNotFoundError(f'The file {i} has not been uploaded yet')

            pX,py,nX,ny,X,y = clssfy_data_import(pos_file = pos_file,neg_file = neg_file, label = self.label)


            if self.label == 'positive':
                return pX,py
            elif self.label == 'negative':
                return nX,ny
            
            else:
                X,y = zip(*random.shuffle(list(zip(X,y))))
                
                try:
                    separator(ratio = self.ratio,X = X,y =y)
                except:
                    raise AttributeError('Please enter ratio value in true type. Options: "None, float, List"')
        else:
        
            pos_file = file_path + '/' + self.set_type + '_positive_' + self.protein_feature + '.txt'
            neg_file = file_path + '/' + self.set_type + '_negative_' + self.protein_feature + '.txt'

            train_pos_idx = file_path + '/' + self.set_type + '_positive_train_indices.txt'
            train_neg_idx = file_path + '/' + self.set_type + '_negative_train_indices.txt'

            test_pos_idx = file_path + '/' + self.set_type + '_positive_test_indices.txt'
            test_neg_idx = file_path + '/' + self.set_type + '_negative_test_indices.txt'



            data_files = [pos_file, neg_file, train_pos_idx, train_neg_idx, test_pos_idx, test_neg_idx]
            
            for i in data_files:
                if not os.path.isfile(i):
                    if self.set_type == 'target':
                        raise FileNotFoundError(f'The file {i} has not been uploaded yet or data size is not enough')

                    else:
                        raise FileNotFoundError(f'The file {i} has not been uploaded yet')
            
            
            tpX,tpy,tnX,tny,tX,ty = clssfy_data_import(pos_file = pos_file, neg_file = neg_file, 
                pos_indices = train_pos_idx,neg_indices = train_neg_idx,
                label = self.label)
            tepX,tepy,tenX,teny,teX,tey = clssfy_data_import(pos_file = pos_file, neg_file = neg_file, 
                pos_indices = test_pos_idx,neg_indices = test_neg_idx,
                label = self.label)


            if self.label == 'positive':
                return tpX,tepX,tpy,tepy
            elif self.label == 'negative':
                return tnX,tenX,tny,teny
            
            else:
            
                trdn = list(zip(tX,ty))
                random.shuffle(trdn)
                tX,ty = zip(*trdn)
            
                terdn = list(zip(teX,tey))
                random.shuffle(terdn) 
                teX,tey = zip(*terdn)
            
                if not self.ratio:
                    return tX,teX,ty,tey
                    
                if type(self.ratio) == float:
                    tX,vX,ty,vy = separator(ratio = self.ratio,X = tX,y = ty)
                    return tX,teX,vX,ty,tey,vy
                
                else:
                    raise AttributeError('Please enter ratio value in true type. Options: "None, float" for pre_determined = True')
                    