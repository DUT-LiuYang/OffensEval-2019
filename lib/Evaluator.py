class Evaluator:

    def __init__(self, true_labels=[], sentences=[], task=1):
        self.max_F1 = -1
        self.max_F1_epoch = -1

        self.true_labels = true_labels

        if task == 1:
            self.nums = [0] * 2
        elif task == 2:
            self.nums = [0] * 3
        elif task == 3:
            self.nums = [0] * 4

        self.dir = "../results/"
        self.word_index_dir = "../laptop_data/word_index.txt"

        self.sentences = sentences
        self.index_word = self.load_index_word()
        self.save_results(true_labels, self.dir + "true_label.txt")

    def get_each_category_num(self, true_labels=[]):
        for label in true_labels:
            for index, val in enumerate(label):
                self.nums[index] += val

        print("nums of each class are as follow:")
        res = ""
        for num in self.nums:
            res += str(num) + " "
        print(res)

    @staticmethod
    def save_results(predictions=[], file=''):
        wf = open(file, 'w')
        for label in predictions:
            wf.write(str(label) + "\n")
        wf.close()

    @staticmethod
    def calculate_f_score(p_p=0, pr_p=0, num=0):
        if p_p == 0:
            return 0, 0, 0

        P = float(pr_p) / p_p
        R = float(pr_p) / num
        if P == 0 or R == 0:
            return 0, 0, 0
        F = 2 * P * R / (P + R)

        return P, R, F

    def get_macro_f1(self, predictions=[], epoch=-1, task=1):
        predictions = self.get_predicted_label(predictions)

        # here is special in this task.
        p_temp = [0] * (task + 1)
        pr_temp = [0] * (task + 1)

        for label, true_label in zip(predictions, self.true_labels):
            p_temp[label] += 1
            if label == true_label:
                pr_temp[label] += 1

        # F_scores = []
        F_sum = 0

        for p_p, pr, num in zip(p_temp, pr_temp, self.nums):
            p, r, f = self.calculate_f_score(p_p, pr, num)
            # F_scores.append([p, r, f])
            print(str(p_p) + " : " + str(p) + " " + str(r) + " " + str(f))
            F_sum += f

        F = F_sum / (task + 1)

        if F > self.max_F1:
            self.max_F1 = F
            self.max_F1_epoch = epoch
            self.save_results(predictions=predictions, file=self.dir + str(epoch) + ".txt")
            self.error_analysis(true_labels=self.true_labels,
                                predicted_labels=predictions,
                                sentences=self.sentences,
                                error_analysis_file=self.dir + "e_a_" + str(epoch) + ".txt")

    @staticmethod
    def get_predicted_label(predictions=[]):
        prediction_labels = []

        for scores in predictions:
            index = 0
            max = -100
            for i, score in enumerate(scores):
                if score > max:
                    max = score
                    index = i
            prediction_labels.append(index)

        return prediction_labels

    def error_analysis(self, true_labels=[], predicted_labels=[],
                       sentences=[], error_analysis_file=""):
        wf = open(error_analysis_file, 'w')

        for label, true_label, sentence in zip(predicted_labels, true_labels, sentences):
            if label != true_label:
                wf.write(str(true_label) + "-" + str(label) + "#")
                temp = ""
                for index in sentence:
                    if index == 0:
                        break
                    else:
                        temp += self.index_word[index] + " "
                wf.write(temp + "###")

        wf.close()

    def load_index_word(self):
        index_word = {}
        rf = open(self.word_index_dir, 'r')
        while True:
            line = rf.readline()
            if line == "":
                break
            line = line.split()
            index_word[int(line[1])] = line[0]
        rf.close()
        return index_word


if __name__ == '__main__':
    pass
