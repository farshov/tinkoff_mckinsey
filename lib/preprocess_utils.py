import numpy as np
from datetime import datetime


def calc_duration(data, nan='NAN'):
    """
    Claculating of duration of using of Tinkoff app in years
    :param data: dataframe containing column first_session_dttm
           nan: format of Nanin your dataframe
    :return: None, adds column of duration in-place
    """
    new_col = [0] * len(data)
    for i in range(len(data)):
        date = data.first_session_dttm[i]
        if date != nan:
            duration = (datetime.today() - datetime.strptime(data.first_session_dttm[i],
                                                             '%Y-%m-%d %H:%M:%S')).days / 365
            new_col[i] = duration

    na = np.average(new_col)
    for i in range(len(data)):
        date = data.first_session_dttm[i]
        if date == nan:
            duration = na
            new_col[i] = duration
    data['duration'] = new_col


def transform_to_year(data, nan='NAN'):
    """
        Transforming datetime into just year
        :param data: dataframe containing column first_session_dttm
               nan: format of Nanin your dataframe
        :return: None, adds column of duration in-place
        """
    years = [nan] * len(data)
    for i in range(len(data)):
        date = data.first_session_dttm[i]
        if date != nan and isinstance(date, str):
            years[i] = datetime.strptime(data.first_session_dttm[i], '%Y-%m-%d %H:%M:%S').year
    data.first_session_dttm = years
