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
