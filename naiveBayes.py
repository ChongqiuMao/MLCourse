
import numpy as np
from utils import *
from IPython import embed

if __name__ == '__main__':
    trainfilename = 'propublicaTrain.csv'
    testfilename = 'propublicaTest.csv'

    """
    def bin_feat1(x):   # age
        x = float(x)
        return int(x/5)

    def bin_feat6(x):   # count
        x = float(x)
        return int(x/3)

    binid = lambda x: x
    bins = None
    bins = [binid, bin_feat1, binid, binid, binid, binid, binid, binid, binid]
    """
    bins = None
    y_gt, features, type_0, type_1, _ = dataset_process(trainfilename, False, 0, int32=True, binfunc=bins)
    test_y_gt, test_features, test_type_0, test_type_1, _ = dataset_process(testfilename, False, 0, int32=True, binfunc=bins)

    # embed()
    # Training
    N = features.shape[0]
    M = features.shape[1]
    
    # Prior
    logp_Y0 = np.log(len(type_0) / N)
    logp_Y1 = np.log(len(type_1) / N)

    # Likelihood
    p_xiy0 = [{} for _ in range(M)] # Count P(x|y)
    p_xiy1 = [{} for _ in range(M)]
    p_xy0 = [0 for _ in range(M)]   # Sum P(x|y)
    p_xy1 = [0 for _ in range(M)]
    diy0 = [0 for _ in range(M)]    # d in additive smoothing
    diy1 = [0 for _ in range(M)]

    for y0sample in type_0:
        for i in range(M):
            feati = y0sample[i]
            if feati not in p_xiy0[i]:
                p_xiy0[i][feati] = 0
            p_xiy0[i][feati] += 1
    for i in range(M):
        p_xy0[i] = sum(p_xiy0[i].values())
        diy0[i] = len(p_xiy0[i].keys())

    for y1sample in type_1:
        for i in range(M):
            feati = y1sample[i]
            if feati not in p_xiy1[i]:
                p_xiy1[i][feati] = 0
            p_xiy1[i][feati] += 1
    for i in range(M):
        p_xy1[i] = sum(p_xiy1[i].values())
        diy1[i] = len(p_xiy1[i].keys())


    correct = 0
    alpha = 1                       # additive smoothing factor
    # embed()

    for i in range(test_features.shape[0]):
        data = test_features[i]
        p_y0 = logp_Y0
        p_y1 = logp_Y1
        # p_y0, p_y1 = np.exp(logp_Y0), np.exp(logp_Y1)
        for j in range(1, M):
            featj = data[j]
            """
            if featj not in p_xiy0:
                p_y0 = -np.inf
            else:
                p_y0 += np.log(p_xiy0[j][featj] / p_xy0[j])
            if featj not in p_xiy1:
                p_y1 = -np.inf
            else:
                p_y1 += np.log(p_xiy1[j][featj] / p_xy1[j])
            """
            # p_y0 *= 1e-10 if featj not in p_xiy0[j] else p_xiy0[j][featj] / p_xy0[j]
            # p_y1 *= 1e-10 if featj not in p_xiy1[j] else p_xiy1[j][featj] / p_xy1[j]
            
            tmp = 0 if featj not in p_xiy0[j] else p_xiy0[j][featj]
            p_y0 += np.log( (tmp + alpha) / (p_xy0[j] + diy0[j] * alpha) )
            tmp = 0 if featj not in p_xiy1[j] else p_xiy1[j][featj]
            p_y1 += np.log( (tmp + alpha) / (p_xy1[j] + diy1[j] * alpha) )

        if p_y0 >= p_y1:
            if test_y_gt[i] == 0:
                correct += 1
        else:
            if test_y_gt[i] == 1:
                correct += 1

    print("accuracy: {:8f}".format(correct * 1.0 / test_features.shape[0]))



