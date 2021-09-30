"""
    Author: John Jayson B. De Leon
    Github: savjaylade84
    Email:savjaylade84@gmail.com

    tools for injecting executable code in the image
    using python.

    usage: img-inject [option] <image-name> <code file>
"""

import argparse

parser = argparse.ArgumentParser(
description='''python tools for injecting,extracting,and removing executable code in the image.''',
formatter_class=argparse.RawDescriptionHelpFormatter,epilog=''' 
Author: John Jayson B. De Leon 
Email: savjaylade84@gmail.com 
Github: savjaylade84 
    ''',prog='python3 img-inject.py',usage='%(prog)s [options] <image> <executable-code>')

parser.add_argument("image",help="image name")
parser.add_argument("executable",help="executable code")

parser.add_argument('-r','--remove'
                                 ,help='remove code from the image'
                                 ,action='store_true'
                                 ,default=False)

parser.add_argument('-e','--extract'
                                 ,help='extract code from the image'
                                 ,action='store_true'
                                 ,default=False)

parser.add_argument('-x','--isExist'
                                 ,help='read the image and show if there\'s existing code'
                                 ,action='store_true'
                                 ,default=False)

parser.add_argument('-i','--inject'
                                 ,help='inject the executable code'
                                 ,action='store_true'
                                 ,default=False)
                                 
parser.add_argument('-v','--verbose'
                                 ,help='give more update in the process (default is in silent)'
                                 ,action='store_true'
                                 ,default=False)
                        
args = parser.parse_args()


def prompt(message,verbose):
    if verbose:
        print(message)
    pass

def isImageExtension(string):
    if '.png' in string or '.jpeg' in string or'jpg' in string:
        return True
    return False

def imageHexEnd(content):
    #check if the image is from painter or photo editing software
    #why i put two different finding end here because the 
    #hex ending of a painter is different from a common picture 
    #that's why i use two different approach.
    if(content.count(bytes.fromhex(b'\x00IEND\xaeB`\x82'.hex())) > 0):
        offset = content.index(bytes.fromhex(b'\x00IEND\xaeB`\x82'.hex()))
        return offset + 9

    if(content.count(bytes.fromhex('FFD9')) > 0):
        offset = content.index(bytes.fromhex('FFD9'))
        return offset + 2
    return 0

""" 
    check if the image hex end has next hex code
"""
def imageHexEnd_next(content,index):
    try:
        temp = content[index]
        return True
    except:
        return False

def inject(image,executable):
    prompt('-- checking the files --',args.verbose)
    if isImageExtension(image):
        prompt('[/] done checking the files.',args.verbose)
        try:
            prompt('-- opening the files --',args.verbose)
            with open(f'{image}','ab') as fi, open(f'{executable}','rb') as fe:
                prompt('[/] done file existed.',args.verbose)
                prompt('-- attempting to inject --',args.verbose)
                fi.write(fe.read())
                prompt('[/] done injecting.',args.verbose)
            prompt('[/] injecting is complete.',True)
            prompt('[/]process is done--',args.verbose)
            prompt('-- program exiting --',args.verbose)    
        except FileNotFoundError:
            prompt('Error: failed to inject code in a image',args.verbose)
    else:
        prompt('Error: Image is not in a proper file format',args.verbose)

def extract(image,executable):

    prompt('-- checking the files --',args.verbose)
    if isImageExtension(image):
        prompt('[/] finished.',args.verbose)

        try:
            prompt('-- opening the files --',args.verbose)
            with open(f'{image}','rb') as file:

                prompt('[/] Existed.',args.verbose)
                prompt('-- reading and locating the executable code in the image --',args.verbose)
                content = file.read()

                file.seek(imageHexEnd(content))

                prompt('[/] done reading and locating.',args.verbose)
                prompt('-- creating or opening a file for the executable code --',args.verbose)
                with open(f'{executable}','wb') as exe:
                    prompt('[/] done creating or opening a file.',args.verbose)
                    prompt('-- writing the executable code in the file --',args.verbose)
                    exe.write(file.read())
                    prompt('[/] done writing the file.',args.verbose)
                prompt('[/] extracting is complete.',True)
                prompt('[/]process is done--',args.verbose)
                prompt('-- program exiting --',args.verbose)  

        except FileNotFoundError:
            prompt('Error: failed to extract code in a image',True)
    else:
        prompt('Error: Image is not in a proper file format',True)

    
def remove(image):
    prompt('-- checking the files --',args.verbose)
    if isImageExtension(image):
        prompt('[/] finished.',args.verbose)
        try:
            prompt('-- opening the files --',args.verbose)
            with open(f'{image}','rb') as fread:
                prompt('[/] Existed.',args.verbose)
                prompt('-- reading and locating the executable code in the image --',args.verbose)
                content = fread.read()
                if(imageHexEnd(content) == None):
                    prompt('[/] done scanning no injected executable code.',args.verbose)
                    prompt('[*] aborting removing process.',args.verbose)
                else:
                    prompt('-- initiate removing process --',args.verbose)
                    prompt('[*]seperating image hex to executable hex.',args.verbose)
                    newContent = content[0:imageHexEnd(content)]
                    with open(f'{image}','wb') as fwrite:
                        fwrite.write(newContent.strip())
                    prompt('[/] done seperating.',args.verbose)
                prompt('[/] removing is complete.',True)
                prompt('[/]process is done--',args.verbose)
                prompt('-- program exiting --',args.verbose)  

        except FileNotFoundError:
            prompt('Error: failed to extract code in a image',True)
    else:
        prompt('Error: Image is not in a proper file format',True)

def isExist(image):
    prompt('-- checking the files --',args.verbose)
    if isImageExtension(image):
        prompt('[/] finished.',args.verbose)
        try:
            prompt('-- opening the files --',args.verbose)
            with open(f'{image}','rb') as file:
                prompt('[/] Existed.',args.verbose)
                prompt('-- scanning the executable code in the image --',args.verbose)
                content = file.read()
                if not imageHexEnd_next(content,imageHexEnd(content)):
                    prompt('[/] done scanning no injected executable code.',True)
                else:
                    prompt('[/] done scanning executable code is exist in the image.',True)  
                prompt('[/]process is done--',args.verbose)
                prompt('-- program exiting --',args.verbose)            
        except FileNotFoundError:
            prompt('Error: failed to extract code in a image',True)
    else:
        prompt('Error: Image is not in a proper file format',True)

if args.inject:
    prompt('## injecting process ##',args.verbose)
    inject(args.image,args.executable)

if args.extract:
    prompt('## extracting process ##',args.verbose)
    extract(args.image,args.executable)

if args.remove:
    prompt('## removing ##',args.verbose)
    remove(args.image)

if args.isExist:
    prompt('## checking ##',args.verbose)
    isExist(args.image)

