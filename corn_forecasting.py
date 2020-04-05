# %% Import packages
import pandas as pd

# %% Read WASDE forecasts
wasde = pd.read_csv('./Data/WASDE/WASDE.csv', parse_dates=['Date'])
wasde = wasde.drop('Unnamed: 5', 1)
wasde['year'] = pd.DatetimeIndex(wasde['Date']).year
wasde['month'] = pd.DatetimeIndex(wasde['Date']).month
wasde['day'] = pd.DatetimeIndex(wasde['Date']).day
wasde.head(10)

# %% Read and prepare Avhrr ndvi data
avhrr = pd.read_csv('./Data/AvhrrNdvi.csv')
avhrr = avhrr.drop('.geo', 1)
avhrr = avhrr.dropna()
avhrr['system:time_start'] = avhrr['system:time_start'].multiply(1/1000)
avhrr['date'] = pd.to_datetime(avhrr['system:time_start'], unit='s')
avhrr['year'] = pd.DatetimeIndex(avhrr['date']).year
avhrr['month'] = pd.DatetimeIndex(avhrr['date']).month
avhrr['day'] = pd.DatetimeIndex(avhrr['date']).day
avhrr['GEOID'] = avhrr['GEOID'].astype(str)
avhrr.head(10)

# %% Read and prepare Modis ndvi data
modis = pd.read_csv('./Data/ModisNdvi.csv')
modis = modis.drop('.geo', 1)
modis = modis.dropna()
modis['NDVI'] = modis['NDVI'].multiply(1/10000)
modis['system:time_start'] = modis['system:time_start'].multiply(1/1000)
modis['date'] = pd.to_datetime(modis['system:time_start'], unit='s')
modis['year'] = pd.DatetimeIndex(modis['date']).year
modis['month'] = pd.DatetimeIndex(modis['date']).month
modis['day'] = pd.DatetimeIndex(modis['date']).day
modis['GEOID'] = modis['GEOID'].astype(str)
modis.head()

# %% Read and prepare the weather data (PRISM)
prism = pd.read_csv('./Data/PrismCornProducers.csv')
prism = prism.drop('.geo', 1)
prism.head(10)
# %%
corn = pd.read_csv('./Data/CornProduction.csv')
corn = corn.dropna()
corn['CountyANSI'] = corn['CountyANSI'].astype(int)
corn['StateANSI'] = corn['StateANSI'].astype(str)
corn['CountyANSI'] = corn['CountyANSI'].astype(str)
corn['CountyANSI'] = corn['CountyANSI'].apply(lambda x: x.zfill(3))
corn['GEOID'] = corn['StateANSI'] + corn['CountyANSI']
corn.head(10)
# %% Select the Aug forecast & data for it 
forecast_month = 8
mask_wasde = (wasde['month'] == forecast_month)
mask_avhrr = (avhrr['month'] <= forecast_month)
mask_modis = (modis['month'] <= forecast_month)
wasde_selection = wasde.loc[mask_wasde]
avhrr_selection = avhrr.loc[mask_avhrr]
modis_selection = modis.loc[mask_modis]
# %% Select a random county
avhrr_county = (avhrr_selection['GEOID'] == '17109')
modis_county = (modis_selection['GEOID'] == '17109')
county_avhrr = avhrr_selection[avhrr_county]
county_modis = modis_selection[modis_county]
county_modis.head(10)


# %%
