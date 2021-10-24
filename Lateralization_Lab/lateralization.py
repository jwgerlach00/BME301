import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class IndividualData:
    def __init__(self, file_path):
        self.data = pd.read_excel(file_path)

    def compute_error(self):
        """
        Computes the error between each target and prediction -- smallest error magnitude given bounds of 0 to 360
        degrees.
        :return: errors
        """
        errors = []
        for i in range(len(self.data)):
            target = self.data.iloc[i]['Target']
            prediction = self.data.iloc[i]['Prediction']

            # Account for distance from angle in either polar direction
            diff = abs(target - prediction)
            errors.append(diff if diff < 360 - diff else 360 - diff)

        return errors

    def append_error(self, error_name='Error'):
        """
        Appends error column to data attribute.
        """
        error_col = self.compute_error()
        self.data[error_name] = error_col

    def split_dataset(self):
        """
        Splits the ata attribute into two parts.
        :return: first pd DataFrame, second pd DataFrame
        """
        first, second = np.array_split(self.data, 2)
        return first, second


class ClassData(IndividualData):
    def __init__(self, file_path, targets):
        super().__init__(file_path)
        self.targets = targets

    def average(self):
        self.data = pd.DataFrame(self.data.mean(axis=1), columns=['Prediction'])

    def append_targets(self):
        self.data['Target'] = self.targets


if __name__ == '__main__':
    individual_data = IndividualData('individual_data.xlsx')
    individual_data.append_error()
    individual_data.data.to_excel('individual_error_data.xlsx', index=False)

    class_data = ClassData('class_data.xlsx', targets=individual_data.data['Target'].tolist())
    class_data.average()
    class_data.append_targets()
    class_data.append_error()
    class_data.data.to_excel('class_error_data.xlsx', index=False)

    # Split datasets into first and second trial
    first_ind, second_ind = individual_data.split_dataset()
    first_class, second_class = class_data.split_dataset()

    # Sort datasets ascending by true angle
    def sort_by_target(data, target_name='Target'):
        data.sort_values(target_name, inplace=True)
        return data
    first_ind = sort_by_target(first_ind)
    second_ind = sort_by_target(second_ind)
    first_class = sort_by_target(first_class)
    second_class = sort_by_target(second_class)


    def plot_data(first_trial, second_trial, plot_title, target_name='Target', error_name='Error'):
        plt.figure()
        plt.plot(first_trial[target_name], first_trial[error_name])
        plt.plot(second_trial[target_name], second_trial[error_name])
        plt.xlabel('{0} Angle (degrees)'.format(target_name))
        plt.title(plot_title)
        plt.ylabel(error_name)
        plt.legend(['trial 1', 'trial 2'])
        plt.savefig('{0}.png'.format(plot_title.replace(' ', '_')))

    plot_data(first_ind, second_ind, 'Individual Lateralization Data')
    plot_data(first_class, second_class, 'Class Lateralization Data')

    mean_df = pd.DataFrame([[first_ind['Error'].mean(), second_ind['Error'].mean()],
                            [first_class['Error'].mean(), second_class['Error'].mean()]],
                           index=['Individual', 'Class'], columns=['Trial 1', 'Trial 2'])

    mean_df.to_excel('means_output.xlsx')

