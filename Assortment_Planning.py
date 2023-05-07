# -*- coding: utf-8 -*-
"""
Created on Tue Apr 25 12:03:19 202

@author: Akshays
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import optimize
import warnings
warnings.filterwarnings("ignore")
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
np.seterr(divide='ignore', invalid='ignore')
import time
st.set_option('deprecation.showPyplotGlobalUse', False)
np.seterr(divide='ignore', invalid='ignore')
from time import sleep
from time import time
import math
import webbrowser
from math import isnan
from pulp import *
from collections import Counter
from more_itertools import unique_everseen
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from scipy import optimize
import streamlit as st
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules
import time
from time import sleep
from PIL import Image

rad = st.sidebar.radio('Navigation',['Assortment','Shelf Space Optimization','Market Basket'])

if rad=='Assortment':
    
    try:
        
        st.header('ASSORTMENT PLANNING')
        
        st.image('Assortment.png',use_column_width=True)
        
        
        f = st.file_uploader('Upload a file',key='f4')
        if f is not None:
            
            df=pd.read_excel(f)
            df.head()
        
            dfl=np.log10(df.loc[:,'Space-Cookies':'Sales-Choco-Chip'])
        
            x=dfl[['Space-Cookies','Space-Digestive','Space-Choco-Chip']]
            y_sports=dfl[['Sales-Cookies']]
            y_luxury=dfl[['Sales-Digestive']]
            y_everyday=dfl[['Sales-Choco-Chip']]
        
            model_sports=LinearRegression()
            model_luxury=LinearRegression()
            model_everyday=LinearRegression()
        
            model_sports.fit(x,y_sports)
            model_luxury.fit(x,y_luxury)
            model_everyday.fit(x,y_everyday)
        
            sports_intercept=model_sports.intercept_[0]
            luxury_intercept=model_luxury.intercept_[0]
            everyday_intercept=model_everyday.intercept_[0]
        
            cols=x.columns
            sports_coef=dict(zip(cols,model_sports.coef_[0]))
            luxury_coef=dict(zip(cols,model_luxury.coef_[0]))
            everyday_coef=dict(zip(cols,model_everyday.coef_[0]))
            
            
        
            
        
            a,b,c = st.columns(3)
        
            with a:
               min1 = st.number_input("Min space for Cookies Biscuit")
            with b:
                min2 = st.number_input('Min space for Digestive Biscuits')
            with c:
                min3 = st.number_input('Min space for Choco-Chip Biscuits')
                
                
            Total_area = st.number_input('Total space')
        
                
            variables = [min1,min2,min3]
        
            def assortment(variables):
                sports_sales=((10**sports_intercept)*(variables[0]**sports_coef['Space-Cookies'])*(variables[1]**sports_coef['Space-Digestive'])*
                             (variables[2]**sports_coef['Space-Choco-Chip']))
                
                luxury_sales=((10**luxury_intercept)*(variables[0]**luxury_coef['Space-Cookies'])*(variables[1]**luxury_coef['Space-Digestive'])*
                             (variables[2]**luxury_coef['Space-Choco-Chip']))
                
                everyday_sales=((10**everyday_intercept)*(variables[0]**everyday_coef['Space-Cookies'])*(variables[1]**everyday_coef['Space-Digestive'])*
                             (variables[2]**everyday_coef['Space-Choco-Chip']))
                
                profit=(sports_sales*df['Avg_Margin_Cookies'][0])+(luxury_sales*df['Avg_Margin_Digestive'][0])+(everyday_sales*df['Avg_Margin_Choco_Chip'][0])
                
                return (-profit)
        
        
            def con(variables):
                return (variables[0]+variables[1]+variables[2]-Total_area)
        
        
        
            cons={'type':'eq','fun':con}
            bnds=((min1,Total_area),(min2,Total_area),(min3,Total_area))
        
        
        
        
        
            optim=optimize.minimize(assortment,variables,bounds=bnds,constraints=cons)
            Profit = (optim.fun)
            sports = (optim.x[0])
            luxury = (optim.x[1])
            everyday = (optim.x[2])
        
        
        
            if(st.button('Submit')):
                
                progress = st.progress(0)
                for i in range(100):
                    time.sleep(0.1)
                    progress.progress(i+1)
                    
                st.success('Optimization Completed')
                st.write('Max Weekly Profit: Rs',-Profit)
                st.write('Optimized space for Cookies Biscuits:',round(sports,2),'m2')
                st.write('Optimized space for Digestive Biscuits:',round(luxury,2),'m2')
                st.write('Optimized space for Choco-Chip Biscuits:',round(everyday,2),'m2')
                
    except:
        st.write('Please load the data to continue..')
        

if rad=='Shelf Space Optimization':
    st.header('SHELF SPACE OPTIMIZATION')

    st.image('Shelf_optimization.jpg',use_column_width=True)
    
    try:
    
        file1 = st.file_uploader('Upload the data',key='f1')
        file2 = st.file_uploader('Upload the current plan of shelf',key='f2')
        
    
        if (file1,file2) is not None:
            sales=pd.read_excel(file1,header=None)
            plan = pd.read_excel(file2,header=None)
            
            
            
            lift=sales.iloc[1:,1:]
            lift=np.array(lift)
            lift = lift.astype(np.int64)
    
            brands=sales.iloc[0:1,:]
            brands=np.array(brands)
            brands=np.delete(brands,0)
            brands=brands.tolist()
    
            ff=Counter(brands)
    
            all_brands=ff.items()
    
            #define the optimization function
    
            prob=LpProblem("SO",LpMaximize)
    
            #define decision variables
    
            dec_var=LpVariable.matrix("dec_var",(range(len(lift)),range(len(lift[0]))),0,1,LpBinary)
    
    
            #Compute the sum product of decision variables and lifts
    
            prodt_matrix=[dec_var[i][j]*lift[i][j] for i in range(len(lift))
    
            for j in range(len(lift[0]))]
    
    
            prob+=lpSum(prodt_matrix)
    
            order=list(unique_everseen(brands))
            order_map = {}
            for pos, item in enumerate(order):
    
                order_map[item] = pos
    
    
            #brands in order as in input file
    
            brands_lift=sorted(all_brands,key=lambda x: order_map[x[0]])
            
            st.header('Enter the shelf constraints')
            
            a,b,c = st.columns(3)
    
            with a:
               min1 = st.number_input("Maximum no of products in Shelf 1", min_value=0, max_value=5)
            with b:
                min2 = st.number_input('Maximum no of products in Shelf 2', min_value=0, max_value=5)
            with c:
                min3 = st.number_input('Maximum no of products in Shelf 3', min_value=0, max_value=5)
                
            c,d = st.columns(2)
    
            with c:
                min4 = st.number_input('Maximum no of products in Shelf 4', min_value=0, max_value=5)
            with d:
                min5 = st.number_input('Maximum no of products in Shelf 5', min_value=0, max_value=5)
                
            
            
    
            #DEFINE CONSTRAINTS
    
            #1) Each shelf can have only one product i.e. sum (each row)<=input constraints
    
    
            row_con=[min1,min2,min3,min4,min5]
    
            for i in range(len(lift)):
    
                prob+=lpSum(dec_var[i])<=row_con[i]
                
                
            #2) Each product can be displayed only on a limited number of shelves i.e. Column constraints
    
            #Constraints are given as
    
            dec_var=np.array(dec_var)
    
            col_data=[]
    
            for j in range(len(brands)):
    
                col_data.append(list(zip(*dec_var))[j])
    
                prob+=lpSum(col_data[j])<=1
                
                
            prob.writeLP("SO.lp")
    
            prob.solve()
    
            if(st.button('Submit')):
                
                
    
                progress = st.progress(0)
                for i in range(100):
                    sleep(0.1)
                    progress.progress(i+1)
                st.success('Shelf Optimization Completed')
                st.subheader('Information Provided')
                st.table(sales)
                st.subheader('Current Plan')
                st.table(plan)
                
                lift_plan=plan.iloc[1:,1:]
                lift_plan=np.array(lift_plan)
                lift_plan = lift_plan.astype(np.int64)
                
                plan_Matrix=[[0 for X in range(len(lift[0])) ] for y in range(len(lift))]
                r=[]
                for x in range(len(lift)):
                    for y in range(len(lift[0])):
                        if(lift_plan[x][y]==1):
                            plan_Matrix[x][y]=lift[x][y]
                            r.append(lift[x][y])
                            
                z = list(sales.iloc[0,1:])            
                dfv1 = pd.DataFrame(data = plan_Matrix,columns=z,index=['Shelf1','Shelf2','Shelf3','Shelf4','Shelf5'])
                st.subheader('Estimated Sales as per current plan')
                st.table(data=dfv1)
                st.write('Maximum Sales obtained as per current plan:',sum(r))
                
                
                
                Matrix=[[0 for X in range(len(lift[0]))] for y in range(len(lift))]
    
                for v in prob.variables():
                
                    Matrix[int(v.name.split("_")[2])][int(v.name.split("_")[3])]=v.varValue
                
                    matrix=np.int_(Matrix)
                
                w = list(sales.iloc[0,1:])
                dfs = pd.DataFrame(data = matrix,columns=w,index=['Shelf1','Shelf2','Shelf3','Shelf4','Shelf5'])
                st.subheader('Planned Shelf')
                dfs1 = dfs.astype(str)
                st.table(data=dfs1)
                
                val_Matrix=[[0 for X in range(len(lift[0])) ] for y in range(len(lift))]
                for x in range(len(lift)):
                    for y in range(len(lift[0])):
                        if(matrix[x][y]==1):
                            val_Matrix[x][y]=lift[x][y]
                            
                dfv = pd.DataFrame(data = val_Matrix,columns=w,index=['Shelf1','Shelf2','Shelf3','Shelf4','Shelf5'])
                st.subheader('Estimated Sales as per plan')
                st.dataframe(data=dfv)
                
                st.write('Maximum Sales obtained:',value(prob.objective))
                
                per_inc = round(((value(prob.objective)-sum(r))/sum(r))*100,2)
                
                st.write('Percentage increase in revenue:',per_inc,'%')
                
                st.subheader('Representation of shelf')
                table_data=matrix.tolist()
                col_names = ['GOODDAY', 'MOMS_MAGIC', 'HIDE_N_SEEK', 'BOURBON', 'MARIE']
                row_names = ['Shelf 1', 'Shelf 2', 'Shelf 3', 'Shelf 4', 'Shelf 5']
                images = [Image.open(f"{name}.png") for name in col_names]
                
                for i in range(len(images)):
                    for j in range(len(images)):
                        if table_data[i][j] == 1:
                            table_data[i][j] = images[j]
                        else:
                            table_data[i][j] = 0
                            
                dfss = pd.DataFrame(table_data, columns=col_names, index=row_names)
                
                dfss = pd.concat([pd.DataFrame([[0]*len(col_names)], columns=col_names, index=['New Row']), dfss], axis=0)
                dfss.insert(0, ' ', [0]*len(dfss))
                
                for i in range(len(dfss)):
                    cols = st.columns(len(dfss.columns))
                    for j, col in enumerate(dfss.columns):
                        if i == 0:
                            cols[j].markdown(f"<h6>{col}</h6>", unsafe_allow_html=True)
                        elif j == 0:
                            cols[j].write(dfss.index[i])
                        elif isinstance(dfss.iloc[i, j], Image.Image):
                            cols[j].image(dfss.iloc[i, j], width=100, caption='', use_column_width=True)
                        else:
                            cols[j].write(0)
                
                
    except:
        st.write('Please load the data to continue..')
                
            
            
            
if rad=='Market Basket':
    st.title('Market Basket Analysis')
    st.image('market.jpg',width=800)
    f=st.file_uploader('Upload file',key='f3')

    if f is not None:
        df=pd.read_excel(f)
        df['Item']=df['Brand']+'_'+df['Sub_Category']
        df=df[['Invoice_ID','Item']]
        for i in range(len(df)):
            df['Item'][i]=df['Item'][i].split('(')[0].rstrip()
        df['Quantity']=1
        df['Invoice_ID'] = df['Invoice_ID'].astype('str')
        
        mybasket=(df.groupby(['Invoice_ID','Item'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('Invoice_ID'))
        
        
        
        def my_encode_units(x):
            if x <= 0:
                return 0
            if x >= 1:
                return 1

        my_basket_sets = mybasket.applymap(my_encode_units)
        
        my_frequent_itemsets = apriori(my_basket_sets, min_support=0.01, use_colnames=True)
        
        my_rules = association_rules(my_frequent_itemsets, metric="lift", min_threshold=1)
        
        s=my_rules.sort_values("confidence",ascending=False).reset_index(drop=True)
        s=s[ (s['lift'] >= 1) &(s['lift'] <= 50) ]
        
        if(st.button('Submit')):
            progress=st.progress(0)
            for i in range(100):
                sleep(0.05)
                progress.progress(i+1)
                
            st.subheader('Possible Combinations')
            st.write(list(s['antecedents'][0])[0],'--------->',list(s['consequents'][0])[0])
            st.write(list(s['antecedents'][1])[0],'--------->',list(s['consequents'][1])[0])
            st.write(list(s['antecedents'][2])[0],'--------->',list(s['consequents'][2])[0])
            st.write(list(s['antecedents'][3])[0],'--------->',list(s['consequents'][3])[0])
