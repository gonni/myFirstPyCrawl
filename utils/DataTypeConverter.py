def convert_updown_number(text) -> float:
    if text.find('보합') == 0:
        return 0.0

    tokens = text.split()
    if tokens[0] == '하락':
        return float(tokens[1]) * -1
    else :
        return float(tokens[1])
# tx = '''하락
# 				425'''
# print(convert_updown_number(tx))


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
# print(convert_number('12,123,123'))


def convert_uck(text) -> int:
    negative = 1
    if text[0] == '+':
        text = text[1:]
        negative = 1
    elif text[0] == '-':
        text = text[1:]
        negative = -1

    if text.endswith('%'):
        text = text[:-1]
    elif text.endswith('억'):
        text = text[:-1] + '00000000'

    text = text.replace(',', '')
    return int(text) * negative

print(convert_uck('+762억'))
