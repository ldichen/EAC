from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score


class ME:
    type = 'modelEvaluation'

    def __init__(self, y_true, y_pred):
        self.true = y_true
        self.pred = y_pred
    def macro_p(self):
        macro_precision = precision_score(self.true, self.pred, average='macro')
        print("Macro-average precision:", macro_precision)
        return macro_precision

    def macro_r(self):
        macro_recall = recall_score(self.true, self.pred, average='macro')
        print("Macro-average recall:", macro_recall)
        return macro_recall

    def macro_f1(self):
        # 计算Macro-average的F1分数
        macro_f1 = f1_score(self.true, self.pred, average='macro')
        print("Macro-average F1:", macro_f1)
        return macro_f1

    def weighted_p(self):
        weighted_precision = precision_score(self.true, self.pred, average='weighted')
        print("Weighted-average precision:", weighted_precision)
        return weighted_precision

    def weighted_r(self):
        weighted_recall = recall_score(self.true, self.pred, average='weighted')
        print("Weighted-average recall:", weighted_recall)
        return weighted_recall

    def weighted_f1(self):
        # 计算weighted-average的F1分数
        weighted_f1 = f1_score(self.true, self.pred, average='weighted')
        print("Weighted-average F1:", weighted_f1)
        return weighted_f1

    def micro_p(self):
        micro_precision = precision_score(self.true, self.pred, average='micro')
        print("Micro-average precision:", micro_precision)
        return micro_precision

    def micro_r(self):
        micro_recall = recall_score(self.true, self.pred, average='micro')
        print("Micro-average recall:", micro_recall)
        return micro_recall

    def micro_f1(self):
        # 计算micro-average的F1分数
        micro_f1 = f1_score(self.true, self.pred, average='micro')
        print("Micro-average F1:", micro_f1)
        return micro_f1
