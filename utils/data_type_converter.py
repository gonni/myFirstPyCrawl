class DataConverter:
    def convert_number(self, text) -> float:
        negative = 1
        if text[0] == '+':
            text = text[1:]
            negative = 1
        elif text[0] == '-':
            text = text[1:]
            negative = -1
        if text.endswith('%'):
            text = text[:-1]
        text = text.replace(',', '')
        return float(text) * negative

    def convert_updown_number(self, text) -> float:
        if text.find('보합') == 0:
            return 0.0
        tokens = text.split()
        if tokens[0] == '하락':
            return float(tokens[1]) * -1
        else :
            return float(tokens[1])


def convert_number(text) -> float:
    negative = 1
    if text[0] == '+':
        text = text[1:]
        negative = 1
    elif text[0] == '-':
        text = text[1:]
        negative = -1
    if text.endswith('%'):
        text = text[:-1]
    text = text.replace(',', '')
    return float(text) * negative


def convert_updown_number(text) -> float:
    if text.find('보합') == 0:
        return 0.0

    tokens = text.split()
    if tokens[0] == '하락':
        return float(tokens[1]) * -1
    else :
        return float(tokens[1])


