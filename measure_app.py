import numpy as np
from analytic_geometry import line_circle_intersection, line_intersection, tangents
import cv2
from math import sqrt, acos


def main(img_path):
    # Ucitavanje originalne slike/Loading orignal photo
    img = cv2.imread(img_path)
    # Prikaz originalne slike/ Plotting orignal photo
    # cv2.imshow('Original', img)
    # cv2.waitKey(0)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #Zamucenje/ blur
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 0)
    # Prikaz zamucenih fotografija/ Plotting blured pictures
    # cv2.imshow('Zamucena slika', img_blur)
    # cv2.waitKey(0)

    # Sobelov filtar za isticanje ivice, Sobel's filter for efflux edges
    sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5)
    sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5)
    sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5)
    # Prikaz Sobelvih transformacija/ Plotting Sobel's transformation
    #cv2.imshow('Sobel X', sobelx)
    # cv2.waitKey(0)
    #cv2.imshow('Sobel Y', sobely)
    # cv2.waitKey(0)
    #cv2.imshow('Sobel X Y using Sobel() function', sobelxy)
    # cv2.waitKey(0)

    # Canny detektuje ivice/Canny detects edges
    edges = cv2.Canny(image=img_blur, threshold1=100,
                      threshold2=200)
    # cv2.imshow('Canny Edge Detection', edges)
    # cv2.waitKey(0)

    # Hofova transformacija za detekciju linija/Hough transformation for line detection
    lines = cv2.HoughLinesP(edges, rho=1, theta=1 * np.pi / 180,
                            threshold=100, minLineLength=100, maxLineGap=50)
    x1 = 0
    x2 = img.shape[1]

    # Crtanje i prikaz linije/ Drawing and plotting the line
    for x1_, y1, x2_, y2 in lines[0]:
        cv2.line(img, (x1, y1), (x2, y2), (25, 205, 208), 1)
    # cv2.imshow('houghlines5.jpg', img)
    # cv2.waitKey(0)

    # Hofova transformacija za detekciju kruznice/ Haugh Transformation for circle deteciton
    rows = img_gray.shape[0]
    circles = cv2.HoughCircles(img_gray, cv2.HOUGH_GRADIENT, 1, rows,
                               param1=100, param2=30,
                               minRadius=30, maxRadius=500)
    x0 = circles[0][0][0]
    y0 = circles[0][0][1]
    r0 = circles[0][0][2]
    y1 = lines[0][0][1]
    y2 = lines[0][0][3]

    p = (x0, y0, r0)
    lsp = (x1, y1)
    lep = (x2, y2)

    # Crtanje i prikaz kruznice/ Drawing and plotting circle

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for i in circles[0, :]:
            center = (i[0], i[1])
            # centar kruga
            cv2.circle(img, center, 1, (60, 7, 104), 2)
            # poluprecnik kruga
            radius = i[2]
            cv2.circle(img, center, radius, (60, 7, 104), 2)
    # cv2.imshow("detected circles", img)
    # cv2.waitKey(0)
    # Trazenje preseka ravni i kruznice/ Findnig intersection points
    inp = line_circle_intersection(p, lsp, lep)
    x0_int = int(inp[0][0])
    y0_int = int(inp[0][1])

    # Prikazivanje tacaka preseka ravni i kruznice/ Plotting intersection points
    cv2.circle(img, (x0_int, y0_int), radius=1,
               color=(104, 7, 15), thickness=7)
    x1_int = int(inp[1][0])
    y1_int = int(inp[1][1])
    cv2.circle(img, (x1_int, y1_int), radius=1,
               color=(104, 7, 15), thickness=7)
    # cv2.imshow("Tacke preseka", img)
    # cv2.waitKey(0)

    # Trazenje tangenti/ Findnig Tangents
    p1, p2, p3, p4, p5, p6, m_ab, c, c1 = tangents(
        y0, y0_int, x0, x0_int, x1_int, y1_int, x2)

    m_cd = (y0 - y1_int) / (x0 - x1_int)
    m_ab = -1 / m_cd
    c = - m_ab * x1_int + y1_int

    cv2.line(img, p1, p2, (40, 131, 132), 1)
    cv2.line(img, p1, p3, (40, 131, 132), 1)
    cv2.line(img, p4, p5, (40, 131, 132), 1)
    cv2.line(img, p4, p6, (40, 131, 132), 1)

    # cv2.imshow("Tangenta", img)
    # cv2.waitKey(0)

    # Trazenje  preseka tangenti/ Finging intersection of tangents
    x1_li = int(line_intersection((p1, p2), (p4, p5))[0])
    y1_li = int(line_intersection((p1, p2), (p4, p5))[1])
    cv2.circle(img, (x1_li, y1_li), radius=1, color=(104, 7, 15), thickness=7)

    # Racunaje ugla/ Angle calculation
    hipotenuse = sqrt((x1_li - x1_int) ** 2 + (y1_li - y1_int) ** 2)
    catete = abs(x1_int - x0_int) / 2
    angle = acos(catete / hipotenuse)

    # Svodjenje ugla na prvi kvadrant/ Convert angle to first quardrant
    if m_ab > 0:
        deg_angle = angle * 180 / 3.1415926
    else:
        deg_angle = 180 - angle * 180 / 3.1415926

    cv2.ellipse(img, (x1_int, y1_int), (50, 50), 0, 180,
                deg_angle + float(180), (255, 0, 0), 2)
    cv2.ellipse(img, (x0_int, y0_int), (50, 50),
                0, 0, -deg_angle, (255, 0, 0), 2)
    cv2.putText(img, str(deg_angle)[:7], (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    #cv2.imwrite(save_path, img)
    #cv2.imshow("Image", img)
    # cv2.waitKey(0)

    return str(deg_angle), img
