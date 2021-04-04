from io import StringIO, BytesIO

import cv2
import csv
import numpy as np
from PIL import Image
from django.core.files.base import ContentFile

from formDecryptor.models import Form
from mainApp.models import CSVFile

from openpyxl import Workbook

bukvi = ["Д","Г","В","Б","А"]
radW = 15
radH = 10
stolb = 2
klass = 11
otvet = []
otvetb = []
final_answer = []

def get_main_color(img):
    colors = img.getcolors(256)
    max_occurence, most_present = 0, 0
    try:
        for c in colors:
            if c[0] >  max_occurence:
                (max_occurence, most_present) = c
        return most_present
    except TypeError:
        raise Exception("Too many colors in the image")

def main_work(W, H,stolb, nachalo, img, sto, mini, maxi):
    vhod = W * stolb
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)

    thresh = cv2.threshold( gray, 30, 255, cv2.THRESH_BINARY)[1]

    contours = cv2.findContours(thresh, cv2.RETR_TREE,  cv2.CHAIN_APPROX_SIMPLE )
    contours = contours[0] if len(contours) == 2 else contours[1]

    result = img.copy()

    X = []
    Y = []

    min_area = mini
    max_area = maxi

    for c in contours:

        area = cv2.contourArea(c)
        if area > min_area and area < max_area:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(result, [box], -1, (255, 0, 0), 1)

    s = 0
    for g in box:
        X.append(tuple(box[s])[0])
        Y.append(tuple(box[s])[1])
        s = s + 1

    y = min(Y)
    x = min(X)
    w = max(X) - min(X)
    h = max(Y) - min(Y)

    crop_img = img[y:y+h, x:x+w]
    graYP = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
    graYP = cv2.bitwise_not(graYP)
    thresh2 = cv2.threshold( graYP, 30, 255, cv2.THRESH_BINARY)[1]

    contours = cv2.findContours(thresh2, cv2.RETR_TREE,  cv2.CHAIN_APPROX_SIMPLE )
    contours = contours[0] if len(contours) == 2 else contours[1]

    min_area1 = 80
    max_area1 = 140 

    n = 0
    s = 0
    first = 0
    old = 0
    oldY = 0
    
    XP = []
    YP = []
    
    for c in range(nachalo,W):
        XP.append([])
    for c in range(H):
        YP.append([])
    
    for c in contours:
        area = cv2.contourArea(c)
        if area > min_area1 and area < max_area1:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            X1 = []
            Y1 = []
            for l in range(4):
                X1.append(list(box[l])[0])
                Y1.append(list(box[l])[1])


            XO = max(X1) - min(X1)
            YO = max(Y1) - min(Y1)
            if (old - 5 > (box[0])[0] or old + 5 < (box[0])[0]) or (oldY - 5 > (box[0])[1] or oldY + 5 < (box[0])[1]):
                if ((XO - 5 < YO  and  XO + 5 > YO ) or (XO > YO - 5  and  XO < YO + 5)):
                    if s == 0 and sto == 0:
                        first = round((max(Y1) + min(Y1))/2)
                    if s == W:
                        s = 0
                        n += 1
                    for l in range(round(((max(Y1) + min(Y1))/2)) - 3, round(((max(Y1) + min(Y1))/2)) + 3):
                            if l == first or sto == 1:
                                if s > W - nachalo - 1  and  sto == 0:
                                    XP[W - nachalo - 1].append(round((max(X1) + min(X1))/2))
                                else:
                                    XP[s].append(round((max(X1) + min(X1))/2))
                                YP[n * sto].append(round((max(Y1) + min(Y1))/2))
                                break
                    s += 1

            old = (box[0])[0]
            oldY = (box[0])[1]
    XP = sorted(XP, key = None, reverse = True)
    

    X2 = []
    Y2 = []
    
    for c in range(W - nachalo):
        XP[c] = sorted(XP[c])
    for c in range(H):
        YP[c] = sorted(YP[c])


    for c in XP:
        kolv = 0
        bold = 0
        vse = {}

        for b in c:
            if bold != b:
                kolv = 0
            kolv += 1
            vse[b] = kolv
            bold = b

        bold = 0
        n = max(vse.values())
        for b in c:
            if bold != b:
                if vse[b] == n:
                    if b > bold + 5:
                        X2.append(b)

            if vse[b] == n:
                bold = b 

    for c in YP:
        kolv = 0
        bold = 0
        vse = {}

        for b in c:
            if bold != b:
                kolv = 0
            kolv += 1
            vse[b] = kolv
            bold = b

        bold = 0
        n = max(vse.values())
        for b in c:
            if bold != b:
                if vse[b] == n:
                    if b > bold + 5:
                        Y2.append(b)

            if vse[b] == n:
                bold = b 
    
    X2 = sorted(set(X2), key = None, reverse = True)
    Y2 = sorted(set(Y2), key = None, reverse = True)
    Aold = 0
    if sto == 0:
        for A in X2:
            if Aold < A + 5:
                X2.remove(A)
            Aold = A

    n = 0
    s = 1
    kolv = 0
    old = 0
    oldY = 0
   
    for c in contours:

        area = cv2.contourArea(c)
        if area > min_area1 and area < max_area1:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            cv2.drawContours(crop_img, [box], -1, (255, 0, 0), 1)
            X1 = []
            Y1 = []
            for l in range(4):
                X1.append(tuple(box[l])[0])
                Y1.append(tuple(box[l])[1])


            XO = max(X1) - min(X1)
            YO = max(Y1) - min(Y1)
            if (old - 5 > (box[0])[0] or old + 5 < (box[0])[0]) or  (oldY - 5 > (box[0])[1] or oldY + 5 < (box[0])[1]):
                if ((XO - 6 < YO  and  XO + 6 > YO ) or (XO > YO - 6  and  XO < YO + 6)):
                    cv2.drawContours(crop_img, [box], -1, (255, 0, 0), 1)

                    y = min(Y1) + 1
                    x = min(X1) + 1
                    w = max(X1) - min(X1) - 2
                    h = max(Y1) - min(Y1) - 2   

                    cube = thresh2[y:y+h, x:x+w]
                    V = get_main_color(Image.fromarray(np.uint8(cube)))

                    kolv += 1
                    n += 1
                    if n > W*(H/2):
                        s += 1
                        n = 0

                    if V != 0:
                        rub = 0
                        for g in X2:
                            if ((max(X1) + min(X1))/2) + 10 > g:
                                break
                            rub += 1
            
                        rubs = 0
                        if sto == 1:
                            for g in Y2:
                                if ((max(Y1) + min(Y1))/2) + 10 > g:
                                    break

                                rubs = rubs + 1
                                if rubs >= (H / stolb):
                                    rubs = 0
                        
                        if sto == 1:
                            otvet.append(str((round(((vhod)/s) - (rub)))) + bukvi[rubs] )

                        if sto == 0:
                            for l in range(round(((max(Y1) + min(Y1))/2)) - 4, round(((max(Y1) + min(Y1))/2)) + 4):
                                if l == Y2[0]:
                                    otvet.append(str(round((vhod - rub - 1))) + " klass")
                                    break

                        cv2.circle(crop_img, (((c[0])[0])[0], ((c[0])[0])[1]), 5, (0, 0, 255), -1)
            old = (box[0])[0]
            oldY = (box[0])[1]

    return kolv

def create_csv(*args, **kwargs):
    a = 0
    csvfile = BytesIO()

    wb = Workbook()
    wr = wb.active

    with open('./media/documents/cartridge_accounting.xlsx'):
        while a < kwargs['count']:
            otvet.clear()
            pk = int(kwargs['file_list'][str(a)])
            img = cv2.imread(Form.objects.get(pk=pk).get_full_url())

            main_work(radW, radH, 2, 0, img, 1, 75000, 100000)
            main_work(11, 1, 1, 1, img, 0, 50000, 80000)

            wr.append(otvet)
            a += 1

        wb.save(csvfile)
        file = ContentFile(csvfile.getvalue())

        final_csv = CSVFile(user=kwargs['user'])
        try:
            final_csv.save()
            final_csv.file.save('cartridge_accounting.xlsx', file)
        except:
            return

        return final_csv.pk