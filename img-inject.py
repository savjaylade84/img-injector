"""
    Author: John Jayson B. De Leon
    Github: savjaylade84
    Email:savjaylade84@gmail.com

    tools for injecting executable code in the image
    using python.

    usage: img-inject [option] <image-name> <code file>
"""

import argparse
import time


parser = argparse.ArgumentParser(
description='''python tools for injecting,extracting,and removing executable code in the image.''',
formatter_class=argparse.RawDescriptionHelpFormatter,epilog=''' 
Author: John Jayson B. De Leon 
Email: savjaylade84@gmail.com 
Github: savjaylade84 
    ''',prog='python3 img-inject.py',usage='%(prog)s [options] <image> <executable-code>')

parser.add_argument("image",help="image name")
parser.add_argument("executable",help="executable code")
parser.add_argument('text',help="text file")

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

parser.add_argument('-t','--transferFile',
                                 help='transfer hex from executable file to text file'
                                 ,action='store_true'
                                 ,default=False)
                        
args = parser.parse_args()



''' 
    this will only prompt if verbose argument is on 

'''
def prompt(message,status,verbose):
    space:str = 200 * ' '
    if verbose:
        if status == 'progress':
            print(f'\r[In Progress] => {message}{space}',end='\r')
        if status == 'process':
            print(f'\r[Progress Status] => {message}{space}',end='\r')
        if status == 'progress-check':
            print(f'\r[Progress Done] => {message}{space}',end='\r')
        if status == 'progress-failed' or status == 'progress-cross':
            print(f'\r[Progress Failed] => {message}{space}',end='\r')
        if status == 'error':
            print(f'\r[Program Error] => {message}{space}',end='\r')
        if status == 'header':
            print(f'[***] {message} [***]')
        time.sleep(3)
    pass

''' validate if the file is immage  '''
def isImageExtension(string):
    for extension in ['.png','.jped','.jpg']:
        if extension in string:
            return True
    return False

    '''
        check if the image is from painter or photo editing software
        why i put two different finding end here because the
        hex ending of a painter is different from a common picture
        that's why i use two different approach.
    '''
def imageHexEnd(content):

    ''' for a image hex format that are save in microsoft paint '''
    if(content.count(bytes.fromhex(b'\x00IEND\xaeB`\x82'.hex())) > 0):
        offset = content.index(bytes.fromhex(b'\x00IEND\xaeB`\x82'.hex()))
        return offset + 9

    ''' for default image hex format '''
    if(content.count(bytes.fromhex('FFD9')) > 0):
        offset = content.index(bytes.fromhex('FFD9'))
        return offset + 2
    return 0

''' check if the image hex end has next hex code '''
def imageHexEnd_next(content,index):
    try:
        temp = content[index]
        return True
    except:
        return False

''' Inject hex content of executable to the end of image hex '''
def inject(image,executable):
    prompt('checking the files','progress',args.verbose)
    if isImageExtension(image):
        prompt('done checking the files','progress-check',args.verbose)
        try:
            prompt('opening the files','progress',args.verbose)
            with open(f'{image}','ab') as fi, open(f'{executable}','rb') as fe:
                prompt('done file existed.','progress-check',args.verbose)
                prompt('attempting to inject','progress',args.verbose)
                fi.write(fe.read())
                prompt('done injecting.','progress-check',args.verbose)
            prompt('injecting is complete.','process',True)
            prompt('process is done','process',args.verbose)
            prompt('program exiting','process',args.verbose)    
        except FileNotFoundError:
            prompt('failed to inject code in a image','error',True)
    else:
        prompt('Image is not in a proper file format','error',True)

''' extract the excutable code in the image '''
def extract(image,executable):

    prompt('checking the files','progress',args.verbose)
    if isImageExtension(image):
        prompt('finished.','progress-check',args.verbose)

        try:
            prompt('opening the files','progress',args.verbose)
            with open(f'{image}','rb') as file:

                prompt('File Existed.','process',args.verbose)
                prompt('reading and locating the executable code in the image','progress',args.verbose)
                content = file.read()

                file.seek(imageHexEnd(content))

                prompt('done reading and locating.','progress-check',args.verbose)
                prompt('creating or opening a file for the executable code','progress',args.verbose)
                with open(f'{executable}','wb') as exe:
                    prompt('done creating or opening a file.','progress-check',args.verbose)
                    prompt('writing the executable code in the file','progress',args.verbose)
                    exe.write(file.read())
                    prompt('done writing the file.','progress-check',args.verbose)
                prompt('extracting is complete.','process',True)
                prompt('process is done','process',True)
                prompt('-- program exiting --',True)  

        except FileNotFoundError:
            prompt('failed to extract code in a image','error',True)
    else:
        prompt('Image is not in a proper file format','error',True)


''' remove the executable code in the image hex content '''    
def remove(image):
    prompt('checking the files','progress',args.verbose)
    if isImageExtension(image):
        prompt('finished.','progress-check',args.verbose)
        try:
            prompt('opening the files','progress',args.verbose)
            with open(f'{image}','rb') as fread:
                prompt('Existed.','progress-check',args.verbose)
                prompt('reading and locating the executable code in the image','progress',args.verbose)
                content = fread.read()
                if(imageHexEnd(content) == None):
                    prompt('done scanning no injected executable code.','progress-check',args.verbose)
                    prompt('aborting removing process.','progress-cross',args.verbose)
                else:
                    prompt('initiate removing process','progress',args.verbose)
                    prompt('seperating image hex to executable hex.','process',args.verbose)
                    newContent = content[0:imageHexEnd(content)]
                    with open(f'{image}','wb') as fwrite:
                        fwrite.write(newContent.strip())
                    prompt('done seperating.','progress-check',args.verbose)
                prompt('removing is complete.','progress-check',True)
                prompt('process is done','progress-check',True)
                prompt('program exiting','process',True)  

        except FileNotFoundError:
            prompt('Error: failed to extract code in a image',True)
    else:
        prompt('Error: Image is not in a proper file format',True)

''' 
    this will check if the executable code already exist in the image 
'''
def isExist(image):
    prompt('checking the files','progress',args.verbose)
    if isImageExtension(image):
        prompt('finished.','progress-check',args.verbose)
        try:
            prompt('opening the files','progress',args.verbose)
            with open(f'{image}','rb') as file:
                prompt('Existed.','progress-check',args.verbose)
                prompt('scanning the executable code in the image','progress',args.verbose)
                content = fileile.read()
                if not imageHexEnd_next(content,imageHexEnd(content)):
                    prompt('done scanning no injected executable code.','progress-check',True)
                else:
                    prompt('done scanning executable code is exist in the image.','progress-check',True)  
                prompt('process is done','progress-check',True)
                prompt('program exiting','process',True)            
        except FileNotFoundError:
            prompt('failed to extract code in a image','error',True)
    else:
        prompt('Image is not in a proper file format','error',True)

def transfer_hex_file(file,text):
    prompt('Starting transfering information of executable to text','progress',args.verbose)
    with open(f'{file}','rb') as file:
        prompt('opening executable file','progress',args.verbose)
        with open(f'{text}','w') as text:
            prompt('done opening executable file','progress-check',args.verbose)
            prompt('opening text files','progress',args.verbose)
            prompt('opening text files','progress-check',args.verbose)
            prompt('transfering','progress',args.verbose)
            text.write(str(file.read()))
            prompt('done transfering','progress-check',True)
            prompt('program exiting','process',True)   


if(args.image and args.executable):
    if args.inject:
        prompt('injecting process','header',args.verbose)
        inject(args.image,args.executable)

    if args.extract:
        prompt('extracting process','header',args.verbose)
        extract(args.image,args.executable)

elif(args.image):
    if args.remove:
        prompt('removing','header',args.verbose)
        remove(args.image)

    if args.isExist:
        prompt('checking','header',args.verbose)
        isExist(args.image)
elif(args.executable and args.text):
    if args.transferFile:
        prompt('transfering','header',args.verbose)
        transfer_hex_file(args.executable,args.text)


