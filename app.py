import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Erstelle ein Dictionary mit den Daten
data = {
    'life_expectancy_men':              [75] * 5 + [76] * 5 + [77] * 5 + [78] * 5 + [79] * 10 + [80] * 10 + [81] * 15 + [82] * 20 + [83] * 15 + [84] * 10 + [85] * 10 + [86] * 5 + [87] * 5 + [88] * 5 + [89] * 5,
    'life_expectancy_women':            [79] * 5 + [80] * 5 + [81] * 5 + [82] * 5 + [83] * 10 + [84] * 10 + [85] * 15 + [86] * 20 + [86] * 15 + [87] * 10 + [88] * 10 + [89] * 5 + [90] * 5 + [91] * 5 + [92] * 5,
    'Ernährung_men':                    [5, 5, 2, 3, 4, 5, 3, 1, 5, 5, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 4, 5, 5, 3, 4, 5, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 3, 2, 4, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 3, 4, 4, 3, 4, 5, 3, 4, 5, 4, 2, 5, 3, 4, 5, 3, 4, 5, 4, 1, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 1, 4, 5, 4, 2, 5, 4, 5, 3, 4, 1, 3, 2, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2],
    'Ernährung_women':                  [5, 4, 3, 4, 4, 5, 2, 4, 4, 3, 5, 5, 3, 2, 1, 4, 2, 4, 5, 3, 4, 5, 4, 2, 5, 3, 4, 5, 4, 3, 4, 4, 3, 2, 3, 4, 3, 3, 4, 3, 2, 3, 1, 5, 3, 4, 3, 2, 5, 4, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 4, 5, 4, 2, 5, 4, 5, 3, 4, 5, 4, 1, 4, 1, 2, 5, 4, 1, 3, 4, 2, 4, 2, 2, 3, 1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1],
    'Bewegung_men':                     [1,1,2,3,2,1,2,1,2,3,2,1,2,2,1,2,3,4,3,4,3,2,3,2,5,2,3,4,2,3,5,3,4,3,1,1,1,4,3,2,4,2,3,5,2,3,2,5,4,3,4,5,4,2,3,1,4,1,4,2,3,2,4,3,5,2,4,3,2,3,4,3,2,4,4,4,3,2,3,4,1,4,3,4,3,4,5,2,3,4,3,4,5,4,5,4,5,4,4,4,3,4,5,4,5,4,5,3,2,3,4,3,2,3,4,5,5,4,5,5,4,5,4,3,4,2,4,5,2,5],
    'Bewegung_women':                   [2,1,3,2,2,2,3,3,2,1,2,1,2,1,3,1,4,2,1,2,3,4,3,2,4,1,2,1,2,3,2,3,2,2,2,2,2,4,3,1,5,2,5,3,2,3,2,3,4,3,4,3,2,3,3,3,2,3,2,1,2,3,1,3,3,3,3,3,4,5,2,5,2,5,2,3,2,3,2,4,3,4,4,4,3,4,3,2,3,3,2,3,5,3,2,2,3,3,2,1,4,1,3,2,3,4,3,4,4,5,4,5,3,5,4,5,3,4,3,3,2,3,2,5,5,5,2,5,5,5],
    'Rauchen_men':                      [5,5,5,5,5,3,4,3,5,4,4,4,5,4,3,4,5,5,3,5,3,5,4,5,5,3,5,1,5,1,5,5,4,5,4,4,3,2,2,2,2,2,4,3,1,5,2,5,3,2,3,2,3,4,3,4,3,2,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,2,3,3,4,3,1,4,2,2,1,2,2,1,1,1,2,2,3,2,3,1,3,1,5,1,1,2,2,3,2,1,3,1,3,1,1,2,2,1,1,2,1,2,2,2,1,1,1,2,1,1,1,2,1,1,1,1],
    'Rauchen_women':                    [5,5,5,5,5,4,5,3,5,5,4,4,5,4,3,5,5,5,3,5,4,5,4,5,5,3,5,4,5,5,5,5,4,5,4,4,3,2,2,2,2,2,4,3,1,5,2,5,3,2,3,2,3,4,3,4,3,2,3,3,3,2,3,3,3,3,3,3,3,3,3,3,3,2,3,3,4,3,1,4,2,2,1,2,2,1,1,1,2,2,3,2,3,1,3,1,2,1,1,2,2,1,2,1,3,1,2,1,1,1,1,1,1,2,1,2,2,2,1,1,1,2,1,1,1,2,1,1,1,1],
    #'Alkoholkonsum_men':                [5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #'Alkoholkonsum_women':              [5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #'Stress_men':                       [5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #'Stress_women':                     [5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #'Schlafqualität_men':               [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5],
    #'Schlafqualität_women':             [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5],
    #'Bildungsniveau_men':               [5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #'Bildungsniveau_women':             [5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    #'Zugang_Gesundheitsvers._men':      [5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #'Zugang_Gesundheitsvers._women':    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,3,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5,5]

}

#     'Ernährung':                        [3, 4, 2, 5, 3, 4, 3, 2, 4, 5, 3, 3, 4, 2, 4, 5, 3, 3, 2, 4, 3, 4, 2, 5, 3, 4, 3, 2, 4, 5, 3, 3, 4, 2, 4, 5, 3, 3, 2, 4, 3, 4, 2, 5, 3, 4, 3, 2, 4],
#    'Bewegung':                         [4, 5, 3, 4, 2, 5, 3, 2, 4, 5, 3, 4, 5, 3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5],
#    'Rauchen':                          [2, 1, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 1],
#    'Alkoholkonsum':                    [3, 2, 4, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 1, 5],
#    'Stress':                           [4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 4, 3, 5, 2, 3],
#    'Schlafqualität':                   [3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 2, 3, 4, 5, 3, 2],
#   'Soziales Umfeld':                  [4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 3, 4, 5, 1, 2],
#    'Bildungsniveau':                   [3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3],
#    'Zugang zur Gesundheitsversorgung': [5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 3, 4, 2, 5, 4, 2, 2, 3],





# Berechnung der Korrelation
corr_men = np.corrcoef(data['life_expectancy_men'], data['Ernährung_men'])[0, 1]
corr_women = np.corrcoef(data['life_expectancy_women'], data['Ernährung_women'])[0, 1]
corr_movement_men = np.corrcoef(data['life_expectancy_men'], data['Bewegung_men'])[0, 1]
corr_movement_women = np.corrcoef(data['life_expectancy_women'], data['Bewegung_women'])[0, 1]
corr_smoking_men = np.corrcoef(data['life_expectancy_men'], data['Rauchen_men'])[0, 1]
corr_smoking_women = np.corrcoef(data['life_expectancy_women'], data['Rauchen_women'])[0, 1]

# Korrelationsgraph für Männer (Ernährung)
fig, ax = plt.subplots()
sns.regplot(x=data['Ernährung_men'], y=data['life_expectancy_men'], fit_reg=False, ax=ax)
plt.title('Korrelation zwischen Lebenserwartung von Männern und Ernährung (Korrelation: {:.2f})'.format(corr_men))
plt.xlabel('Ernährung (Männer)')
plt.ylabel('Lebenserwartung (Männer)')
st.pyplot(fig)

# Korrelationsgraph für Frauen (Ernährung)
fig, ax = plt.subplots()
sns.regplot(x=data['Ernährung_women'], y=data['life_expectancy_women'], fit_reg=False, ax=ax)
plt.title('Korrelation zwischen Lebenserwartung von Frauen und Ernährung (Korrelation: {:.2f})'.format(corr_women))
plt.xlabel('Ernährung (Frauen)')
plt.ylabel('Lebenserwartung (Frauen)')
st.pyplot(fig)

# Korrelationsgraph für Männer (Bewegung)
fig, ax = plt.subplots()
sns.regplot(x=data['Bewegung_men'], y=data['life_expectancy_men'], fit_reg=False, ax=ax)
plt.title('Korrelation zwischen Lebenserwartung von Männern und Bewegung (Korrelation: {:.2f})'.format(corr_movement_men))
plt.xlabel('Bewegung (Männer)')
plt.ylabel('Lebenserwartung (Männer)')
st.pyplot(fig)

# Korrelationsgraph für Frauen (Bewegung)
fig, ax = plt.subplots()
sns.regplot(x=data['Bewegung_women'], y=data['life_expectancy_women'], fit_reg=False, ax=ax)
plt.title('Korrelation zwischen Lebenserwartung von Frauen und Bewegung (Korrelation: {:.2f})'.format(corr_movement_women))
plt.xlabel('Bewegung (Frauen)')
plt.ylabel('Lebenserwartung (Frauen)')
st.pyplot(fig)

# Korrelationsgraph für Männer (Rauchen)
fig, ax = plt.subplots()
sns.regplot(x=data['Rauchen_men'], y=data['life_expectancy_men'], fit_reg=False, ax=ax)
plt.title('Korrelation zwischen Lebenserwartung von Männern und Rauchen (Korrelation: {:.2f})'.format(corr_smoking_men))
plt.xlabel('Rauchen (Männer)')
plt.ylabel('Lebenserwartung (Männer)')
st.pyplot(fig)

# Korrelationsgraph für Frauen (Rauchen)
fig, ax = plt.subplots()
sns.regplot(x=data['Rauchen_women'], y=data['life_expectancy_women'], fit_reg=False, ax=ax)
plt.title('Korrelation zwischen Lebenserwartung von Frauen und Rauchen (Korrelation: {:.2f})'.format(corr_smoking_women))
plt.xlabel('Rauchen (Frauen)')
plt.ylabel('Lebenserwartung (Frauen)')
st.pyplot(fig)









# Erstelle ein DataFrame aus dem Dictionary
#df = pd.DataFrame(data)

# Zeige den DataFrame in Streamlit an
#st.write(df)

# Überprüfe die Länge der Liste
# länge = len(data['Bewegung_men'])

# Zeige die Länge in Streamlit an
# st.write("Die Länge der Liste 'ernährung' beträgt:", länge)
