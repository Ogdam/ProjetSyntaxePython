from tokenizer.tokenizer import tokenizer

with open("test.py", 'r', encoding='utf-8') as testfile:
    a = testfile.read()
    a = tokenizer(a)
