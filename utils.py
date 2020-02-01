def remove_brackets(s):
    import re

    parts = re.split('\[|\]', s)
    return ''.join([parts[i] for i in range(len(parts)) if i % 2 == 0])


def get_grouper(args):
    import nltk

    if args.grouper == 'porter':
        return nltk.PorterStemmer().stem
    elif args.grouper == 'lancaster':
        return nltk.LancasterStemmer().stem
    else:
        lemmatizer = nltk.WordNetLemmatizer()
        return lambda s: lemmatizer.lemmatize(s, pos='v')


def num_to_superscript(num):
    return ''.join([{'0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
                     '+': '⁺', '-': '⁻', '.': '⋅'}[d] for d in str(num)])
