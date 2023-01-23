import webcolors

COLORS = ["dark red", "light red", "dark orange", "light orange", "dark yellow",
          "dark green", "light green", "dark blue", "light blue", "dark purple", "light purple",
          "dark black", "light black", "dark white", "light white", "brown"]

MAIN_COLORS = ["red", "orange", "yellow",
               "green", "blue", "purple"]

colorMappings = {"aliceblue": "light white",
                 "antiquewhite": "dark white",
                 "cyan": "light blue",
                 "aquamarine": "light green",
                 "azure": "light white",
                 "beige": "dark white",
                 "bisque": "dark white",
                 "black": "dark black",
                 "blanchedalmond": "dark white",
                 "blue": "dark blue",
                 "blueviolet": "dark purple",
                 "brown": "dark red",
                 "burlywood": "brown",
                 "cadetblue": "dark blue",
                 "chartreuse": "light green",
                 "chocolate": "dark orange",
                 "coral": "dark orange",
                 "cornflowerblue": "light blue",
                 "cornsilk": "dark white",
                 "crimson": "dark red",
                 "darkblue": "dark blue",
                 "darkcyan": "dark blue",
                 "darkgoldenrod": "dark yellow",
                 "darkgray": "light black",
                 "darkgreen": "dark green",
                 "darkkhaki": "dark yellow",
                 "darkmagenta": "dark purple",
                 "darkolivegreen": "dark green",
                 "darkorange": "dark orange",
                 "darkorchid": "light purple",
                 "darkred": "dark red",
                 "darksalmon": "light orange",
                 "darkseagreen": "light green",
                 "darkslateblue": "dark blue",
                 "darkslategray": "dark black",
                 "darkturquoise": "light blue",
                 "darkviolet": "light purple",
                 "deeppink": "light red",
                 "deepskyblue": "light blue",
                 "dimgray": "light black",
                 "dodgerblue": "light blue",
                 "firebrick": "dark red",
                 "floralwhite": "light white",
                 "forestgreen": "dark green",
                 "magenta": "light purple",
                 "gainsboro": "light white",
                 "ghostwhite": "light white",
                 "gold": "dark yellow",
                 "goldenrod": "dark yellow",
                 "gray": "light black",
                 "green": "dark green",
                 "greenyellow": "light green",
                 "honeydew": "light white",
                 "hotpink": "light red",
                 "indianred": "light red",
                 "indigo": "dark purple",
                 "ivory": "light white",
                 "khaki": "light yellow",
                 "lavender": "light purple",
                 "lavenderblush": "light white",
                 "lawngreen": "light green",
                 "lemonchiffon": "light yellow",
                 "lightblue": "light blue",
                 "lightcoral": "light red",
                 "lightcyan": "light blue",
                 "lightgoldenrodyellow": "light yellow",
                 "lightgray": "dark white",
                 "lightgreen": "light green",
                 "lightpink": "light red",
                 "lightsalmon": "light orange",
                 "lightseagreen": "dark blue",
                 "lightskyblue": "light blue",
                 "lightslategray": "light black",
                 "lightsteelblue": "light blue",
                 "lightyellow": "dark white",
                 "lime": "light green",
                 "limegreen": "dark green",
                 "linen": "light white",
                 "maroon": "dark red",
                 "mediumaquamarine": "light green",
                 "mediumblue": "dark blue",
                 "mediumorchid": "light purple",
                 "mediumpurple": "light purple",
                 "mediumseagreen": "light green",
                 "mediumslateblue": "dark purple",
                 "mediumspringgreen": "light green",
                 "mediumturquoise": "light blue",
                 "mediumvioletred": "dark red",
                 "midnightblue": "dark blue",
                 "mintcream": "light white",
                 "mistyrose": "dark white",
                 "moccasin": "dark white",
                 "navajowhite": "dark white",
                 "navy": "dark blue",
                 "oldlace": "light white",
                 "olive": "dark green",
                 "olivedrab": "dark green",
                 "orange": "light orange",
                 "orangered": "dark orange",
                 "orchid": "light purple",
                 "palegoldenrod": "light yellow",
                 "palegreen": "light green",
                 "paleturquoise": "light blue",
                 "palevioletred": "light red",
                 "papayawhip": "dark white",
                 "peachpuff": "dark white",
                 "peru": "dark yellow",
                 "pink": "light red",
                 "plum": "light purple",
                 "powderblue": "light blue",
                 "purple": "dark purple",
                 "red": "dark red",
                 "rosybrown": "brown",
                 "royalblue": "dark blue",
                 "saddlebrown": "brown",
                 "salmon": "light orange",
                 "sandybrown": "light orange",
                 "seagreen": "dark green",
                 "seashell": "light white",
                 "sienna": "brown",
                 "silver": "dark white",
                 "skyblue": "light blue",
                 "slateblue": "dark purple",
                 "slategray": "light black",
                 "snow": "light white",
                 "springgreen": "light green",
                 "steelblue": "dark blue",
                 "tan": "brown",
                 "teal": "dark blue",
                 "thistle": "light purple",
                 "tomato": "light red",
                 "turquoise": "light blue",
                 "violet": "light purple",
                 "wheat": "brown",
                 "white": "light white",
                 "whitesmoke": "light white",
                 "yellow": "dark yellow",
                 "yellowgreen": "light green"}


def nearest_color(rgb: tuple):
    try:
        name = webcolors.rgb_to_name(rgb)
    except ValueError:
        diffs = {}
        for color_hex, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
            r, g, b = webcolors.hex_to_rgb(color_hex)
            diffs[sum([(r - rgb[0]) ** 2, (g - rgb[1]) **
                  2, (b - rgb[2]) ** 2])] = color_name
        name = diffs[min(diffs.keys())]
    return colorMappings.get(name)


def dom_color(rgbs: list):
    colors = []
    for rgb in rgbs:
        colors.append(nearest_color(rgb))
    for color in colors:
        if ((color != "dark black") & (color != "light black") & (color != "dark white") & (color != "light white")):
            return color
    return colors[0]


def nearest_color_orig(rgb: tuple):
    try:
        name = webcolors.rgb_to_name(rgb)
    except ValueError:
        diffs = {}
        for color_hex, color_name in webcolors.CSS3_HEX_TO_NAMES.items():
            r, g, b = webcolors.hex_to_rgb(color_hex)
            diffs[sum([(r - rgb[0]) ** 2, (g - rgb[1]) **
                  2, (b - rgb[2]) ** 2])] = color_name
        name = diffs[min(diffs.keys())]
    return name
