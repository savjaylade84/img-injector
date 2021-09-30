

def extractFileToHexFormat(file,text):
    with open(f'{file}','rb') as file:
        with open(f'{text}','w') as text:
            text.write(str(file.read()))   

file = input('[executable filename]:')
text = input('[text filename]: ')
extractFileToHexFormat(file,text)

