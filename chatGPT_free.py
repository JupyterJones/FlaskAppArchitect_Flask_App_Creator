import g4f
dir(g4f)

#print(g4f.Provider.Ails.params)  # supported args

# Automatic selection of provider
'''
# normal response
response = g4f.ChatCompletion.create(
    model=g4f.models.gpt_4,
    messages=[{"role": "user", "content": "hi"}],
)  # alterative model setting


for message in response:
    print(message)
    '''