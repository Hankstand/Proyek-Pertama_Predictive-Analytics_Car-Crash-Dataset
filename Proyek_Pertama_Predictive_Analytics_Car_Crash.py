# -*- coding: utf-8 -*-
"""PA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1_3rsgzHlE3JgTZgoZu4qE3Xv6SR4hATO

## 1. Import Library
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import calendar
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.model_selection import cross_val_score

"""## 2. Load Dataset

### 2.1 Mengecek tipe encoding file
"""

import chardet

rawdata = open('data/monroe county car crach 2003-2015.csv', 'rb').read()
result = chardet.detect(rawdata)
encoding = result['encoding']

print(f"Encoding file adalah: {encoding}")

"""### 2.2 Memanggil dataframe"""

data = pd.read_csv("data/monroe county car crach 2003-2015.csv", delimiter=',', encoding='ISO-8859-1')
data

"""### 2.3 Mengecek dimensi dari data struktur"""

data.shape

"""## 3. Data Understanding

Attribute  | Keterangan
------------- | -------------
Year | merepresentasikan tahun kejadian tabrakan
Month | merepresentasikan bulan kejadian tabrakan
Day | merepresentasikan hari kejadian tabrakan
Weekend? | merepresentasikan apakah tabrakan terjadi di akhir pekan atau bukan
Hour | merepresentasikan jam kejadian tabrakan.       
Collision Type | merepresentasikan jenis tabrakan
Injury Type  | merepresentasikan jenis cedera
Primary Factor |merepresentasikan faktor utama penyebab tabrakan
Reported_Location |merepresentasikan lokasi kejadian tabrakan
Latitude |merepresentasikan garis lintang lokasi kejadian
Longitude |merepresentasikan garis bujur lokasi kejadian

### 3.1 Mengecek tipe data pada setiap atribut
"""

data.info()

"""### 3.2 Mengecek deskripsi data pada dataframe"""

data.describe(include='object')

"""### 3.3 Mengecek duplikasi pada dataframe"""

data.duplicated().sum()

"""### 3.4 Mengecek missing value pada setiap atribut pada dataframe"""

data.isnull().sum()

"""### 3.5 Mengecek jumlah baris data dari setiap nilai unik"""

data['Year'].value_counts().sort_index(ascending=False)

data['Month'].value_counts().sort_index(ascending=False)

data['Day'].value_counts().sort_index(ascending=False)

data['Weekend?'].value_counts().sort_index(ascending=False)

data['Hour'].value_counts().sort_index(ascending=False)

data['Collision Type'].value_counts().sort_index

data['Injury Type'].value_counts().sort_index

data['Primary Factor'].value_counts().sort_index

data['Reported_Location'].value_counts().sort_index

data['Longitude'].value_counts().sort_index

"""## 4. Visualisasi Data

### 4.1 Visualisasi distribusi setiap atribut
"""

plt.figure(figsize=(16, 4))
data['Year'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribusi Kecelakaan per Tahun')
plt.xlabel('Tahun')
plt.ylabel('Jumlah Kecelakaan')
plt.xticks(rotation=0)
plt.show()

plt.figure(figsize=(16, 4))
months = data['Month'].value_counts().sort_index().index
data['Month'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribusi Kecelakaan per Bulan')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Kecelakaan')
plt.xticks(range(0, 12), rotation=0, labels=[calendar.month_abbr[i] for i in range(1, 13)])
plt.show()

bahasa = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]

plt.figure(figsize=(16, 4))
days = data['Day'].value_counts().sort_index().index
data['Day'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribusi Kecelakaan per Hari')
plt.xlabel('Hari')
plt.ylabel('Jumlah Kecelakaan')
plt.xticks(range(0, 7), rotation=0, labels=bahasa)
plt.show()

plt.figure(figsize=(16, 4))
hours = data['Hour'].value_counts().sort_index().index
data['Hour'].value_counts().sort_index().plot(kind='bar')
plt.title('Distribusi Kecelakaan per Jam')
plt.xlabel('Jam')
plt.ylabel('Jumlah Kecelakaan')
plt.xticks(range(24), rotation=0, labels=[str(i) for i in range(1, 25)])
plt.show()

plt.figure(figsize=(16, 4))
sns.countplot(data['Weekend?'])
plt.title(f'Distribusi Kecelakaan pada akhir minggu atau tidak')
plt.xlabel('Jumlah Kecelakaan')
plt.ylabel('Weeked?')
plt.show()

plt.figure(figsize=(16, 4))
sns.countplot(data['Collision Type'])
plt.title('Distribusi Jenis Tabrakan')
plt.xlabel('Jumlah Kecelakaan')
plt.ylabel('Jenis Tabrakan')
plt.show()

plt.figure(figsize=(14, 14))

value_counts = data['Primary Factor'].value_counts().head(10)
value_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)

plt.title('Distribusi Faktor Utama Kecelakaan (Top 10)')
plt.ylabel('')

plt.show()

plt.figure(figsize=(14, 14))

value_counts = data['Reported_Location'].value_counts().head(10)
value_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)

plt.title('Distribusi Lokasi Pelaporan Kecelakaan (Top 10)')
plt.ylabel('')

plt.show()

"""## 5. Data Preparation

### 5.1 Menghapus duplikasi
"""

data.drop_duplicates(inplace=True)

"""### 5.2 Mengisi nilai missing value"""

column = ['Weekend?', 'Hour', 'Collision Type', 'Primary Factor', 'Reported_Location', 'Latitude', 'Longitude']

for nan in column:
    median = data[nan].mode()[0]
    data[nan].fillna(median, inplace=True)

data.isnull().sum()

"""### 5.3 Melakukan Subset Data, Encoding dan Scaling"""

data_subset = data[['Hour', 'Collision Type', 'Injury Type', 'Primary Factor']]
data_subset = data_subset.sample(frac=0.6, random_state=42)

label_encoder = LabelEncoder()
data_encoded = data_subset.apply(label_encoder.fit_transform)

scaler = StandardScaler()
data_scaled = scaler.fit_transform(data_encoded)

"""## 6. Modeling

### 6.1 Algoritma yang digunakan
"""

# Partitioning_Cluster (KMEANS Clustering)
kmeans = KMeans(n_clusters=3, n_init=10, random_state=42)
data_subset['Partitioning_Cluster'] = kmeans.fit_predict(data_scaled)

# Hierarchical Clustering (Agglomerative Clustering)
agg_cluster = AgglomerativeClustering(n_clusters=3)
data_subset['Hierarchical_Cluster'] = agg_cluster.fit_predict(data_scaled)

# Density-based Clustering (DBSCAN)
dbscan = DBSCAN(eps=0.5, min_samples=20)
data_subset['Density_Cluster'] = dbscan.fit_predict(data_scaled)

# Model-based Clustering (Gaussian Mixture Model)
gmm = GaussianMixture(n_components=3, random_state=42)
data_subset['Model_Based_Cluster'] = gmm.fit_predict(data_scaled)

"""### 6.2 Hasil modeling"""

data_subset['Partitioning_Cluster'].value_counts()

data_subset['Hierarchical_Cluster'].value_counts()

data_subset['Density_Cluster'].value_counts()

data_subset['Model_Based_Cluster'].value_counts()

"""### 6.3 Visualisasi hasil modeling"""

cluster_columns = ['Partitioning_Cluster', 'Hierarchical_Cluster', 'Density_Cluster', 'Model_Based_Cluster']

plt.figure(figsize=(15, 8))
for i, column in enumerate(cluster_columns, 1):
    plt.subplot(2, 2, i)
    sns.countplot(data=data_subset, x=column, hue=column, palette='viridis', legend=False)
    plt.title(f'{column} Clustering')

plt.tight_layout()
plt.show()

"""6.4 Metrik Evaluasi"""

# Fit and predict clusters
data_subset['Partitioning_Cluster'] = kmeans.fit_predict(data_scaled)
data_subset['Hierarchical_Cluster'] = agg_cluster.fit_predict(data_scaled)
data_subset['Density_Cluster'] = dbscan.fit_predict(data_scaled)
data_subset['Model_Based_Cluster'] = gmm.fit_predict(data_scaled)

# Calculate Silhouette Score
silhouette_scores = {
    'KMeans': silhouette_score(data_scaled, data_subset['Partitioning_Cluster']),
    'Agg_Cluster': silhouette_score(data_scaled, data_subset['Hierarchical_Cluster']),
    'DBSCAN': silhouette_score(data_scaled, data_subset['Density_Cluster']),
    'GMM': silhouette_score(data_scaled, data_subset['Model_Based_Cluster'])
}

# Calculate Calinski-Harabasz Index
calinski_harabasz_scores = {
    'KMeans': calinski_harabasz_score(data_scaled, data_subset['Partitioning_Cluster']),
    'Agg_Cluster': calinski_harabasz_score(data_scaled, data_subset['Hierarchical_Cluster']),
    'DBSCAN': calinski_harabasz_score(data_scaled, data_subset['Density_Cluster']),
    'GMM': calinski_harabasz_score(data_scaled, data_subset['Model_Based_Cluster'])
}

# Display the results
print("Silhouette Scores:")
for algorithm, score in silhouette_scores.items():
    print(f"{algorithm}: {score:.4f}")

print("\nCalinski-Harabasz Scores:")
for algorithm, score in calinski_harabasz_scores.items():
    print(f"{algorithm}: {score:.4f}")

"""## Tunning Model"""

inertia_values = []

for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, n_init=10, random_state=42)
    kmeans.fit(data_scaled)
    inertia_values.append(kmeans.inertia_)

# Plot Elbow Method
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), inertia_values, marker='o')
plt.title('Elbow Method for Optimal K')
plt.xlabel('Number of Clusters (K)')
plt.ylabel('Inertia')
plt.show()

# Partitioning_Cluster (KMEANS Clustering)
TM_kmeans = KMeans(n_clusters=4, n_init=10, random_state=42)
data_subset['TM_Partitioning_Cluster'] = TM_kmeans.fit_predict(data_scaled)

# Hierarchical Clustering (Agglomerative Clustering)
TM_agg_cluster = AgglomerativeClustering(n_clusters=4)
data_subset['TM_Hierarchical_Cluster'] = TM_agg_cluster.fit_predict(data_scaled)

# Density-based Clustering (DBSCAN)
TM_dbscan = DBSCAN(eps=0.5, min_samples=61)
data_subset['TM_Density_Cluster'] = TM_dbscan.fit_predict(data_scaled)

# Model-based Clustering (Gaussian Mixture Model)
TM_gmm = GaussianMixture(n_components=4, random_state=42)
data_subset['TM_Model_Based_Cluster'] = TM_gmm.fit_predict(data_scaled)

cluster_columns = ['TM_Partitioning_Cluster', 'TM_Hierarchical_Cluster', 'TM_Density_Cluster', 'TM_Model_Based_Cluster']

plt.figure(figsize=(15, 8))
for i, column in enumerate(cluster_columns, 1):
    plt.subplot(2, 2, i)
    sns.countplot(data=data_subset, x=column, hue=column, palette='viridis', legend=False)
    plt.title(f'{column} Clustering')

plt.tight_layout()
plt.show()

# Fit and predict clusters
data_subset['TM_Partitioning_Cluster'] = TM_kmeans.fit_predict(data_scaled)
data_subset['TM_Hierarchical_Cluster'] = TM_agg_cluster.fit_predict(data_scaled)
data_subset['TM_Density_Cluster'] = TM_dbscan.fit_predict(data_scaled)
data_subset['TM_Model_Based_Cluster'] = TM_gmm.fit_predict(data_scaled)

# Calculate Silhouette Score
TM_silhouette_scores = {
    'KMeans': silhouette_score(data_scaled, data_subset['TM_Partitioning_Cluster']),
    'Agg_Cluster': silhouette_score(data_scaled, data_subset['TM_Hierarchical_Cluster']),
    'DBSCAN': silhouette_score(data_scaled, data_subset['TM_Density_Cluster']),
    'GMM': silhouette_score(data_scaled, data_subset['TM_Model_Based_Cluster'])
}

# Calculate Calinski-Harabasz Index
TM_calinski_harabasz_scores = {
    'KMeans': calinski_harabasz_score(data_scaled, data_subset['TM_Partitioning_Cluster']),
    'Agg_Cluster': calinski_harabasz_score(data_scaled, data_subset['TM_Hierarchical_Cluster']),
    'DBSCAN': calinski_harabasz_score(data_scaled, data_subset['TM_Density_Cluster']),
    'GMM': calinski_harabasz_score(data_scaled, data_subset['TM_Model_Based_Cluster'])
}

# Display the results
print("Silhouette Scores:")
for algorithm, score in TM_silhouette_scores.items():
    print(f"{algorithm}: {score:.4f}")

print("\nCalinski-Harabasz Scores:")
for algorithm, score in TM_calinski_harabasz_scores.items():
    print(f"{algorithm}: {score:.4f}")