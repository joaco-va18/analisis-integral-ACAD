import statsmodels.api as sm
from datos import model_data
from datos import rf_d
y = model_data["ACAD_exc"]
X = sm.add_constant(model_data[["Rm"]])
capm = sm.OLS(y, X).fit()
print(capm.summary())
print("Alpha | Beta:", capm.params)
X_ff3 = sm.add_constant(model_data[["Rm", "SMB", "HML"]])
ff3 = sm.OLS(y, X_ff3).fit()
print(ff3.summary())
print("Alpha | Beta:", ff3.params)
aux_smb = sm.OLS(model_data["SMB"], X).fit()
aux_hml = sm.OLS(model_data["HML"], X).fit()
print(ff3.params["Rm"] + ff3.params["SMB"] * aux_smb.params["Rm"]
      + ff3.params["HML"] * aux_hml.params["Rm"])
print("delta SMB:", aux_smb.params["Rm"])
print("delta HML:", aux_hml.params["Rm"])
ff3_hc3 = sm.OLS(y, X_ff3).fit(cov_type="HC3")
print(ff3_hc3.summary())
expected_return = rf_d.mean() * 252 + capm.params["Rm"] * (model_data["Rm"].mean() * 252)
print(f"Expected Return: {expected_return:.2%}")
