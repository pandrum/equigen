import splitfolders

splitfolders.ratio("equigen_album_images", output="split", seed=1337, ratio=(
    0.7, 0.15, 0.15), group_prefix=None, move=False)
