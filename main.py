import csv
import statistics
import thresholding

# Splitting dataset according to classes
red_zone = []
yellow_zone = []
green_zone = []
data = []


# Splitting into training and testing data
def data_split(data, training):
    training_data = []
    testing_data = []

    length = 0

    for row in data:
        if length < training:
            training_data.append(row)
        else:
            testing_data.append(row)
        length += 1

    return training_data, testing_data


# Reading csv database
with open('Dataset/data.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        data.append(row)
        if row[4] == '0':
            green_zone.append(row)
        elif row[4] == '1':
            yellow_zone.append(row)
        else:
            red_zone.append(row)
    print('Dataset segregated')


print(len(green_zone))
print(len(yellow_zone))
print(len(red_zone))

# Carrying out splitting
green_training, green_testing = data_split(green_zone, 400)
yellow_training, yellow_testing = data_split(yellow_zone, 400)
red_training, red_testing = data_split(red_zone, 400)


# Calculating mean and standard deviation of the data
def calculate_threshold_data(data):
    gx = []
    gy = []
    gz = []
    gnet = []

    for i in range(0, len(data)):
        gx.append(float(data[i][0]))
        gy.append(float(data[i][1]))
        gz.append(float(data[i][2]))
        gnet.append(float(data[i][3]))

    m1 = statistics.mean(gx)
    m2 = statistics.mean(gy)
    m3 = statistics.mean(gz)
    m4 = statistics.mean(gnet)
    m5 = statistics.pstdev(gx, mu=m1)
    m6 = statistics.pstdev(gy, mu=m2)
    m7 = statistics.pstdev(gz, mu=m3)
    m8 = statistics.pstdev(gnet, mu=m4)

    return m1, m2, m3, m4, m5, m6, m7, m8


# Calculating parameters
gxm, gym, gzm, gnm, gxd, gyd, gzd, gnd = calculate_threshold_data(green_training)
yxm, yym, yzm, ynm, yxd, yyd, yzd, ynd = calculate_threshold_data(yellow_training)
rxm, rym, rzm, rnm, rxd, ryd, rzd, rnd = calculate_threshold_data(red_training)

# Printing parameters
print("\nRed Zone: \n")
print('{0} {1} {2} {3}'.format(rxm, rym, rzm, rnm))
print('{0} {1} {2} {3}'.format(rxd, ryd, rzd, rnd))

print("\nYellow Zone: \n")
print('{0} {1} {2} {3}'.format(yxm, yym, yzm, ynm))
print('{0} {1} {2} {3}'.format(yxd, yyd, yzd, ynd))

print("\nGreen Zone: \n")
print('{0} {1} {2} {3}'.format(gxm, gym, gzm, gnm))
print('{0} {1} {2} {3}'.format(gxd, gyd, gzd, gnd))

# Calculation of threshold
Tx1 = (gxm + yxm)/2
Tx2 = (yxm + rxm)/2

Ty1 = (gym + yym)/2
Ty2 = (yym + rym)/2

Tz1 = (gzm + yzm)/2
Tz2 = (yzm + rzm)/2

Tn1 = (gnm + ynm)/2
Tn2 = (ynm + rnm)/2

# Printing thresholds
print("\nFor X:\n")
print("T1 = {0} & T2 = {1}".format(Tx1, Tx2))
print("=====================================")

print("\nFor Y:\n")
print("T1 = {0} & T2 = {1}".format(Ty1, Ty2))
print("=====================================")

print("\nFor Z:\n")
print("T1 = {0} & T2 = {1}".format(Tz1, Tz2))
print("=====================================")

print("\nFor Net:\n")
print("T1 = {0} & T2 = {1}".format(Tn1, Tn2))
print("=====================================")

# Final Testing
print("Starting Training and Testing\n")

accuracy, b, c, d = thresholding.apply_thresholding(data, Tx1, Tx2, Ty1, Ty2, Tz1, Tz2, Tn1, Tn2)
red_accuracy, r1, r2, r3 = thresholding.apply_thresholding(red_zone, Tx1, Tx2, Ty1, Ty2, Tz1, Tz2, Tn1, Tn2)
yellow_accuracy, y1, y2, y3 = thresholding.apply_thresholding(yellow_zone, Tx1, Tx2, Ty1, Ty2, Tz1, Tz2, Tn1, Tn2)
green_accuracy, g1, g2, g3 = thresholding.apply_thresholding(green_zone, Tx1, Tx2, Ty1, Ty2, Tz1, Tz2, Tn1, Tn2)

print("Accuracy obtained = {0}\n".format(accuracy))

print("\n==========For Green Zone=============\n")
print("Overall Accuracy obtained = {0}\n".format(green_accuracy))
print("Green = {0}".format(g1))
print("Yellow = {0}".format(g2))
print("Red = {0}".format(g3))

print("\n==========For Yellow Zone=============\n")
print("Overall Accuracy obtained = {0}\n".format(yellow_accuracy))
print("Green = {0}".format(y1))
print("Yellow = {0}".format(y2))
print("Red = {0}".format(y3))

print("\n==========For Red Zone=============\n")
print("Overall Accuracy obtained = {0}\n".format(red_accuracy))
print("Green = {0}".format(r1))
print("Yellow = {0}".format(r2))
print("Red = {0}".format(r3))