import torch
import torch.nn as nn
import data_preprocess
import numpy as np

num_epochs = 20
concat = False

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


class NeuralNet(nn.Module):
    def __init__(self, input_size, hidden_size, num_classes):
        super(NeuralNet, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc3 = nn.Linear(hidden_size, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return out


mean, std, feature_mat_train, feature_mat_val, gender_vec_train, gender_vec_val, income_vec_train, income_vec_val = \
    data_preprocess.train_process("train.csv", 0.8, True)


feature_mat_test,  gender_vec_test = data_preprocess.test_process("test_no_income.csv", mean, std, True)

if concat:
    model = NeuralNet(14, 256, 1).to(device)
else:
    print("using no cat")
    model = NeuralNet(13, 512, 1).to(device)

criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=1e-4)

batch_size = 500


if concat:
    feature_mat_train_all = np.concatenate((feature_mat_train, np.expand_dims(gender_vec_train, 1)), axis=1)
    feature_mat_val_all = np.concatenate((feature_mat_val, np.expand_dims(gender_vec_val, 1)), axis=1)
else:
    feature_mat_train_all = feature_mat_train
    feature_mat_val_all = feature_mat_val

for epoch in range(num_epochs):
    cur_order = np.random.permutation(feature_mat_train.shape[0])
    for iter in range(feature_mat_train.shape[0]//batch_size):
        ibatch_start = iter * batch_size
        ibatch_end = (iter + 1) * batch_size

        project_ind_batch = cur_order[ibatch_start:ibatch_end]

        feature_mat_train_batch = feature_mat_train_all[project_ind_batch]
        income_vec_train_batch = income_vec_train[project_ind_batch]

        in_fea = torch.from_numpy(feature_mat_train_batch).float().to(device)
        targets = torch.from_numpy(income_vec_train_batch).float().to(device)

        outputs = model(in_fea)
        loss = criterion(outputs, targets.resize(targets.size(0), 1))

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        # print("loss = ", loss.item())
    # test

    val_fea = torch.from_numpy(feature_mat_val_all).float().to(device)
    pred_income = model(val_fea).cpu().data.numpy()[:, 0]


    gen1_pred = np.asarray((pred_income > 0.5), dtype=np.float32)
    gen1_correct = (gen1_pred == income_vec_val) * gender_vec_val
    # print("gen1_pred", gen1_pred.shape, income_vec_val.shape, gender_vec_val.shape)

    # print("gen1_correct", gen1_correct, gen1_correct.shape)
    gen1_correct_num = np.sum(gen1_correct)

    gen0_pred = np.asarray((pred_income > 0.5), dtype=np.float32)
    gen0_correct = (gen0_pred == income_vec_val) * (1 - gender_vec_val)
    gen0_correct_num = np.sum(gen0_correct)

    total = gender_vec_val.shape[0]
    num1 = np.sum(gender_vec_val)
    num0 = total - num1

    pred_income_binary = np.asarray((pred_income > 0.5), dtype=np.float32)
    cor_num = np.sum((pred_income_binary == income_vec_val))

    print("accuracy of A= {} \n accuracy of B= {} \n overall accuracy = {}".format(gen1_correct_num / num1,
                                                                                   gen0_correct_num / num0,
                                                                                   cor_num / total))



