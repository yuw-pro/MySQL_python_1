from SQL_helper import MySQLHelper
import pandas as pd
import matplotlib.pyplot as plt 
import seaborn as sns

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class DoubanEDA:
    def __init__(self, database = "douban"):
        data_sql = MySQLHelper(database = database)
        connection = data_sql.connect()
        self.df = pd.read_sql('select * from douban_films', con=connection)
# EDA 1.概览 2.完整性 3.分布 4.关联5.异常值6.可视化
    #1.概览
    def overview(self):
        print('===数据形状===\n', self.df.shape)

        print('===数据前五行===\n', self.df.head())
        print('===数据后五行===\n', self.df.tail())

        print('===数据列名===\n', self.df.columns)
        print('===普通列表===\n', self.df.columns.tolist())

        print('===数据信息===\n') 
        self.df.info()
        print('===数据描述===\n', self.df.describe())

    #2.完整性
    def integrity(self):
        # 真缺失:None / NaN
        missing = self.df.isna().sum()
        print('===缺失值===\n', missing[missing > 0])

        # 空串:只对文本列,用 dropna 排除真缺失,避免和上面重复计数
        self.text_cols = self.df.select_dtypes(include=['object', 'string']).columns
        blank = pd.Series({
            col: self.df[col].dropna().str.strip().eq('').sum()
            for col in self.text_cols
        })
        for col in self.text_cols:
            if blank[col] > 0:
                print(f"Column '{col}' has {blank[col]} empty strings.")

        # 有缺失才往下推进
        if missing.sum() > 0 or blank.sum() > 0:
            total = missing.add(blank, fill_value=0)
            rate = (total / len(self.df) * 100).round(2)
            print('===缺失值占比===\n', rate[rate > 0])
        else:
            print('===无===')
        #填补或者

    #3.
    def distribution(self):
        #单个变量
        self.num_cols = self.df.select_dtypes(include = ['number'])
        for num_col in self.num_cols:
            #range
            print(
                f'==={num_col}范围===\n', f'==={num_col}最大值===', self.df[num_col].max(), 
                f'==={num_col}最小值===', self.df[num_col].min(), f'==={num_col}极差===', self.df[num_col].max() - self.df[num_col].min()
            ) 
            #mean
            print(
                f'==={num_col}平均值===\n', self.df[num_col].mean(),
                f'==={num_col}中位数===\n', self.df[num_col].median(),
                f'==={num_col}众数===\n', self.df[num_col].mode()
            )
            #std
            print(f'==={num_col}标准差===\n', self.df[num_col].std())
            print(f'==={num_col}IQR===\n', self.df[num_col].quantile(0.75)
                                           -self.df[num_col].quantile(0.25))
            #skew
            print(f'==={num_col}偏度===\n', self.df[num_col].skew()) 
            print(f'==={num_col}峰度===\n', self.df[num_col].kurt())
            #counts统计
            print(f'===={num_col}频数统计===', self.df[num_col].value_counts().sort_index())
            print(f'===={num_col}百分比===', self.df[num_col].value_counts(normalize=True).sort_index())
            print(f'==={num_col}不同值===', self.df[num_col].nunique())
        #类
        for text_col in self.text_cols:
            print(f'===={text_col}频数统计===', self.df[text_col].value_counts().head())
            print(f'===={text_col}百分比===', self.df[text_col].value_counts(normalize=True).sort_index())
            print(f'==={text_col}不同值===', self.df[text_col].nunique())
    #4.关联
    def correlation(self):
        self.num_cols_corr = ['rating', 'review_count', 'release_date']
        self.text_cols_corr = ['country', 'genre', 'director']
        #数值数值
        print('===相关系数===\n', self.df[self.num_cols_corr].corr())
        #数值定性
        for col in self.num_cols_corr:
            for text_col in self.text_cols_corr: 
                print(f'===={col} by {text_col}====\n',
                self.df.groupby(text_col)[col].describe())
        #strstr
        for text_col1 in self.text_cols_corr:
            for text_col2 in self.text_cols_corr:
                if text_col1 != text_col2:
                    print(f'===={text_col1} by {text_col2}====\n',  
                        pd.crosstab(self.df[text_col1],
                                    self.df[text_col2],
                                    margins=True))
    #5.异常值
    def outlier(self):
        for col in self.num_cols_corr:
            Q1=self.df[col].quantile(0.25)
            Q3=self.df[col].quantile(0.75)
            IQR=Q3-Q1
            lower = Q1-1.5*IQR
            upper = Q3+1.5*IQR
            print(f'===={col}异常值====\n', 
            self.df[(self.df[col]<lower) | (self.df[col]>upper)])
    #run
    def run(self):
        self.overview()
        self.integrity()
        self.distribution()
        self.correlation()
        self.outlier()
        self.visualize()

    #6.可视化
    def visualize(self):
        plt.figure(figsize = (8,6))
        plt.title('豆瓣Top100直方图')
        plt.xlabel('评分')
        plt.ylabel('电影数量')
        sns.histplot(data = self.df, x = 'rating', bins = 10, kde = True)
        plt.show()
        #boxplot
        plt.figure(figsize = (8,6))
        plt.title('豆瓣Top100箱线图')
        plt.ylabel('评分')
        sns.boxplot(data = self.df, y = 'rating')
        plt.show()
        #pie
        plt.figure(figsize = (8,6))
        plt.title('豆瓣Top100饼状图')
        plt.pie(self.df['rating'].value_counts(), 
                labels = self.df['rating'].value_counts().index,
                autopct = '%1.1f%%')
        plt.show()
        #scatter
        plt.figure(figsize = (8,6))
        plt.title('豆瓣Top100散点图')
        plt.xlabel('评分')
        plt.ylabel('评价人数')
        sns.scatterplot(data = self.df, x = 'rating', y = 'review_count', 
                        hue='rating', style='rating', 
                        size='review_count', alpha=0.6, palette='viridis')
        plt.show()
        #heatmap
        plt.figure(figsize = (8,6))
        plt.title('豆瓣Top100相关系数热力图')
        sns.heatmap(self.df[self.num_cols_corr].corr(), 
                    annot = True,
                    cmap = 'coolwarm',
                    linewidths = 0.5,
                    linecolor = 'black')
        plt.show()
        #分类频数
        plt.figure(figsize = (8,6))
        plt.title('豆瓣Top100国家频数')
        plt.xlabel('国家')
        plt.ylabel('电影数量')
        sns.countplot(data = self.df, x = 'country')
        plt.xticks(rotation=45)
        plt.show()
        #时序演进
        plt.figure(figsize = (8,6))
        plt.title('豆瓣Top100上映时间演进')
        plt.xlabel('上映时间')
        plt.ylabel('评价人数')
        sns.lineplot(data = self.df, x = 'release_date', y = 'review_count', 
                    hue = 'country', size = 'review_count', 
                    alpha = 0.6, palette = 'viridis')
        plt.show()

if __name__ == '__main__':
    eda = DoubanEDA()
    eda.run()        
