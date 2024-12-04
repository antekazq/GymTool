
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

import sys
import json




#JSON data från Node.js
input_data = json.loads(sys.argv[1])
sleep_hours = input_data["sleep_hours"]
calories = input_data["calories"]
emotional_state = input_data["emotional_state"]
gym_performance_scale = input_data["gym_performance_scale"]
dates = input_data["dates"]



#Konvertera inputs till numpy array (2D)
x = np.array([sleep_hours, calories, emotional_state]).T  #Independent variables
y = np.array(gym_performance_scale)  #Dependent variable

#Skapa linjär regressionslinje
reg = LinearRegression()
reg.fit(x, y) #Modellen ser ut så här: y = b0 + B1 * x1 + B2 * x2 + B3 * x3

#Modellens resultat
coefficients = reg.coef_ #B1, B2, B3 (m-värden)
intercept = reg.intercept_ #B0 (C-värde)
predictions = reg.predict(x)  #y predictions när vi går igenom alla x värden

#Utvärdera modellen
r2 = r2_score(y, predictions)  #Räknar ut hur stor skillnad det är mellan y-predictions och de faktiska y-värdena

#ANOVA
#För att utvärdera om påverkan är signifikant
data = pd.DataFrame({
    "Sleep": sleep_hours,
    "Kcal": calories,
    "Emotionalstate": emotional_state,
    "Gymperformance": gym_performance_scale
})

anova_model = ols("Gymperformance ~ Sleep + Kcal + Emotionalstate", data=data).fit()
anova_table = sm.stats.anova_lm(anova_model, typ=2)

anova_table = anova_table.replace([np.nan, np.inf, -np.inf], 0)

#Plotting
independent_variables = [sleep_hours, calories, emotional_state]
variable_names = ["Sleep (hours)", "Kcal", "Emotionalstate"]


#Skapa subplots för varje oberoende variabel
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, (x_var, var_name) in enumerate(zip(independent_variables, variable_names)):
    axes[i].scatter(dates, x_var, edgecolor="black", color="none", label="Datapunkter")
    axes[i].set_title(f"{var_name} vs Date")
    axes[i].set_xlabel("Date")
    if i == 0:
        axes[i].set_ylabel("Value")
    axes[i].legend()

plt.tight_layout()
plt.show(block=False)  # Non-blocking
plt.pause(5)  # Keep the plot open for 5 seconds
plt.close()  # Close the plot automatically






#Returnera resultaten som JSON
results = {
    "coefficients": {name: float(coef) for name, coef in zip(variable_names, coefficients)},
    "r2": float(r2),
    "anova": anova_table.astype(float).to_dict()  #Säkerställ att all data i ANOVA-tabellen är flyttal
}

print(json.dumps(results, ensure_ascii=False))


