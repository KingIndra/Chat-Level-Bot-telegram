def remove_unsupported_letter(text):
    return text.replace('<',">")

def getHyperLink(user_id, first_name):
    first_name = remove_unsupported_letter(first_name)
    hyper_name = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    return hyper_name

def is_a_valid_name(test_str):
    # test_str = remove_unsupported_letter(test_str)
    res = test_str != '' and all(chr.isalpha() or chr.isspace() for chr in test_str)
    return res

def gethtmlLink(user_id, first_name):
    first_name = remove_unsupported_letter(first_name)
    hyper_name = f'<a href="tg://user?id={user_id}">{first_name}</a>'
    return hyper_name

def a(chat_id, text):
    # text = remove_unsupported_letter(text)
    hyper_name = f'<a href="tg://user?id={chat_id}">{text}</a>'
    return hyper_name

def bold(text):
    # text = remove_unsupported_letter(text)
    return f"<b>{text}</b>"