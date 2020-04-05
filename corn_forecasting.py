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
prism['system:time_start'] = prism['system:time_start'].multiply(1/1000)
prism['date'] = pd.to_datetime(prism['system:time_start'], unit='s')
prism['year'] = pd.DatetimeIndex(prism['date']).year
prism['month'] = pd.DatetimeIndex(prism['date']).month
prism['day'] = pd.DatetimeIndex(prism['date']).day
prism['GEOID'] = prism['GEOID'].astype(str)
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
mask_avhrr = (avhrr['month'] <= forecast_month) & (avhrr['year'] < 2000) & (avhrr['year'] > 1981)
mask_modis = (modis['month'] <= forecast_month)
mask_prism = (prism['month'] <= forecast_month)
wasde_selection = wasde.loc[mask_wasde]
avhrr_selection = avhrr.loc[mask_avhrr]
modis_selection = modis.loc[mask_modis]
prism_selection = prism.loc[mask_prism]
prism_selection.head(10)
# %% Select a random county
corn_county = (corn['GEOID'] == '17109')
avhrr_county = (avhrr_selection['GEOID'] == '17109')
modis_county = (modis_selection['GEOID'] == '17109')
prism_county = (prism_selection['GEOID'] == '17109')
county_corn = corn[corn_county]
county_avhrr = avhrr_selection[avhrr_county]
county_modis = modis_selection[modis_county]
county_prism = prism_selection[prism_county]
county_prism.head(10)
# %%
y = county_corn[['year','Value']]
def determinePeriod(x, type):
    if x <= 15: 
        return 'a' + '_' + type
    if x > 15: 
        return 'b' + '_' + type
# Avhrr        
county_avhrr['position'] = county_avhrr['day'].apply(determinePeriod, type='ndvi')
county_avhrr['period'] = county_avhrr['month'].astype(str) + county_avhrr['position']
x_avhrr = county_avhrr[['ndvi', 'year', 'period']]
x_avhrr = x_avhrr.pivot(index='year', columns='period', values='ndvi')
# Modis
county_modis['position'] = county_modis['day'].apply(determinePeriod, type='ndvi')
county_modis['period'] = county_modis['month'].astype(str) + county_modis['position']
x_modis = county_modis[['NDVI', 'year', 'period']]
x_modis = x_modis.pivot(index='year', columns='period', values='NDVI')
# Prism
county_prism['position'] = county_prism['day'].apply(determinePeriod, type='')
county_prism['period'] = county_prism['month'].astype(str) + county_prism['position']
x_tmean = county_prism[['tmean', 'year', 'period']]
x_tmean['period'] = x_tmean['period'].apply(lambda x: x + 'tmean')
x_tmean = x_tmean.pivot(index='year', columns='period', values='tmean')

x_tmean = county_prism[['tmean', 'year', 'period']]
x_tmean['period'] = x_tmean['period'].apply(lambda x: x + 'tmean')
x_tmean = x_tmean.pivot(index='year', columns='period', values='tmean')

x_ppt = county_prism[['ppt', 'year', 'period']]
x_ppt['period'] = x_ppt['period'].apply(lambda x: x + 'ppt')
x_ppt = x_ppt.pivot(index='year', columns='period', values='ppt')

x_vpdmax = county_prism[['vpdmax', 'year', 'period']]
x_vpdmax['period'] = x_vpdmax['period'].apply(lambda x: x + 'vpdmax')
x_vpdmax = x_vpdmax.pivot(index='year', columns='period', values='vpdmax')

# %% Combine the x variables on year
x_sat = x_modis.append(x_avhrr)
x_combined = pd.concat([x_sat, x_tmean, x_ppt, x_vpdmax], axis=1, sort=True)
full_combined = pd.merge(x_combined, y, how='left', on=['year'])
full_combined.head(10)

# %%


# %%
