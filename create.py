from io import BytesIO
import requests
from PIL import Image
from functools import reduce
import stopwatch
import concurrent.futures
from colorthief import ColorThief
import colors as clr

# generate auth token at https://developer.spotify.com/console/get-current-user-top-artists-and-tracks/
auth_token = 'BQAr-IPHhPI8KivSc0f48e8NGxHhz4tyazNzRvs5uriNEtfZqWnwqgeJHFKoOOiUZqPqlLqTxHBIBUh9D9kfGw3Xcc0__F9CotnrM5cv76F4DYtrRqHpapNxIPdD9QUmS193JU9qPnYBf3cZeIpCmCKkeBmLkWxcdKgMLFkqIib7YoM8L3SYTjOCizfZSRTJkq-YzMyIkS2c'

timer = stopwatch.Stopwatch()

def makeCollage(item_type, limit, offset, time_range):
    print(time_range)

    req_url = 'https://api.spotify.com/v1/me/top/' + \
        item_type + '?' + 'limit=' + \
        str(limit) + '&offset=' + str(offset) + '&time_range=' + time_range

    response = requests.get(url=req_url, headers={
        "Authorization": "Bearer " + auth_token, "Content-Type": "application/json"}).json()

    count = 1
    imgSize = 10000
    imageLinks = {}
    for i in response['items']:  # cycle through items

        # print info
        if (item_type == 'tracks'):
            info = i['name'] + ' - '
            albumInfo = i['album']['name'] + "-" + \
                i['album']['artists'][0]['name']
            numArtists = len(i['artists'])
            for j in range(0, numArtists):
                info += i['artists'][j]['name']
                if (j != numArtists - 1):
                    info += ', '
        else:
            info = i['name']
            albumInfo = info

        if (item_type == 'tracks'):  # artist or tracks
            pics = i['album']['images']
        else:
            pics = i['images']

        lastImg = pics[1]  # last pic is smallest pixels

        if (lastImg['width'] < imgSize):  # maintain accurate size
            imgSize = lastImg['width']

        imageLinks.update({albumInfo: lastImg['url']})
        info += '\n' + lastImg['url']

        print(str(count) + '. ' + info)  # track info
        print("ALBUM: " + albumInfo + "\n")

        count += 1

    print("API call done...")

    images = []
    with concurrent.futures.ThreadPoolExecutor(32) as executor:
        for i in imageLinks.values():
            executor.submit(downloadImg, i, images, imgSize)

    print("image downloads done... " + str(len(images)) + " images")

    colors = []
    fileConvertTime = 0
    dominantColorFindTime = 0
    for image in images:
        with BytesIO() as file_object:
            timer.start()
            image.save(file_object, "PNG")
            timer.stop()
            fileConvertTime += timer.time()

            timer.start()
            cf = ColorThief(file_object)
            color = cf.get_palette(color_count=4, quality=1)
            colors.append(color)
            timer.stop()
            dominantColorFindTime += timer.time()

    print("dominant colors found... avg file save time: " + str(fileConvertTime / len(images))
          + "  avg color finding time: " + str(dominantColorFindTime / len(images)))

    
    constructCollage(images, imgSize)
    constructColoredCollage(images, colors, imgSize)


def sortColors(images: list, colors: list):
    colorSortings = {}
    for i in range(len(colors)):
        color = clr.dom_color(colors[i])
        list = colorSortings.get(color)
        if list == None:
            colorSortings.update({color: []})
        colorSortings.get(color).append(images[i])
    return colorSortings


def constructCollage(images: list, imgSize: int):
    dimensions = getDim(len(images))
    print("dimensions: " + str(dimensions))
    cols = dimensions[0]
    rows = dimensions[1]
    print("img size: " + str(imgSize))

    collage = Image.new(mode="RGB", size=(imgSize * cols, imgSize * rows))

    imgIndex = 0
    for r in range(0, rows):
        for c in range(0, cols):
            if (imgIndex >= len(images)):
                break
            collage.paste(images[imgIndex], (imgSize * c, imgSize * r))
            imgIndex += 1

    collage.show()


def constructColoredCollage(images: list, colors: list, imgSize: int):
    sorted = sortColors(images, colors)
    dim = 7
    collage = Image.new(mode="RGB", size=(imgSize * dim, imgSize * dim))
    r = 0
    for color in clr.MAIN_COLORS:
        currImages = []
        dark = sorted.get("dark " + color)
        if dark != None:
            for darkImg in dark:
                currImages.append(darkImg)

        light = sorted.get("light " + color)
        if light != None:
            for lightImg in light:
                currImages.append(lightImg)

        c = 0
        for image in currImages:
            collage.paste(image, (imgSize * c, imgSize * r))
            c += 1
        r += 1

    collage.show()


def downloadImg(imgLink, images: list, imgSize: int):
    image = Image.open(requests.get(
        imgLink, stream=True).raw).resize([imgSize, imgSize])
    images.append(image)


def factorTuples(n):
    # get all factors
    factors = sorted(reduce(list.__add__,
                            ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))
    tuples = []
    # create tuples of all factors
    for i in range(0, int(len(factors) / 2)):
        tuple = [factors[i], factors[len(factors) - 1 - i]]
        tuples.append(tuple)
    return tuples


def getDim(num):
    MAX_DIFF = 4  # maintain squareness
    smallest = [0, 0]
    while (smallest[0] == 0):
        factors = factorTuples(num)
        smallestDiff = factors[len(factors) - 1]
        diff = smallestDiff[1] - smallestDiff[0]
        if (diff <= MAX_DIFF):
            smallest[0] = smallestDiff[0]
            smallest[1] = smallestDiff[1]
        num -= 1
    return smallest


def main():
    length = ''
    while(length != 's' and length != 'm' and length != 'l'):
        length = input('Would you like a short (1 month), medium (6 months), or long (all time) term collage? Enter s, m, or, l: ')
        if(length != 's' and length != 'm' and length != 'l'):
            print('INVALID!')
    
    if(length == 's'):
        term = 'short_term'
    if(length == 'm'):
        term = 'medium_term'
    if(length == 'l'):
        term = 'long_term'

    makeCollage('tracks', 100, 0, term)
    input('press enter to end')
    

if __name__ == '__main__':
    main()

# makeCollage('artists', 100, 0, 'long_term')
# makeCollage('artists', 100, 0, 'medium_term')
# makeCollage('artists', 100, 0, 'short_term')


