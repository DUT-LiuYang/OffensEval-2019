class FileReader:

    map1 = {"NOT": 0, "OFF": 1}
    map2 = {"TIN": 0, "TTH": 1, "UNT": 2}
    map3 = {"IND": 0, "GRP": 1, "ORG": 2, "OTH": 3}
    dir = "../resource/"

    def __init__(self):
        pass

    @staticmethod
    def read_file(file="", train=True):
        """
        read the raw text and labels from the origin file.
        :param file:
        :param train:
        :return:
        """
        sentences = []
        max_len = 0

        label1 = []
        label2 = []
        label3 = []

        sentences2 = []
        sentences3 = []

        index1 = 0
        index2 = 0
        index3 = 0

        rf = open(FileReader.dir + file, 'r', encoding='utf-8')

        while True:
            line = rf.readline()
            if line == "":
                break
            data = line.strip("\n").split("\t")
            data[0] = data[0].replace("“", "\"").replace("”", "\"")

            temp = len(data[0].split(" "))
            if temp > max_len:
                max_len = temp

            sentences.append(data[0])
            # print(str(len(data)))
            if train:
                # label1.append([0] * 2)
                temp = FileReader.map1[data[1]]
                # label1[index1][temp] = 1
                label1.append(temp)

                if temp != 0:

                    sentences2.append(data[0])
                    # label2.append([0] * 3)
                    temp = FileReader.map2[data[2]]
                    # label2[index2][temp] = 1
                    label2.append(temp)

                    index2 += 1

                    if temp != 2:
                        sentences3.append(data[0])
                        # label3.append([0] * 4)
                        # label3[index3][FileReader.map3[data[3]]] = 1
                        label3.append(FileReader.map3[data[3]])
                        index3 += 1

            index1 += 1

        rf.close()

        print("max length in " + file + " is " + str(max_len))

        if not train:
            return sentences, max_len
        else:
            return sentences, sentences2, sentences3, label1, label2, label3, max_len

    @staticmethod
    def write_file(sentences=[], file=""):
        wf = open(FileReader.dir + file, 'w', encoding='utf-8')

        for str in sentences:
            wf.write(str.strip() + "\n")

        wf.close()

    @staticmethod
    def write_label(labels=[], file=""):
        wf = open(FileReader.dir + file, 'w', encoding='utf-8')

        for label in labels:
            wf.write(str(label) + "\n")

        wf.close()


if __name__ == '__main__':
    file = "offenseval-trial.txt"
    file_reader = FileReader()
    sentences, sentences2, sentences3, label1, label2, label3, max_len = file_reader.read_file(file)

    file1 = "sentences-sub-task1.txt"
    file2 = "sentences-sub-task2.txt"
    file3 = "sentences-sub-task3.txt"

    file_reader.write_file(sentences, file1)
    file_reader.write_file(sentences2, file2)
    file_reader.write_file(sentences3, file3)

    file1 = "labels-sub-task1.txt"
    file2 = "labels-sub-task2.txt"
    file3 = "labels-sub-task3.txt"

    file_reader.write_label(label1, file1)
    file_reader.write_label(label2, file2)
    file_reader.write_label(label3, file3)
