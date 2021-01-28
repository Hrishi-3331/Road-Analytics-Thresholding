def apply_thresholding(data, Tx1, Tx2, Ty1, Ty2, Tz1, Tz2, Tn1, Tn2):
    attempt = 0
    correct = 0
    red = 0
    yellow = 0
    green = 0

    mx1 = Tx1/2
    mx2 = (Tx1 + Tx2)/2
    mx3 = Tx2 + (Tx1/2)

    my1 = Ty1 / 2
    my2 = (Ty1 + Ty2) / 2
    my3 = Ty2 + (Ty1 / 2)

    mz1 = Tz1 / 2
    mz2 = (Tz1 + Tz2) / 2
    mz3 = Tz2 + (Tz1 / 2)

    mn1 = Tn1 / 2
    mn2 = (Tn1 + Tn2) / 2
    mn3 = Tn2 + (Tn1 / 2)

    m = [[mx1, mx2, mx3], [my1, my2, my3], [mz1, mz2, mz3], [mn1, mn2, mn3]]

    for row in data:
        x = float(row[0])
        y = float(row[1])
        z = float(row[2])
        net = float(row[3])
        res = int(row[4])

        pred = [0, 0, 0]
        pred[threshold(x, Tx1, Tx2)] += 1
        pred[threshold(y, Ty1, Ty2)] += 1
        pred[threshold(z, Tz1, Tz2)] += 1
        pred[threshold(net, Tn1, Tn2)] += 1

        if pred[0] > pred[1] and pred[0] > pred[2]:
            prediction = 0
        elif pred[1] > pred[0] and pred[1] > pred[2]:
            prediction = 1
        elif pred[2] > pred[0] and pred[2] > pred[1]:
            prediction = 2
        else:
            i = 0
            poss = []
            while i < 3:
                if pred[i] == 2:
                    poss.append(i)
                i += 1
            prediction = get_deviation(row, m, poss)

        if prediction == res:
            correct += 1
            print("==============Iteration {0} -> Correct Prediction".format(attempt+1))
        else:
            print("==============Iteration {0} -> Incorrect Prediction".format(attempt + 1))
        attempt += 1

        if prediction == 0:
            green += 1
        elif prediction == 1:
            yellow += 1
        elif prediction == 2:
            red += 1

    return float((correct/attempt)*100), float((green/attempt)*100), float((yellow/attempt)*100), float((red/attempt)*100)


def get_deviation(row, m, poss):
    poss1 = poss[0]
    poss2 = poss[1]

    d1 = (abs(m[0][poss1] - float(row[0])) + abs(m[1][poss1] - float(row[1])) + abs(m[2][poss1] - float(row[2])) + abs(m[3][poss1] - float(row[3])))/4
    d2 = (abs(m[0][poss2] - float(row[0])) + abs(m[1][poss2] - float(row[1])) + abs(m[2][poss2] - float(row[2])) + abs(m[3][poss2] - float(row[3])))/4

    if d1 <= d2:
        return poss1
    else:
        return poss2


def threshold(x, T1, T2):
    if x <= T1:
        return 0
    elif T1 < x <= T2:
        return 1
    else:
        return 2
