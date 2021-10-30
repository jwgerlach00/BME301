# def remove_outliers(df, means, stds):
#     """
#     Removes outliers > 3 or < 3 standard deviations from the mean. Updates stats.
#     """
#
#     drop_indices = []
#     for col_n, col_name in enumerate(df.columns):
#
#         for row_n, value in enumerate(df[col_name]):
#
#             if value < means[col_n] - 3 * stds[col_n] or value > means[col_n] + 3 * stds[col_n]:
#                 # Drop entire row if the value is +/- 3 standard deviations from the column mean
#                 drop_indices.append(row_n)
#
#     # Remove duplicate indices
#     drop_indices = list(set(drop_indices))
#
#     # Save identified outliers
#     self.outliers = self.data.iloc[drop_indices]
#
#     # Drop outliers and reset index
#     self.data.drop(index=drop_indices, inplace=True)
#     self.data.reset_index(drop=True, inplace=True)
#
#     # Recompute stats after dropping outliers
#     print(self.means)
#     print(self.stds)
#     self.stats()

def compute_angle_error(prediction, target):
    """
    Computes error while accounting for distance from angle in polar coordinates.
    :param prediction: predicted angle value
    :param target: actual angle value
    :return: error
    """
    diff = abs(target - prediction)

    return diff if diff < 360 - diff else 360 - diff
