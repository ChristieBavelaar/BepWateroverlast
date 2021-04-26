import sys
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor, BaggingRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.model_selection import RandomizedSearchCV
import time


def stemmerDataframe(): 
	print("Generate dataframe with stemmer")

	stemmer = SnowballStemmer('english')

	def str_stemmer(s):
		return " ".join([stemmer.stem(word) for word in s.lower().split()])

	def str_common_word(str1, str2):
		return sum(int(str2.find(word)>=0) for word in str1.split())

	df_all = pd.read_csv('./data/train.csv', encoding="ISO-8859-1")
	df_attr = pd.read_csv('./data/attributes.csv')
	df_pro_desc = pd.read_csv('./data/product_descriptions.csv')

	# Join all attribute values in one string
	df_attr_value = df_attr.astype(str)
	df_attr_value = df_attr.astype(str).groupby(df_attr.product_uid)['value'].apply(' '.join)
	df_attr_value = pd.DataFrame(df_attr_value)
	df_attr_value['product_uid'] = df_attr_value.index
	df_attr_value = df_attr_value.reset_index(drop=True)
	df_attr_value = df_attr_value.rename(columns={'value': 'attributes'})

	# Merge description and attributes with training data
	df_all = pd.merge(df_all, df_pro_desc, how='left', on='product_uid')
	df_all = pd.merge(df_all, df_attr_value, how='left', on='product_uid')

	# Stem attributes, search term, product title and product description
	df_attr_value['attributes'] = df_attr_value['attributes'].map(lambda x:str_stemmer(x))
	df_all['search_term'] = df_all['search_term'].map(lambda x:str_stemmer(x))
	df_all['product_title'] = df_all['product_title'].map(lambda x:str_stemmer(x))
	df_all['product_description'] = df_all['product_description'].map(lambda x:str_stemmer(x))

	# Create one attribute to hold the search term, product title, product description and attributes
	df_all['product_info'] = df_all['search_term']+"\t"+df_all['product_title']+"\t"+df_all['product_description'] + "\t" + df_all['attributes']

	# Drop rows with empty values
	df_all = df_all.dropna()

	# Add new attributes for number of words of the search term appear in the description, title or attributes
	df_all['word_in_title'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[1]))
	df_all['word_in_description'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[2]))
	df_all['word_in_attribute'] = df_all['product_info'].map(lambda x:str_common_word(str(x).split('\t')[0],str(x).split('\t')[3]))

	# Save working dataframe
	df_all.to_csv('dfAllTemp.csv')

	# # Drop unnecessary columns
	# df_all = df_all.drop(['search_term','product_title','product_description','product_info','attributes','id'],axis=1)
	# cols = [col for col in df_all.columns if 'Unnamed' not in col]
	# df_all = df_all[cols]

	# # Save dataframe to file
	# df_all.to_csv('dfAll.csv')

	return df_all

def idfDataframe():
	print("Generate dataframe with Tfidfvectorizer")

	df_all = pd.read_csv('./data/train.csv', encoding="ISO-8859-1")
	df_attr = pd.read_csv('./data/attributes.csv')
	df_pro_desc = pd.read_csv('./data/product_descriptions.csv')

	# Join all attribute values in one string
	df_attr_value = df_attr.astype(str)
	df_attr_value = df_attr.astype(str).groupby(df_attr.product_uid)['value'].apply(' '.join)
	df_attr_value = pd.DataFrame(df_attr_value)
	df_attr_value['product_uid'] = df_attr_value.index
	df_attr_value = df_attr_value.reset_index(drop=True)
	df_attr_value = df_attr_value.rename(columns={'value': 'attributes'})

	# Merge description and attributes with training data
	df_all = pd.merge(df_all, df_pro_desc, how='left', on='product_uid')
	df_all = pd.merge(df_all, df_attr_value, how='left', on='product_uid')

	# settings that you use for count vectorizer will go here 
	tfidf_vectorizer=TfidfVectorizer(use_idf=True) 
 
	# just send in all your docs here 
	tfidf_vectorizer_vectors=tfidf_vectorizer.fit_transform(df_all['attributes'])
	
	# # Stem attributes, search term, product title and product description
	# df_attr_value['attributes'] = df_attr_value['attributes'].map(lambda x:str_stemmer(x))
	# df_all['search_term'] = df_all['search_term'].map(lambda x:str_stemmer(x))
	# df_all['product_title'] = df_all['product_title'].map(lambda x:str_stemmer(x))
	# df_all['product_description'] = df_all['product_description'].map(lambda x:str_stemmer(x))

	# # Create one attribute to hold the search term, product title, product description and attributes
	# df_all['product_info'] = df_all['search_term']+"\t"+df_all['product_title']+"\t"+df_all['product_description'] + "\t" + df_all['attributes']

	# # Drop rows with empty values
	# df_all = df_all.dropna()

	# # Add new attributes for number of words of the search term appear in the description, title or attributes
	# df_all['word_in_title'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[1]))
	# df_all['word_in_description'] = df_all['product_info'].map(lambda x:str_common_word(x.split('\t')[0],x.split('\t')[2]))
	# df_all['word_in_attribute'] = df_all['product_info'].map(lambda x:str_common_word(str(x).split('\t')[0],str(x).split('\t')[3]))

	# Save working dataframe
	# Save dataframe to file
	df_all.to_csv('dfAllTemp.csv')

	# Drop unnecessary columns
	df_all = df_all.drop(['search_term','product_title','product_description','product_info','attributes','id'],axis=1)
	cols = [col for col in df_all.columns if 'Unnamed' not in col]
	df_all = df_all[cols]

	# Save dataframe to file
	df_all.to_csv('dfAll.csv')

def simpleAttributes(df_all):
	print('Generate dataframe with attributes not needing stemming.')
	
	df_attr = pd.read_csv('./data/attributes.csv')

	# Calculate length of query
	df_all['len_of_query'] = df_all['search_term'].map(lambda x:len(x.split())).astype(np.int64)

	# Calculate length of attributes
	df_all['len_of_attributes'] = df_all['attributes'].map(lambda x:len(x.split())).astype(np.int64)

	# Boolean value for brandname
	df_attr_brand = df_attr[df_attr['name']== 'MFG Brand Name']
	df_attr_brand['brandname'] = [1]*len(df_attr_brand['product_uid'])
	df_attr_brand = df_attr_brand.drop(columns=['name','value'])
	df_all = df_all.merge(df_attr_brand, on='product_uid', how='left')
	df_all['brandname'] = df_all['brandname'].fillna(0) 
	
	print(df_attr_brand)
	# Count number of bullet points
	df_attr_bullets = df_attr[df_attr['name'].str.contains('Bullet', na=False)]
	df_attr_bullets = df_attr_bullets.groupby('product_uid')['name'].count()
	df_attr_bullets = pd.DataFrame(df_attr_bullets)
	df_attr_bullets['product_uid'] = df_attr_bullets.index
	df_attr_bullets = df_attr_bullets.reset_index(drop=True)
	df_attr_bullets = df_attr_bullets.rename(columns={'name':'nrBullets'})
	df_all = df_all.merge(df_attr_bullets, on='product_uid', how='left')

	# # Drop unnecessary columns
	# df_all = df_all.drop(['search_term','product_title','product_description','product_info','attributes','id'],axis=1)
	# cols = [col for col in df_all.columns if 'Unnamed' not in col]
	# df_all = df_all[cols]

	# Save dataframe to file
	df_all.to_csv('dfAll2.csv')

	return df_all

def convertFractions(df, name):
	# confert all fractions t/n in the cells of column "name" in dataframe "df" to a floating point number
	df = df.copy()
	df = df.reset_index(drop=True)

	for i in df.index:
		# Text in cell to list
		lText = df.iloc[i][name].split()

		# Find all fractions
		fractions = [j for j in lText if '/' in j]
		for frac in fractions:
			# change fraction in lText
			k = lText.index(frac)
			temp = frac.split('/')
			try:
				temp = int(temp[0]) / int(temp[1])
				lText[k] = temp
			except:
				pass

		# convert back to list and change in dataframe
		strText = ' '.join([str(elem) for elem in lText])
		df.at[i,name]=strText
	return df

def addNrNumbers(df, name):
	# Add a column to the dataframe "df" containing the number of numbers in the columns "name" for that row of the dataframe
	df = df.copy()
	df = df.reset_index(drop=True)
	nrNumbers = []
	for i in df.index:
		# Text in cell to list
		lText = df.iloc[i][name].split()
		numbers = 0
		# Try to convert element of lText to a floating point number. If no error occurs this is a number.
		for j in lText:
			try:
				float(j)
				numbers+=1
			except:
				pass
		nrNumbers.append(numbers)

	columnname = name + "_nrNumbers"
	df[columnname] = nrNumbers
	return df

def addMeasurements(df, name):
	# Add a column to dataframe "df" containing all the ft and in measurements for the column "name" in that row

	df = df.copy()
	df = df.reset_index(drop=True)
	measurements1 = []
	for i in df.index:
		# Text to list
		lText = df.iloc[i][name].split()
		measurements = []

		# Find all sq ft and cu ft
		if 'sq' in lText or 'sq.' in lText or 'cu' in lText or 'cu.' in lText:
			npText = np.array(lText)
			indexes = np.where((npText == 'sq') | (npText=='cu') | (npText == 'sq.') | (npText=='cu.'))[0]
			for k in indexes:
				try:
					measurements.append(str(int(lText[k-1])) + lText[k].replace('.','') + lText[k+1][0:2])
				except:
					pass
		
		# Find all in and ft
		elif 'ft' in lText or 'ft.' in lText or 'in' in lText or 'in.' in lText:
			npText = np.array(lText)
			indexes = np.where((npText == 'ft') | (npText=='in') | (npText == 'ft.') | (npText=='in.'))[0]
			for k in indexes:
				try:
					measurements.append(str(int(lText[k-1])) + lText[k].replace('.',''))
				except:
					pass
		measurements1.append(measurements)
	columnname = name+'_measurements'
	df[columnname] = measurements1
	return df

def shortenUnits(df, name):
	# Shorten the units feet and inch to ft and in
	df = df.copy()
	df = df.reset_index(drop=True)
	for i in df.index:
		lText = df.iloc[i][name].split()
		if 'inch' in lText:
			npText = np.array(lText)
			indexes = np.where((npText == 'inch'))[0]
			for k in indexes:
				lText[k] = 'in'
		if 'feet' in lText:
			npText = np.array(lText)
			indexes = np.where((npText == 'feet'))[0]
			for k in indexes:
				lText[k] = 'ft'
		strText = ' '.join([str(elem) for elem in lText])
		df.at[i,name]=strText
	return df

def commonElements(df, name1, name2):
	# Find the number of common elements in the lists of column "name1" and "name2" in the dataframe
	df = df.copy()
	df = df.reset_index(drop=True)

	nrMeasurementMatch = []
	for i in df.index:
		setName1 = set(list(df.iloc[i][name1]))
		setIntersection = setName1.intersection(df.iloc[i][name2])
		nrMeasurementMatch.append(len(list(setIntersection)))
	df[name2+'_nrMeasurementMatch'] = nrMeasurementMatch
	return df

def measurementAttributes(df_all):
	print('Generate dataframe with attributes for measurements.')
	
	#df_all = pd.read_csv('dfAllTemp.csv')

	df_all = convertFractions(df_all,'search_term')
	df_all = shortenUnits(df_all, 'search_term')
	df_all = addNrNumbers(df_all, 'search_term')
	df_all = addMeasurements(df_all, 'search_term')

	df_all = convertFractions(df_all,'product_title')
	df_all = shortenUnits(df_all, 'product_title')
	df_all = addNrNumbers(df_all, 'product_title')
	df_all = addMeasurements(df_all, 'product_title')

	df_all = convertFractions(df_all,'product_description')
	df_all = shortenUnits(df_all, 'product_description')
	df_all = addNrNumbers(df_all, 'product_description')
	df_all = addMeasurements(df_all, 'product_description')

	df_all = convertFractions(df_all,'attributes')
	df_all = shortenUnits(df_all, 'attributes')
	df_all = addNrNumbers(df_all, 'attributes')
	df_all = addMeasurements(df_all, 'attributes')

	df_all = commonElements(df_all, 'search_term_measurements', 'product_title_measurements')
	df_all = commonElements(df_all, 'search_term_measurements', 'product_description_measurements')
	df_all = commonElements(df_all, 'search_term_measurements', 'attributes_measurements')

	df_all.to_csv('dfAllMeasurements.csv', index=False)
	return df_all

def prepareCSV():
	df_all = stemmerDataframe()
	print(df_all.dtypes)
	df_all = simpleAttributes(df_all)
	print(df_all.dtypes)
	df_all = measurementAttributes(df_all)
	print(df_all.dtypes)

	df_all = df_all.drop(columns=['id', 'product_uid','product_title', 'search_term', 'product_description', 'attributes', 'product_info', 'search_term_measurements', 'product_title_measurements', 'product_description_measurements', 'attributes_measurements' ])
	cols = [col for col in df_all.columns if 'Unnamed' not in col]
	df_all = df_all[cols]

	df_all.to_csv('dfAllFinal.csv', index=False)
	print(df_all.dtypes)

def SortImportances(importances, attributes):
	if len(importances) != len(attributes):
		print(len(importances))
		print(importances)
		return

	df = pd.DataFrame(importances)
	df = df.rename(columns= {0:"weights"})
	df["attributes"] = attributes
	df = df.sort_values(by=['weights'], ascending=False)
	return df
		
def multipleLinearRegression(inputFile):
	print("\n\nPerform multiple linear regression")

	# Read dataframe from file
	df_train = pd.read_csv(inputFile)
	df_train = df_train.astype(float)
	
	# Define labels and features
	y_train = df_train['relevance'].values
	X_train = df_train.drop(['relevance'],axis=1).values

	# Create train and test set
	X_split_train, X_split_test, y_split_train, y_split_test = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=42)
	t0 = time.time()
	regressor = LinearRegression()
	regressor.fit(X_split_train, y_split_train)

	y_pred = regressor.predict(X_split_test)
	t1 = time.time()

	print("Mean squared error: ", mean_squared_error(y_split_test,y_pred))
	print("Time elapsed: ", t1-t0)

	importances = regressor.coef_
	attributes = df_train.columns.tolist()
	attributes.	pop(0)
	print(SortImportances(importances, attributes))


def polynomialRegression(inputFile):
	print("\n\nPerform polynomial regression")

	# Read dataframe from file
	df_train = pd.read_csv(inputFile)
	df_train = df_train.astype(float)
	
	# Define labels and features
	y_train = df_train['relevance'].values
	X_train = df_train.drop(['relevance'],axis=1).values

	# Create train and test set
	X_split_train, X_split_test, y_split_train, y_split_test = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=42)
	t0 = time.time()

	poly_reg = PolynomialFeatures(degree = 2)
	X_poly_train = poly_reg.fit_transform(X_split_train)
	lin_reg = LinearRegression()
	lin_reg.fit(X_poly_train, y_split_train)

	X_poly_test = poly_reg.fit_transform(X_split_test)
	y_pred = lin_reg.predict(X_poly_test)

	t1 = time.time()

	print("Mean squared error: ", mean_squared_error(y_split_test,y_pred))
	print("Time elapsed: ", t1-t0)
	

def basicDecisionTreeRegression(inputFile):
	print("\n\nPerform decision tree regression")

	# Read dataframe from file
	df_train = pd.read_csv(inputFile)
	df_train = df_train.astype(float)
	
	# Define labels and features
	y_train = df_train['relevance'].values
	X_train = df_train.drop(['relevance'],axis=1).values

	# Create train and test set
	X_split_train, X_split_test, y_split_train, y_split_test = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=42)
	t0 = time.time()
	regressor = DecisionTreeRegressor()
	regressor.fit(X_split_train, y_split_train)

	y_pred = regressor.predict(X_split_test)
	t1 = time.time()

	print("Mean squared error: ", mean_squared_error(y_split_test,y_pred))
	print("Time elapsed: ", t1-t0)


def randomForest(inputFile):
	print("\n\nPerform random forest")

	# Read dataframe from file
	df_train = pd.read_csv(inputFile)
	df_train = df_train.astype(float)

	# Define labels and features
	y_train = df_train['relevance'].values
	X_train = df_train.drop(['relevance'],axis=1).values

	# Create train and test set
	X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=42)

	t0 = time.time()
	# Train random forest
	rf = RandomForestRegressor(n_estimators=15, max_depth=6, random_state=0)
	clf = BaggingRegressor(rf, n_estimators=45, max_samples=0.1, random_state=25)

	# Fit random forest
	clf.fit(X_train_1, y_train_1)

	# Generate predictions
	y_pred_1 = clf.predict(X_test_1)
	t1 = time.time()

	# Print result
	print("Mean squared error: ", mean_squared_error(y_test_1,y_pred_1))
	print("Time elapsed: ", t1-t0)

def evaluateHyperparameter(model, test_features, test_labels):
	predictions = model.predict(test_features)
	print("Mean squared error: ", mean_squared_error(predictions,test_labels))
	return 

def hyperparemeterOptimization(inputFile):
	# Read dataframe from file
	df_train = pd.read_csv(inputFile)
	df_train = df_train.astype(float)

	# Define labels and features
	y_train = df_train['relevance'].values
	X_train = df_train.drop(['relevance'],axis=1).values

	# Create train and test set
	X_train_1, X_test_1, y_train_1, y_test_1 = train_test_split(X_train, y_train, train_size=0.8, test_size=0.2, random_state=42)

	t0 = time.time()
	# Train random forest
	rf = RandomForestRegressor(n_estimators=15, max_depth=6, random_state=0)

	print(rf.get_params())
	# Number of trees in random forest
	n_estimators = [int(x) for x in np.linspace(start = 200, stop = 2000, num = 10)]
	# Number of features to consider at every split
	max_features = ['auto', 'sqrt']
	# Maximum number of levels in tree
	max_depth = [int(x) for x in np.linspace(10, 110, num = 11)]
	max_depth.append(None)
	# Minimum number of samples required to split a node
	min_samples_split = [2, 5, 10]
	# Minimum number of samples required at each leaf node
	min_samples_leaf = [1, 2, 4]
	# Method of selecting samples for training each tree
	bootstrap = [True, False]# Create the random grid
	random_grid = {'n_estimators': n_estimators,
				'max_features': max_features,
				'max_depth': max_depth,
				'min_samples_split': min_samples_split,
				'min_samples_leaf': min_samples_leaf,
				'bootstrap': bootstrap}
	
	# Random search of parameters, using 10 fold cross validation, 
	# search across 100 different combinations, and use all available cores
	rf_random = RandomizedSearchCV(estimator = rf, param_distributions = random_grid, n_iter = 10, cv = 10, verbose=2, random_state=42, n_jobs = -1)# Fit the random search model
	# Fit the random search model
	rf_random.fit(X_train_1, y_train_1)
	base_model = RandomForestRegressor(n_estimators = 10, random_state = 42)
	base_model.fit(X_train_1, y_train_1)
	base_accuracy = evaluateHyperparameter(base_model, X_train_1, y_train_1)

	print(rf_random.best_params_)
	best_random = rf_random.best_estimator_
	random_accuracy = evaluateHyperparameter(best_random, X_train_1, y_train_1)
	

if __name__ == '__main__':
	# prepareCSV()
	#randomForest("./dfAllFinal.csv")
	# polynomialRegression("./dfAllFinal.csv")
	# basicDecisionTreeRegression("./dfAllFinal.csv")
	# multipleLinearRegression("./dfAllFinal.csv")
	hyperparemeterOptimization('./dfAllFinal.csv')
