texto = b"Lorem ipsum dolor sit amet, consectetur adipiscing elit. Maecenas luctus sem tortor, et ullamcorper enim auctor vel. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Mauris vel bibendum augue, ut iaculis lectus. Vivamus imperdiet fermentum arcu vel molestie. Praesent a scelerisque mauris. Fusce ut urna aliquam, iaculis nibh elementum, finibus mauris. Phasellus gravida ornare tortor pellentesque pharetra. Mauris vestibulum vestibulum nisl, non lacinia lacus tempus sed. Quisque rhoncus, arcu in malesuada porta, metus sapien maximus augue, non mollis mi purus id leo. Duis felis arcu, euismod sit amet egestas vel, facilisis at massa. Aenean euismod, dui at viverra cursus, odio arcu iaculis lacus, vitae semper metus lorem in justo."

text_size = len(texto)
print(text_size)

fh = open("files/100MB.txt", "wb")
num_bytes = 0
while num_bytes < 100000000:
    fh.write(texto)
    num_bytes += text_size
fh.close()


fh = open("files/250MB.txt", "wb")
num_bytes = 0
while num_bytes < 250000000:
    fh.write(texto)
    num_bytes += text_size
fh.close()
