import pandas as pd
import matplotlib.pyplot as plt
import Seth.Util as ut
import matplotlib as mpl
import matplotlib.ticker as mtick

data = pd.read_csv('Dataset_Versions/Original Dataset.csv')
data['prices.range'] = data['prices.amountMax'] - data['prices.amountMin']


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


brandPrices = noNulls.groupby('brand')[['prices.amountMin', 'prices.amountMax', 'prices.range']].mean().sort_values(by='prices.amountMax')
priceRange = ['prices.amountMin', 'prices.amountMax']
ut.plotDF(brandPrices[priceRange].iloc[0:20,]
          , {'kind': 'barh', 'stacked':False},
          {
              'ylabel': 'Brand',
              'xlabel': 'Average Price',
              'title': 'Brands with Highest Prices',
              'savefig': barDir + 'Brand Prices by Max Price.png'},
          removeOutliersBeforePlotting=False)

brandPrices.sort_values(by='prices.range', inplace=True, ascending=True)
ut.plotDF(brandPrices[priceRange].iloc[-20:,]
          , {'kind': 'barh', 'stacked':False},
          {
              'ylabel': 'Brand',
              'xlabel': 'Average Price',
              'title': 'Brands with Highest Price Variation',
              'savefig': barDir + 'Brand Prices by Variation.png'},
          removeOutliersBeforePlotting=False)


merchantPrices = data.groupby('prices.merchant')[['prices.amountMin', 'prices.amountMax', 'prices.range']].mean()
merchantPrices.sort_values(by='prices.amountMax', inplace=True, ascending=True)

ut.plotDF(merchantPrices[priceRange].iloc[-20:,]
          , {'kind': 'barh', 'stacked':False},
          {
              'ylabel': 'Store',
              'xlabel': 'Average Price',
              'title': 'Stores with Highest Prices',
              'savefig': barDir + 'Store Prices by Max Price.png'},
          removeOutliersBeforePlotting=False)

merchantPrices.sort_values(by='prices.range', inplace=True, ascending=True)

ut.plotDF(merchantPrices[priceRange].iloc[-20:,]
          , {'kind': 'barh', 'stacked':False},
          {
              'ylabel': 'Store',
              'xlabel': 'Average Price',
              'title': 'Stores with highest Price Variation',
              'savefig': barDir + 'Store Prices by Variation.png'},
          removeOutliersBeforePlotting=False)


print('finished')