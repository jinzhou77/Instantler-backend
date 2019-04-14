from User.models import UserVector
import numpy as np
from sklearn.neighbors import NearestNeighbors
from .utils import columnNames
import math

def getSimilarUsers(user_id, num):
    querySet = UserVector.objects.all()
    params = querySet.values_list(*columnNames)
    UVs = np.array([arr for arr in params])
    tmp = UVs[:,0].reshape((len(UVs)))
    targetIndex = (tmp == int(user_id))
    nonTargetIndex = (tmp != int(user_id))
    nn = NearestNeighbors(metric='cosine')
    target,nonTarget = UVs[targetIndex], UVs[nonTargetIndex]
    nn.fit(nonTarget[:,1:])
    res = []
    tmp = nn.kneighbors(target[:, 1:], num, return_distance=False)
    for index in tmp[0]:
        res += [nonTarget[index][0]]
    return res

def getCategoryList(user_id, num):
    querySet = UserVector.objects.filter(user=user_id)
    params = querySet.values_list(*columnNames)
    UV = np.array([arr for arr in params])[0][1:]
    sum = np.sum(UV)
    distr = np.array([int(math.ceil(num*i/sum)) for i in UV])
    return(distr)
