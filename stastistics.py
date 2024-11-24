
import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols

#Träningsdata
dates = ["2024-11-01", "2024-11-02", "2024-11-03", "2024-11-04", "2024-11-05"]
sleep_hours = [9, 10, 8, 8, 8]  #Sömn(timmar)
calories = [2000, 2500, 2200, 1800, 2000]  #Kaloriintag (kcal)
emotional_state = [5, 10, 7, 4, 5]  #Emotionellt mående (skala 1–10)
gym_performance_scale = [9, 10, 9, 6, 7]  #Användarens performance rating (dependent variable)

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


#Skapa dictionary för factors och coefficients
factor_names = ["Sömn", "Kalorier", "Emotionellt mående"]

impact = {}
for factor, coeff in zip(factor_names, coefficients):
    impact[factor] = coeff

print("Regressionsmodellen")
print(f"Koefficienter: {impact}")
print(f"Intercept: {intercept}")
print(f"R^2 värde: {r2:.2f}")


#Sortera dict efter absolutvärdet av koefficienterna (störst påverkan först)
sorted_impact = sorted(impact.items(), key=lambda item: abs(item[1]), reverse=True)

print("\nDe här faktorerna påverkar sannolikt din träning:")

#Gå igenom varje faktor och dess koefficient i den sorterade ordboken
for factor, coeff in sorted_impact:
    #Avgör om påverkan är positiv eller negativ
    if coeff > 0:
        influence = "positivt"
    else:
        influence = "negativt"
    
    #Skriv ut faktorn och dess påverkan
    print(f"- {factor}: {influence} påverkan (koefficient = {coeff:.2f})")


#ANOVA - för att utvärdera om påverkan är signifikant
data = pd.DataFrame({
    "Sömn": sleep_hours,
    "Kalorier": calories,
    "Emotionellt_mående": emotional_state,
    "Träningsranking": gym_performance_scale
})

#utför ANOVA
anova_model = ols("Träningsranking ~ Sömn + Kalorier + Emotionellt_mående", data=data).fit()
anova_table = sm.stats.anova_lm(anova_model, typ=2)


print("\nStatsmodels ANOVA-tabell")
print(anova_table)


factor_pvalues = anova_table["PR(>F)"]  #Hämta p-värden från ANOVA-tabellen
factor_significance = factor_pvalues < 0.05  #Bool: Är p-värdet signifikant?

#Kombinera koefficienter och p-värden för rapportering
print("\nFaktorer och Signifikans")
for factor, coeff, pval, sig in zip(factor_names, coefficients, factor_pvalues, factor_significance):
    significance = "Signifikant" if sig else "Inte signifikant"
    print(f"{factor}: Koefficient = {coeff:.2f}, p-värde = {pval:.3f} ({significance})")





#Plotting
#Första versionen, detta kommer ändras


independent_variables = [sleep_hours, calories, emotional_state]
variable_names = ["Sömn (timmar)", "Kalorier", "Emotionellt mående"]

#Skapa subplots för varje oberoende variabel
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=True)

for i, (x_var, var_name) in enumerate(zip(independent_variables, variable_names)):
    x_var_reshaped = np.array(x_var).reshape(-1, 1)
    single_var_model = LinearRegression()
    single_var_model.fit(x_var_reshaped, y)


    x_line = np.linspace(min(x_var), max(x_var), 100).reshape(-1, 1)
    y_line = single_var_model.predict(x_line)

    axes[i].scatter(x_var, y, edgecolor="black", color="none", label="Datapunkter")
    axes[i].plot(x_line, y_line, color="red", label="Regressionslinje")
    axes[i].set_title(f"{var_name} vs Träningsranking")
    axes[i].set_xlabel(var_name)
    if i == 0:
        axes[i].set_ylabel("Träningsranking")
    axes[i].legend()
    
    

plt.tight_layout()
plt.show()



