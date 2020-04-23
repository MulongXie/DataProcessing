# *** 1 ***
# detect block with image processing
rico_block_subtree / detect_block / main_select_classification.py -> 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-block*'

# *** 2 ***
# remove useless info and only leave bounds, class and children
rico_label_processing / label_simplify.py -> 'E:\\Mulong\\Datasets\\gui\\rico\\combined\\simplified\\'

# *** 3 ***
# remove labels with identical bounds
# filter out trivial classes
rico_label_processing / label_filter.py -> 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-tree\\'

# *** 4 ***
# segment subtrees from rico-tree according to block
rico_block_subtree / segment_subtree / main_segment_tree.py -> 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-subtree\\'

# *** 5 ***
# generate caption for each segment
rico_caption / caption_generator.py -> 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-caption'

# *** 6 ***
# convert caption annotations to coco format
# clip segments (blocks with subtrees)
rico_caption / coco_annotation_generator.py -> 'coco.json'
                                            -> 'E:\\Mulong\\Datasets\\gui\\rico\\subtree\\rico-block-clip'