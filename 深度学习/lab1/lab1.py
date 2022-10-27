import numpy as np
import math
import random
import torch
from datetime import datetime
import time
from sklearn.model_selection import train_test_split

datasize = 100000
PI = math.pi
learning_rate = 0.0001
epochs = 2000
def func(x):
  return math.sin(x) + math.pow(math.e, -x)
class MLP(torch.nn.Module):
  def __init__(self):
    super().__init__()
    self.layer1=torch.nn.Linear(1,128)
    self.layer2=torch.nn.Linear(128,128)
    self.layer3=torch.nn.Linear(128,128)
    self.layer4=torch.nn.Linear(128,128)
    self.layer5=torch.nn.Linear(128,128)
    self.layer_final=torch.nn.Linear(128,1)

  def forward(self,x):
    x=self.layer1(x)
    x=torch.nn.functional.relu(x)
    x=self.layer2(x)
    x=torch.nn.functional.relu(x)
    x=self.layer3(x)
    x=torch.nn.functional.relu(x)
    x=self.layer4(x)
    x=torch.nn.functional.relu(x)
    x=self.layer5(x)
    x=torch.nn.functional.relu(x)
    x=self.layer_final(x)
    return x

if __name__ == '__main__':
  mlp = MLP()
  datax = []
  datay = []
  datax = np.random.uniform(0,4 * PI,datasize)
  datay = np.array(list(map(func, datax)))
  train_X, tmp_X, train_Y, tmp_Y = train_test_split(datax, datay, test_size=0.4, random_state=1)
  valid_X, test_X, valid_Y, test_Y = train_test_split(tmp_X, tmp_Y, test_size=0.5, random_state=1)
  
  train_X = torch.tensor(train_X).reshape(-1,1)
  train_Y = torch.tensor(train_Y).reshape(-1,1)
  
  valid_X = torch.tensor(valid_X).reshape(-1,1)
  valid_Y = torch.tensor(valid_Y).reshape(-1,1)
  
  test_X = torch.tensor(test_X).reshape(-1,1)
  test_Y = torch.tensor(test_Y).reshape(-1,1)
  optimizer = torch.optim.Adam(mlp.parameters(), lr=learning_rate)
  mlploss = []
  start = time.time()
  
  for epoch in range(epochs):
    preds=mlp(train_X.float())
    loss=torch.nn.functional.mse_loss(preds,train_Y.float())
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    mlploss.append(loss.item())
    print("epoch:" + str(epoch) + ",loss:" + str(float('%.5f' %(loss.item()))))  

  end = time.time()
  print("time:" + str(end - start) +"ms")
  valid_loss=torch.nn.functional.mse_loss(preds,train_Y.float())
  preds_valid = mlp(valid_X.float())
  loss_valid = torch.nn.functional.mse_loss(preds_valid,valid_Y.float())
  print("valid_loss:" + str(float('%.5f' %(loss_valid.item()))))
  preds_test = mlp(test_X.float())
  np.savetxt('loss_layer'+str("FINAL")+'.txt',mlploss)
  loss_test = torch.nn.functional.mse_loss(preds_test,test_Y.float())
  print("test_loss:" + str(float('%.5f' %(loss_test.item()))))