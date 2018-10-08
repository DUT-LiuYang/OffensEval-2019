class PreProcessor:
    """
    After reading raw text from the origin files.
    We adopt the PreProcessor to process the text.
    """

    def __init__(self):
        self.dir = "../instance/"

    @staticmethod
    def remove_substr(sentence="", len=0, sub="", replace=""):
        index = sentence.find(sub)
        while index != -1:
            temp = sentence[0:index]
            index = sentence.find(' ', index + len)
            if index == -1:
                sentence = temp + replace
                break
            else:
                sentence = temp + replace + sentence[index:]
                index = sentence.find('@', index)

        return sentence

    @staticmethod
    def clean_sentence(sentence=""):

        sentence = sentence.replace('$', ' ')

        sentence = PreProcessor.remove_substr(sentence, 2, "@", "@user")
        sentence = PreProcessor.remove_substr(sentence, 0, "https", "url")

        while "  " in sentence:
            sentence = sentence.replace('  ', ' ')

        return sentence


if __name__ == '__main__':
    pass
