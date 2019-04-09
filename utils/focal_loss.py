import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable


class FocalLoss(nn.Module):

    def __init__(self, alpha=0.75, gamma=2, size_average=True):
        super(FocalLoss, self).__init__()

        self.alpha = alpha
        self.gamma = gamma
        self.size_average = size_average

    def forward(self, inputs, targets):
        inputs = inputs.view(-1)
        targets = targets.view(-1)

        # obj_count = int(sum((targets > 0.5).int()))
        # noobj_count = int(sum((targets < 0.5).int()))
        count = targets.size(0)
        m = nn.Sigmoid()
        inputs_s = m(inputs)

        # 可以选择正样本或负样本不使用focal loss
        # BCELoss = -((targets * torch.log(inputs_s) + (1 - targets) * torch.log(1 - inputs_s))).mean()
        # BCELoss_obj = -(targets * torch.log(inputs_s)).sum()
        # BCELoss_noobj = -((1 - targets) * torch.log(1 - inputs_s)).sum()
        # print(" BCELoss:{}\n BCELoss_obj:{}\n BCELoss_noobj:{}\n".format(BCELoss, BCELoss_obj, BCELoss_noobj))

        # FocalLoss = -(torch.pow(1 - inputs_s, self.gamma) * (targets * torch.log(inputs_s) + torch.pow(inputs_s, self.gamma) * (1 - targets) * torch.log(1 - inputs_s))).mean()
        FocalLoss_obj = -self.alpha * (torch.pow(1 - inputs_s, self.gamma) * targets * torch.log(inputs_s)).sum()
        FocalLoss_noobj = -(1 - self.alpha) * (torch.pow(inputs_s, self.gamma) * (1 - targets) * torch.log(1 - inputs_s)).sum()
        # print(" FocalLoss:{}\n FocalLoss_obj:{}\n FocalLoss_noobj:{}\n".format(FocalLoss, FocalLoss_obj, FocalLoss_noobj))

        loss_sum = FocalLoss_obj + FocalLoss_noobj
        loss_mean = (1 / count) * FocalLoss_obj + (1 / count) * FocalLoss_noobj
        #         loss_sum = BCELoss_obj + BCELoss_noobj
        #         loss_mean = (1 / count) * BCELoss_obj + (1 / count) * BCELoss_noobj
        #         print(loss_sum,loss_mean)

        if self.size_average:
            loss = loss_mean
        else:
            loss = loss_sum
        return loss