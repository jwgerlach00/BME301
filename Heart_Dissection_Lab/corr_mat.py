import pandas as pd
import numpy as np
from statistics import stdev, mean
from scipy.stats import pearsonr
import matplotlib.pyplot as plt


class CorrMatrix:
    def __init__(self, df):
        # Import and format data.
        self.data = df
        self.corr_matrix = None
        self.p_matrix = None

    def run_all(self):
        """
        Runs all class methods.
        """
        self.construct_r_mat()
        self.calculate_p_values()
        self.export_mat('correlation_matrix.xlsx', 'p_matrix.xlsx')

    def construct_r_mat(self, remove_redundant=True):
        """
        Constructs a correlation matrix from the dataset.
        :param remove_redundant: Introduce a diagonal split to the dataset to remove redundant comparisons.
        """
        self.corr_matrix = self.data.corr(method='pearson').round(decimals=3)
        if remove_redundant:
            self.corr_matrix = self.corr_matrix.mask(np.tril(np.ones(self.corr_matrix.shape)).astype(np.bool))
            self.corr_matrix.fillna('---', inplace=True)

    def export_mat(self, corr_out, p_out):
        """
        Exports both the correlation and the p-value matrices to excel.
        :param corr_out: correlation output path (.xlsx)
        :param p_out: p-value output path (.xlsx)
        """
        self.corr_matrix.to_excel(corr_out)
        self.p_matrix.to_excel(p_out)

    def calculate_p_values(self, remove_redundant=True):
        """
        Constructs a p-value matrix from the dataset.
        """

        # Drop blanks
        df = self.data.dropna()

        df_cols = pd.DataFrame(columns=df.columns)
        p_values = df_cols.transpose().join(df_cols, how='outer')

        for r in df.columns:
            for c in df.columns:
                p_values[r][c] = round(pearsonr(df[r], df[c])[1], 3)

        self.p_matrix = p_values

        if remove_redundant:
            self.p_matrix = self.p_matrix.mask(np.tril(np.ones(self.p_matrix.shape)).astype(np.bool))
            self.p_matrix.fillna('---', inplace=True)


class BuildData:
    def __init__(self, df):
        """
        Initialize attributes.
        :param df: Pandas DataFrame
        """
        self.data = df
        self.outliers = None
        self.means = None
        self.stds = None
        self.title = None

    def run_all(self):
        """
        Runs all class methods.
        """
        self.format_header()
        self.remove_outliers()

    def format_header(self):
        """
        Hardcoded formatting of the dataset header.
        """
        self.title = ['LAV Diam (mm)', 'RAV Diam (mm)', 'Aortic Diam (mm)', 'Pulmonary Diam (mm)', 'Atria Vol (mL)',
                      'LV + S Vol (mL)', 'RV Vol (mL)', '(LV + S)/RV Vol (mL)']

        self.data.drop(columns=['Name of Student 1 ', 'Name of Student 2 ', 'Name of Student 3'], inplace=True)
        self.data.columns = self.title

    def stats(self):
        """
        Computes stats for the dataset and saves as attributes.
        """
        # Calculate mean of each measurement type
        self.means = [mean(self.data[col]) for col in self.data.columns]

        # Calculate standard deviations of each measurement type
        self.stds = [stdev(self.data[col]) for col in self.data.columns]

    def remove_outliers(self):
        """
        Removes outliers > 3 or < 3 standard deviations from the mean. Updates stats.
        """
        self.stats()

        drop_indices = []
        for col_n, col_name in enumerate(self.data.columns):

            for row_n, value in enumerate(self.data[col_name]):

                if value < self.means[col_n] - 3 * self.stds[col_n] or value > self.means[col_n] + 3 * self.stds[col_n]:
                    # Drop entire row if the value is +/- 3 standard deviations from the column mean
                    drop_indices.append(row_n)

        # Remove duplicate indices
        drop_indices = list(set(drop_indices))

        # Save identified outliers
        self.outliers = self.data.iloc[drop_indices]

        # Drop outliers and reset index
        self.data.drop(index=drop_indices, inplace=True)
        self.data.reset_index(drop=True, inplace=True)

        # Recompute stats after dropping outliers
        print(self.means)
        print(self.stds)
        self.stats()


if __name__ == '__main__':
    # Import raw data
    input_path = 'Heart Dissection Group Data - Sheet1.csv'
    data = pd.read_csv(input_path)

    # Refine input data
    build_data = BuildData(data)
    build_data.run_all()

    # Construct correlation and p-value matrices and write to Excel
    corr_mat = CorrMatrix(data)
    corr_mat.run_all()

    # Export outliers and stats
    build_data.outliers.to_excel('outliers.xlsx')
    stats_df = pd.concat([pd.Series(build_data.means).round(3), pd.Series(build_data.stds).round(3)], axis=1).transpose()
    stats_df.columns = build_data.data.columns
    stats_df.to_excel('stats.xlsx')

    # Plot data
    y_name = 'RV Vol (mL)'
    y = build_data.data[y_name]
    x_name = 'LV + S Vol (mL)'
    x = build_data.data[x_name]
    m, b = np.polyfit(x, y, 1)  # generate line fit equation in the form mx + b
    plt.scatter(x, y)
    plt.plot(x, m*x + b)
    plt.xlabel(x_name); plt.ylabel(y_name); plt.title('{0} vs. {1}'.format(x_name, y_name))
    plt.show()

    x_name = '(LV + S)/RV Vol (mL)'
    x = build_data.data[x_name]
    m, b = np.polyfit(x, y, 1) # generate line fit equation in the form mx + b
    plt.scatter(x, y)
    plt.plot(x, m*x + b)
    plt.xlabel(x_name); plt.ylabel(y_name); plt.title('{0} vs. {1}'.format(x_name, y_name))
    plt.show()

