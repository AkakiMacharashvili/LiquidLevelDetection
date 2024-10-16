
import numpy
import cv2

def find(img):
    #to determine every pixels number
    pixels = [[[0 for k in range(256)] for j in range(256)] for i in range(256)]
    arr = numpy.array(img)
    a = 0
    b = 0
    c = 0
    h = len(arr)
    w = len(arr[0])

    for i in range(h):
        for j in range(w):
            lst = list(arr[i][j])
            pixels[lst[0]][lst[1]][lst[2]] += 1

    vessel = 0
    #glass volume
    for i in range(h):
        cur = 1
        lst = []
        while cur < w - 1:
            if list(arr[i][0]) != list(arr[i][cur]):
                lst.append(cur)
            cur += 1

        if len(lst) > 1:
            vessel += lst[len(lst) - 1] - lst[0]
    liquid = w * h
    #determination of total liquid level
    for i in range(255, 230, -1):
        for j in range(255, 230, -1):
            for k in range(255, 230, -1):
                liquid -= pixels[i][j][k]


    lst = []
    lst.append(vessel)
    lst.append(liquid)
    #each liquid in pixels
    for i in range(1, 255):
        for j in range(1, 255):
            for k in range(1, 255):
                if k > 150:
                    c += pixels[i][j][k]
                elif k > 50:
                    b += pixels[i][j][k]
                else:
                    a += pixels[i][j][k]

    return [vessel, liquid, a, b, c]




file1 = input('please enter video adress: ')
capture = cv2.VideoCapture(file1)

num = 0
file2 = input('please enter file adrees to store images from video: ')
#converting video into images
while (True):

    success, frame = capture.read()

    if success:
        cv2.imwrite(f'{file2}/frame_{num}.jpg', frame)
    else:
        break

    num = num + 1


#output
V = 0
for i in range(num):
    image = cv2.imread(f'{file2}/frame_{i}.jpg')
    temp = find(image)
    if i == 0:
        V = temp[0]
    print(f'------>{i}')
    k = int((int((temp[1] / V) * 100) - 3) * 100 / 93)
    if k >= 100:
        print('full')
    elif k <= 0:
        print('empty')
    else:
        print('total: ' + str(k) + '%')
    x = int((temp[3] / V))
    y = int((temp[4] / V))
    z = int((temp[2] / V))
    if k > 0:
        if x + y + z <= 1:
            print('tea: ' + str(int((temp[3] / V) * 100)) + '%')
            print('coffee: ' + str(int((temp[2] / V) * 100)) + '%')
            if (temp[1] - temp[3] - temp[4]) > 0:
                print('water: ' + str(int((((temp[1] - temp[3] - temp[2])) / V) * 100)) + '%')
            else:
                print('water: ' + str(0) + '%')
        elif x + y <= 1:
            print('tea: ' + str(int((temp[3] / V) * 100)) + '%')
            print('water: ' + str(int((temp[4] / V) * 100)) + '%')
            print('coffee: ' + str(int(1 - x - y) * 100) + '%')

        elif x <= 1:
            print('tea: ' + str(int((temp[3] / V) * 100)) + '%')
            print('water: ' + str(int(1 - x) * 100) + '%')
            print('coffee: ' + str(0) + '%')

        else:
            print('tea: ' + str(int(100)) + '%')
            print('water: ' + str(0) + '%')
            print('coffee: ' + str(0) + '%')
    else:
        print('tea: ' + str(0) + '%')
        print('water: ' + str(0) + '%')
        print('coffee: ' + str(0) + '%')
