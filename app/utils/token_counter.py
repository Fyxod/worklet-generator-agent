import sentencepiece as spm
sp = spm.SentencePieceProcessor(model_file='test/test_model.model')

sp.encode('This is a test')
# sp = spm.SentencePieceProcessor()
# sp.load("path/to/tokenizer.model")

# Example usage
text = "This is a test."
tokens = sp.encode(text, out_type=str)
print(tokens)
