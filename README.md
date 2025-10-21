# Hidden Code Image Injector <br>

## tools that help inject,extract,and remove executable code </br> in a image using python </br> 

## Usage </br>

template </br>

```python3 img-injector [option] <image-name> <executable code>```

inject the executable code in the image </br>

``` python3 img-injector -i,--inject <image-name> <executable code> ```

extract the executable code in the image </br>

``` python3 img-injector -e,--extract <image-name> <executable code> ```

remove the executable code in the image </br>

``` python3 img-injector -r,--remove <image-name> <executable code> ```

to know if the executable code exit in the image </br>

``` python3 img-injector -x,--isExist <image-name> <executable code> ```

break silent input and be verbose </br>

``` python3 img-injector -v,--verbose <image-name> <executable code> ```

transfer content of executable code to text for better reading </br>

``` python3 img-injector -t,--transferFile <executable code> <text file path> ```

