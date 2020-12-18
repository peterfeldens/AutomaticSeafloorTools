find . -name "*.png" -exec convert "{}" -alpha off "{}" \;


# in numpy 
img = img[:,:,:3]  # remove aslpha channel
