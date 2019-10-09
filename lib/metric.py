import numpy as np


def competition_metric(events, scores):
    weights = {
        'dislike': -10,
        'skip': -0.1,
        'view': 0.1,
        'like': 0.5
    }
    
    return sum([s * weights[e] for e, s in zip(events, scores)])


def probas2scores(events, probas):
    labels = dict(zip(['dislike', 'skip', 'view', 'like'], np.arange(4)))
    
    scores = [p[labels[e]] for e, p in zip(events, probas)]
    
    for i, e in enumerate(events):
        if e in ['skip', 'dislike']:
            scores[i] *= -1
    
    return scores


def probas2scores_xgb(labels, probas):
    mapping = {
        'dislike': [0, -1],
        'like': [1, 1],
        'skip': [2, -1],
        'view': [3, 1]
    }

    scores = []
    for i in range(len(probas)):
        scores.append(probas[i][mapping[labels[i]][0]] * mapping[labels[i]][1])
    return scores


def extract_date_features(date):
    """

    :param date: datetime formate
    :return:  some useful features, you can understand them by their names
    """

    weekday = [0] * 7
    weekday[date.weekday()] = 1

    is_holiday = 0
    if date.weekday() == 5 or date.weekday() == 6:
        is_holiday = 1

    is_work_time = 0
    if 9 < date.hour < 18:
        is_work_time = 1

    return weekday + [is_holiday] + [is_work_time]
