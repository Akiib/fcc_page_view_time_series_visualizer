import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

# Import data (Make sure to parse dates. Consider setting index column to 'date'.)
df = pd.read_csv('fcc-forum-pageviews.csv',parse_dates=True,index_col='date')

# Clean the data by filtering out days when the page views were in the top 2.5% of the dataset or bottom 2.5% of the dataset.
df = df[(df['value']>=df['value'].quantile(.025)) & (df['value']<=df['value'].quantile(.975))]


def draw_line_plot():
    # Draw line plot
    
    fig, ax = plt.subplots(figsize=(12,6))
    plt.title('Daily freeCodeCamp Forum Page Views 5/2016-12/2019')
    plt.xlabel('Date')
    plt.ylabel('Page Views')
    line = plt.plot(df,color='red')

    # Save image and return fig (don't change this part)
    fig.savefig('line_plot.png')
    return fig

def draw_bar_plot():
    # Copy and modify data for monthly bar plot
    df_bar = df.copy()
    df_bar['Years'] = df_bar.index.year
    df_bar['Months'] = df_bar.index.month_name()
    df_bar = pd.DataFrame(df_bar.groupby(['Years','Months'],sort=False)['value'].mean().round().astype(int))
    df_bar = df_bar.rename(columns={'value':'Average Page Views'})
    df_bar = df_bar.reset_index()
    missing_values = {
        "Years": [2016, 2016, 2016, 2016],
        "Months": ['January', 'February', 'March', 'April'],
        "Average Page Views": [0, 0, 0, 0]
    }
    df_bar = pd.concat([pd.DataFrame(missing_values), df_bar])
  
    # Draw bar plot
    fig, ax = plt.subplots()
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    bar_plot = sns.barplot(data=df_bar, x="Years", y="Average Page Views", hue="Months", palette="tab10")
    bar_plot.set_xticklabels(bar_plot.get_xticklabels(), rotation=90, horizontalalignment='center')
    plt.legend()

    # Save image and return fig (don't change this part)
    fig.savefig('bar_plot.png')
    return fig
  

def draw_box_plot():
    # Prepare data for box plots (this part is done!)
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box['year'] = [d.year for d in df_box.date]
    df_box['month'] = [d.strftime('%b') for d in df_box.date]

    # Draw box plots (using Seaborn)

    fig, [ax1,ax2] = plt.subplots(nrows=1,ncols=2)
    
    ax1 = plt.subplot(1,2,1)
    sns.boxplot(data= df_box, x='year',y='value',ax=ax1)
    ax1.set_title('Year-wise Box Plot (Trend)')
    ax1.set_xlabel("Year")
    ax1.set_ylabel('Page Views')
    
    
    ax2= plt.subplot(1,2,2)
    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    sns.boxplot(data= df_box, x='month',y='value',ax=ax2, order=month_order)
    ax2.set_title('Month-wise Box Plot (Seasonality)')
    ax2.set_xlabel("Month")
    ax2.set_ylabel('Page Views')



    # Save image and return fig (don't change this part)
    fig.savefig('box_plot.png')
    return fig
