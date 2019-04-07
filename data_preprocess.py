import csv
import numpy as np

# feature_list = ["Age","workclass","fnlwgt","education","education-num","marital-status","occupation","relationship","race","gender","capital gain","capital loss","hours per week","native-country","income"]


def list_to_dict(list_name):
    out_dict = dict()
    for i, ele in enumerate(list_name):
        out_dict[ele] = i
    return out_dict


def process(filename, normalize=False):
    work_class = ["Private", "Self-emp-not-inc", "Self-emp-inc", "Federal-gov", "Local-gov", "State-gov", "Without-pay",
                  "Never-worked", "?"]

    education = ["Bachelors", "Some-college", "11th", "HS-grad", "Prof-school", "Assoc-acdm", "Assoc-voc", "9th",
                 "7th-8th",
                 "12th", "Masters", "1st-4th", "10th", "Doctorate", "5th-6th", "Preschool", "?"]

    marital_status = ["Married-civ-spouse", "Divorced", "Never-married", "Separated", "Widowed",
                      "Married-spouse-absent",
                      "Married-AF-spouse", "?"]

    occupation = ["Tech-support", "Craft-repair", "Other-service", "Sales", "Exec-managerial", "Prof-specialty",
                  "Handlers-cleaners", "Machine-op-inspct", "Adm-clerical", "Farming-fishing", "Transport-moving",
                  "Priv-house-serv", "Protective-serv", "Armed-Forces", "?"]

    relationship = ["Wife", "Own-child", "Husband", "Not-in-family", "Other-relative", "Unmarried", "?"]

    native_country = ["United-States", "Cambodia", "England", "Puerto-Rico", "Canada", "Germany",
                      "Outlying-US(Guam-USVI-etc)", "India", "Japan", "Greece", "South", "China",
                      "Cuba", "Iran", "Honduras", "Philippines", "Italy", "Poland", "Jamaica", "Vietnam", "Mexico",
                      "Portugal", "Ireland", "France", "Dominican-Republic", "Laos", "Ecuador", "Taiwan", "Haiti",
                      "Columbia", "Hungary", "Guatemala", "Nicaragua", "Scotland", "Thailand", "Yugoslavia",
                      "El-Salvador",
                      "Trinadad&Tobago", "Peru", "Hong", "Holand-Netherlands", "?"]

    feature_list = ["Age", "workclass", "fnlwgt", "education", "education-num", "marital-status", "occupation",
                    "relationship", "race", "gender", "capital gain", "capital loss", "hours per week",
                    "native-country", "income", "?"]

    work_class = list_to_dict(work_class)
    education = list_to_dict(education)
    marital_status = list_to_dict(marital_status)
    occupation = list_to_dict(occupation)
    relationship = list_to_dict(relationship)
    native_country = list_to_dict(native_country)


    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        cnt = 0
        for i, row in enumerate(csv_reader):
            cnt += 1

    print("data num", cnt)
    csv_file.close()

    feature_mat = np.zeros((cnt, 13))
    gender_vec = np.zeros((cnt))
    income_vec = np.zeros((cnt))

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')

        for i, row in enumerate(csv_reader):

            # print(row)
            # feature_vec = np.
            if len(row) > 1 and i>0:
                feature_mat[i, 0] = int(row[0]) * 1.0
                feature_mat[i, 1] = work_class[row[1]] * 1.0
                feature_mat[i, 2] = int(row[2]) * 1.0
                feature_mat[i, 3] = education[row[3]] * 1.0
                feature_mat[i, 4] = int(row[4]) * 1.0
                feature_mat[i, 5] = marital_status[row[5]] * 1.0
                feature_mat[i, 6] = occupation[row[6]] * 1.0
                feature_mat[i, 7] = relationship[row[7]] * 1.0
                feature_mat[i, 8] = int(row[8]) * 1.0  #race

                gender_vec[i] = int(row[9]) * 1.0

                feature_mat[i, 9] = int(row[10]) * 1.0  #cap gain
                feature_mat[i, 10] = int(row[11]) * 1.0  #cap loss
                feature_mat[i, 11] = int(row[12]) * 1.0  #hours per week
                feature_mat[i, 12] = native_country[row[13]] * 1.0

                income_vec[i] = int(row[14]) * 1.0

    print(np.mean(feature_mat, axis=0).shape)
    if normalize:
        feature_mat = (feature_mat - np.mean(feature_mat, axis=0)) / np.std(feature_mat, axis=0)
    return feature_mat, gender_vec, income_vec




if __name__ == '__main__':
    f, g, i = process("train.csv", True)
    print(np.mean(i))
    print(np.mean(g))
    print(np.mean(f[:, 1]), np.std(f[:, 1]))