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
        if e in ['view', 'dislike']:
            scores[i] *= -1
    
    return scores
    