from .set_to_list import clip_set_to_list_on_xaxis, clip_set_to_list_on_yaxis


def clip_set_to_dict_on_xaxis(sets, order):
    dict_images = {}
    for name, set in zip(order, sets):
        image = clip_set_to_list_on_xaxis(set)
        dict_images[name] = image

    return dict_images


def clip_set_to_dict_on_yaxis(sets, order):
    dict_images = {}
    for name, set in zip(order, sets):
        image = clip_set_to_list_on_yaxis(set)
        dict_images[name] = image

    return dict_images
