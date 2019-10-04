import numpy as np


def calc_duration(data):
    """
    Claculating of duration of using of Tinkoff app in years
    :param data: dataframe containing column first_session_dttm
    :return: None, adds column of duration in-place
    """
    new_col = [0] * len(data)
    for i in range(len(data)):
        date = data.first_session_dttm[i]
        if date != 'NAN':
            duration = (datetime.today() - datetime.strptime(data.first_session_dttm[i],
                                                             '%Y-%m-%d %H:%M:%S')).days / 365
            new_col[i] = duration

    na = np.average(new_col)
    for i in range(len(data)):
        date = data.first_session_dttm[i]
        if date == 'NAN':
            duration = na
            new_col[i] = duration
    data['duration'] = new_col