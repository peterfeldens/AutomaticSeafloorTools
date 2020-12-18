#removes all psaces from filenames in current folder
for f in *; do mv "$f" `echo $f | tr ' ' '_'`; done