

def simplify_labels_remap(path : str, query_label : str) -> (str, str):
    """Tensorflow data API transform for combining and simplifying labels
        Arguments
            path : str
                Path to a given image
            query_label : str
                Original un-filtered label for a the image at the path
                specified
    """
    yogurt_map = set('alpro-blueberry-soyghurt',
                      'alpro-vanilla-soyghurt',
                      'arla-mild-vanilla-yoghurt',
                      'arla-natural-mild-low-fat-yoghurt',
                      'arla-natural-yoghurt',
                      'oatly-natural-oatghurt',
                      'valio-vanilla-yoghurt',
                      'yoggi-strawberry-yoghurt',
                      'yoggi-vanilla-yoghurt',
                      'soyghurt',
                      'yoghurt')

    milk_map = set('alpro-fresh-soy-milk',
                   'alpro-shelf-soy-milk',
                   'arla-ecological-medium-fat-milk',
                   'arla-lactose-medium-fat-milk',
                   'arla-medium-fat-milk',
                   'arla-sour-milk',
                   'arla-standard-milk',
                   'garant-ecological-medium-fat-milk',
                   'garant-ecological-standard-milk',
                   'oat-milk',
                   'milk',
                   'oatly-oat-milk',
                   'sour-milk',
                   'soy-milk')

    sour_cream_map = set('arla-ecological-sour-cream',
                        'arla-sour-cream',
                        'sour-cream')

    fruit_juice_map = set('bravo-apple-juice',
                          'bravo-orange-juice',
                          'god-morgon-apple-juice',
                          'god-morgon-orange-juice',
                          'god-morgon-orange-red-grapefruit-juice',
                          'god-morgon-red-grapefruit-juice',
                          'tropicana-apple-juice',
                          'tropicana-juice-smooth',
                          'tropicana-golden-grapefruit',
                          'tropicana-mandarin-morning',
                          'juice')

    apple_map = set('apple',
                    'golden-delicious',
                    'granny-smith',
                    'red-delicious',
                    'royal-gala',
                    'pink-lady')

    melon_map = set('cantaloupe',
                    'galia-melon',
                    'honeydew-melon',
                    'melon',
                    'watermelon')

    pear_map = set('anjou',
                   'kaiser',
                   'pear',
                   'conference')

    pepper_map = set('green-bell-pepper',
                     'orange-bell-pepper',
                     'red-bell-pepper',
                     'yellow-bell-pepper',
                     'pepper')

    tomato_map = set('regular-tomato',
                     'tomato',
                     'vine-tomato',
                     'beef-tomato')

    orange_map = set('nectarine',
                     'orange',
                     'satsumas')

    potato_map = set('floury-potato',
                     'potato',
                     'solid-potato',
                     'sweet-potato')

    onion_map = set('onion',
                    'yellow-onion')

    mushroom_map = set('brown-cap-mushroom',
                       'mushroom')

    mappings = [(yogurt_map, 'yogurt'),
                (milk_map, 'milk'),
                (sour_cream_map, 'sour_cream'),
                (fruit_juice_map, 'fruit_juice'),
                (apple_map, 'apple'),
                (melon_map, 'melon'),
                (pear_map, 'pear'),
                (pepper_map, 'pepper'),
                (tomato_map, 'tomato'),
                (orange_map, 'orange'),
                (potato_map, 'potato'),
                (onion_map, 'onion'),
                (mushroom_map, 'mushroom')]

    for mapping in mappings:
        if query_label in mapping[0]:
            return path, mapping[1]
        else:
            continue
    return path, query_label

