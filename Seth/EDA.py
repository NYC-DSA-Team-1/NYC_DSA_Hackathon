import pandas as pd
import matplotlib.pyplot as plt
import Seth.Util as ut
import matplotlib as mpl
import matplotlib.ticker as mtick
import numpy as np

data = pd.read_csv('Dataset_Versions/Original Dataset.csv')
data.rename(columns={'prices.amountMax': 'maxPrice', 'prices.amountMin': 'minPrice'}, inplace=True)

data['priceRange'] = data['maxPrice'] - data['minPrice']
data['priceRangePercent'] = data['minPrice'] / data['maxPrice']
data['meanPrice'] = (data['maxPrice'] + data['minPrice'])/2


histDir = 'Seth/Plots/'
scatterDir = 'Seth/Plots/'
barDir = 'Seth/Plots/'

histParams = {'kind': 'hist', 'legend': False, 'bins': 50}
barParams = {'kind': 'bar', 'legend': False}
figParams= {'x': 2, 'y': 1}



plt.rc('font', size=40)
plt.rc('axes', labelsize=60)
plt.rc('axes', titlesize=60)

xTickMult = lambda: ut.multiplyRange(plt.xticks()[0], 0.5)
xTickMultLS = lambda: ut.multiplyLinSpace(plt.xticks()[0], 2)
yTickFormat = lambda : plt.gca().yaxis.set_major_formatter(plt.FormatStrFormatter('%.0f'))
xTickFormatPercent = lambda: plt.gca().xaxis.set_major_formatter(mtick.PercentFormatter(decimals=0))
xTickFormatCommas = lambda: plt.gca().xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('{x:,.0f}'))
xTickFormatDollars = lambda x=0:  plt.gca().xaxis.set_major_formatter(mpl.ticker.StrMethodFormatter('${x:,.'+str(x)+'f}'))
#setTickIn = lambda: plt.gca().tick_params(axis='x', direction='in')
trimTicks = lambda: plt.xticks()[0:-1]
nullsDir = 'Visualizations/Nulls/'
histParams = {'kind': 'hist', 'legend': False, 'bins': 100}

#     ut.plotDF(train[['SalePrice']], histParams,
#            {xTickFormatDollars: '',
#             yTickFormat: '',
#             'grid': None,
#             'xlabel': 'Sale Price',
#             'title': 'Sale Price of Houses in Ames, Iowa',
#             'savefig': histDir + 'SalePrice.png'})
# ut.printNulls(data)

noNulls = ut.removeNullColumns(data, 95)
noNulls.to_csv('Dataset_Versions/' + 'Removed Nulls.csv')

ut.plotDF(ut.getNullPercents(noNulls), {'kind': 'barh', 'x': 'Column', 'y': 'Null Percent', 'legend': False},
          {
              'grid': None,
              xTickFormatPercent: '',
              'xlabel': '# of Null Values',
              'title': 'Null Columns ',
              'savefig': barDir + 'Null Percents.png'},
          removeOutliersBeforePlotting=False)

cols = noNulls.columns

#plot price range by brand
data = noNulls

brandPrices = data.groupby('brand')[['minPrice', 'maxPrice', 'priceRange', 'priceRangePercent']].mean().sort_values(by='maxPrice')
priceRange = ['minPrice', 'maxPrice']
ut.plotDF(brandPrices[priceRange].iloc[0:20,]
          , {'kind': 'barh', 'stacked':False},
          {
              'ylabel': 'Brand',
              'xlabel': 'Average Price',
              'title': 'Brands with Highest Prices',
              'savefig': barDir + 'Brand Prices by Max Price.png'},
          removeOutliersBeforePlotting=False)

brandPrices.sort_values(by='priceRangePercent', inplace=True, ascending=False)
#ut.print_full(brandPrices.iloc[-20:,])
ut.plotDF(pd.DataFrame(brandPrices['priceRangePercent']).iloc[-20:,]
          , {'kind': 'barh', 'legend': None},
          {
              'ylabel': 'Brand',
              'xlabel': 'Ratio between minPrice and maxPrice',
              'title': 'Brands with Highest Price Variation',
              'savefig': barDir + 'Brand Prices by Variation.png'},
          removeOutliersBeforePlotting=False)


merchantPrices = data.groupby('prices.merchant')[['minPrice', 'maxPrice', 'priceRange', 'priceRangePercent']].mean()
merchantPrices.sort_values(by='maxPrice', inplace=True, ascending=True)

ut.plotDF(merchantPrices[priceRange].iloc[-20:,]
          , {'kind': 'barh', 'stacked':False},
          {
              'ylabel': 'Merchant',
              'xlabel': 'Average Price',
              'title': 'Merchants with Highest Prices',
              'savefig': barDir + 'Store Prices by Max Price.png'},
          removeOutliersBeforePlotting=False)

merchantPrices.sort_values(by='priceRangePercent', inplace=True, ascending=False)

ut.plotDF(pd.DataFrame(merchantPrices['priceRangePercent']).iloc[-20:,]
          , {'kind': 'barh', 'legend': None},
          {
              'ylabel': 'Merchant',
              'xlabel': 'Ratio between minPrice and maxPrice',
              'title': 'Merchant with highest Price Variation',
              'savefig': barDir + 'Merchant Prices by Variation.png'},
          removeOutliersBeforePlotting=False)

data['prices.merchant'].replace({'Best Buy': 'Bestbuy.com'}, inplace=True)
minPrices = data.groupby('id')[['meanPrice', 'prices.merchant']].min()
maxPrices = data.groupby('id')[['meanPrice', 'prices.merchant']].max()

priceVariations = pd.DataFrame()
priceVariations['minPrice'] = minPrices['meanPrice']
priceVariations['maxPrice'] = maxPrices['meanPrice']
priceVariations['minMerchant'] = minPrices['prices.merchant']
priceVariations['maxMerchant'] = maxPrices['prices.merchant']

bestMerchants = priceVariations.groupby('minMerchant')['minPrice'].count().sort_values(ascending=True)
bestMerchantsTotal = bestMerchants.sum()
bestMerchantsPercent = bestMerchants / bestMerchantsTotal

bestMerchants = pd.DataFrame(bestMerchants)
bestMerchantsPercent = pd.DataFrame(bestMerchantsPercent)

ut.plotDF(bestMerchants.iloc[-20:,]
          , {'kind': 'barh', 'stacked':False, 'legend': None},
          {
              'ylabel': 'Merchant',
              'xlabel': '# of Products with Lowest Price',
              'title': 'Merchants with Lowest Prices',
              'savefig': barDir + 'Best Merchant Prices.png'},
          removeOutliersBeforePlotting=False)

ut.plotDF(bestMerchantsPercent.iloc[-20:,]
          , {'kind': 'barh', 'stacked':False, 'legend': None},
          {
              'ylabel': 'Merchant',
              'xlabel': '% of Products with Lowest Price',
              'title': 'Merchants with Lowest Prices',
              'savefig': barDir + 'Best Merchant Prices By Percent.png'},
          removeOutliersBeforePlotting=False)
merchantCounts = pd.DataFrame(data['prices.merchant'].value_counts()).sort_values(by = 'prices.merchant',ascending=True)

ut.print_full(merchantCounts)
ut.plotDF(merchantCounts[-20:]
          , {'kind': 'barh', 'legend': None},
          {
              'ylabel': 'Merchant',
              'xlabel': '# of Products Merchant Sells',
              'title': 'Merchant Counts',
              'savefig': barDir + 'Merchant Product Counts.png'},
          removeOutliersBeforePlotting=False)

merchantCounts['prices.merchant'] = merchantCounts['prices.merchant'] / merchantCounts['prices.merchant'].sum()
ut.plotDF(merchantCounts[-20:]
          , {'kind': 'barh', 'legend': None},
          {
              'ylabel': 'Merchant',
              'xlabel': '% of Products Merchant Sells',
              'title': 'Merchant Counts',
              'savefig': barDir + 'Merchant Product Count Ratios .png'},
          removeOutliersBeforePlotting=False)

print('finished')