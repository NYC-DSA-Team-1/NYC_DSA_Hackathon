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

data = ut.removeNullColumns(data, 95)
data.to_csv('Dataset_Versions/' + 'Removed Nulls.csv')
ut.plotDF(ut.getNullPercents(data), {'kind': 'barh', 'x': 'Column', 'y': 'Null Percent', 'legend': False},
          {
              'grid': None,
              xTickFormatPercent: '',
              'xlabel': '# of Null Values',
              'title': 'Null Columns ',
              'savefig': barDir + 'Null Percents.png'},
          removeOutliersBeforePlotting=False)


