from sklearn.model_selection import GridSearchCV


class PA:
    type = 'parameter adjustment'

    # def __init__(self, learning_rate=None, max_depth=None, min_child_weight=None, gamma=None, reg_lambda=None,
    #              subsample=None, colsample_bytree=None,n_estimators=None):
    #     self.learning_rate = learning_rate
    #     self.max_depth = max_depth
    #     self.min_child_weight = min_child_weight
    #     self.gamma = gamma
    #     self.reg_lambda = reg_lambda
    #     self.subsample = subsample
    #     self.subsample = subsample
    #     self.colsample_bytree = colsample_bytree
    #     self.n_estimators = n_estimators
    def __init__(self,params):
        self.params = params


