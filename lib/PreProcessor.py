class PreProcessor:
    """
    After reading raw text from the origin files.
    We use a script to segment words and adopt the PreProcessor to process the text.
    """

    def __init__(self):
        self.dir = "../instance/"
        self.data_dir = "../resource/"

    def read_sentences(self, file=""):
        sentences = []
        rf = open(self.data_dir + file, 'r', encoding='utf-8')
        while True:
            line = rf.readline()
            if line == "":
                break
            sentences.append(line)
        rf.close()
        return sentences

    @staticmethod
    def remove_substr(sentence="", offset=0, sub="", replace=""):
        index = sentence.find(sub)
        length = len(replace)
        # print(sentence)
        while index >= 0:
            # print(str(index))
            x = sentence.find(sub, index + 1)
            y = index

            temp = sentence[0:index]
            index = sentence.find(' ', index + offset)
            if index == -1:
                sentence = temp + replace
                break
            else:
                sentence = temp + replace + sentence[index:]
                index = x - (index - y - length)

        return sentence

    @staticmethod
    def clean_sentence(sentence=""):

        sentence = sentence.replace('$', ' ')

        sentence = PreProcessor.remove_substr(sentence, 2, "@", "@user")
        sentence = PreProcessor.remove_substr(sentence, 0, "https", "url")

        while "  " in sentence:
            sentence = sentence.replace('  ', ' ')

        return sentence.strip("\n")

    def convert_raw_text(self, raw_file="", file=""):

        sentences = self.read_sentences(raw_file)

        wf = open(self.dir + file, 'w', encoding='utf-8')
        for sentence in sentences:
            wf.write(PreProcessor.clean_sentence(sentence) + "\n")
        wf.close()


if __name__ == '__main__':
    raw_file = "out.txt"
    file = "sub1.txt"

    p = PreProcessor()
    p.convert_raw_text(raw_file, file)
