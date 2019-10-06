import numpy as np
from datetime import datetime
import pandas as pd


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


def aggregate_transactions(path):
    transactions = pd.read_csv(path)
    transactions.index = transactions.customer_id
    transaction = transactions.drop(columns='customer_id')
    av = []
    av_n_z = []
    num_tr = []
    num_tr_n_z = []
    idxs = np.unique(transaction.index)
    for i in idxs:
        data = transaction.loc[i]
        if type(data) != pd.core.series.Series:
            num_tr.append(len(data.transaction_amt))
            av.append(np.mean(data.transaction_amt))
            if sum(data.transaction_amt != 0) > 0:
                num_tr_n_z.append(sum(data.transaction_amt[data.transaction_amt != 0]))
                av_n_z.append(np.mean(data.transaction_amt[data.transaction_amt != 0]))
            else:
                num_tr_n_z.append(1.)
                av_n_z.append(0.)
        else:
            num_tr.append(1.)
            num_tr_n_z.append(1.)
            av.append(0.)
            av_n_z.append(0.)
    tr_data = np.array([av, av_n_z, num_tr, num_tr_n_z]).T
    tr_data = pd.DataFrame(tr_data, index=idxs, columns=['av', 'av_n_z', 'num_tr', 'num_tr_n_z'])
    return tr_data
