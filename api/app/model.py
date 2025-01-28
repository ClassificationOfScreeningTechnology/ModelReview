import torch
import torch.nn.functional as F
import torch.optim as optim
import pytorch_lightning as pl
import torchmetrics
import torch.nn as nn
from torchvision import models
from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights

class MovieFrame(pl.LightningModule):
    def __init__(self, layer1_size, dropout_rate, lr, num_classes=4):
        super().__init__()
        self.model = models.efficientnet_b0(weights = EfficientNet_B0_Weights.IMAGENET1K_V1) 
        self.backbone = self.model.features
        self.pooling = self.model.avgpool
        self.dropout = nn.Dropout(p=dropout_rate, inplace=True)
        self.fc1 = nn.Linear(1280 , layer1_size)
        self.fc2 = nn.Linear(layer1_size, num_classes)
        self.lr = lr
        self.loss_function = nn.CrossEntropyLoss()

        self.train_acc = torchmetrics.Accuracy(task="multiclass", num_classes=num_classes)
        self.val_acc = torchmetrics.Accuracy(task="multiclass", num_classes=num_classes)
        self.test_acc = torchmetrics.Accuracy(task="multiclass", num_classes=num_classes)

        self.train_macro_f1 = torchmetrics.F1Score(num_classes=num_classes, task="multiclass", average='macro')
        self.val_macro_f1 = torchmetrics.F1Score(num_classes=num_classes, task="multiclass", average='macro')
        self.test_f1 = torchmetrics.F1Score(num_classes=num_classes, task="multiclass", average='macro')
        

        self.train_macro_recall = torchmetrics.Recall(num_classes=num_classes, task="multiclass", average='macro')
        self.val_macro_recall = torchmetrics.Recall(num_classes=num_classes, task="multiclass", average='macro')

        self.train_macro_precision = torchmetrics.Precision(num_classes=num_classes, task="multiclass", average='macro')
        self.val_macro_precision = torchmetrics.Precision(num_classes=num_classes, task="multiclass", average='macro')

        
        for param in self.backbone.parameters():
            param.requires_grad = False

    def forward(self, x):
      self.backbone.eval()
      with torch.no_grad():
          x = self.backbone(x)
          x = self.pooling(x).flatten(1)
      x = self.dropout(x)
      x = F.relu(x)
      x = self.fc1(x)
      x = self.dropout(x)
      x = F.relu(x)
      x = self.fc2(x)

      return x
    

    def configure_optimizers(self):
      optimizer =  optim.Adam(self.parameters(), lr=self.lr)
      return optimizer

    def training_step(self, train_batch, batch_idx):
      inputs, labels = train_batch["pixel_values"], train_batch["label"]


      outputs = self.forward(inputs.float())
      loss = self.loss_function(outputs, labels)


      self.log('train_loss', loss, on_step = True, on_epoch = True)

      outputs = F.softmax(outputs, dim =1)

      self.train_acc(outputs, labels)
      self.log('train_acc', self.train_acc, on_epoch=True, on_step= False)

      self.train_macro_f1(outputs, labels)
      self.log('train_macro_f1', self.train_macro_f1, on_epoch=True, on_step= False)

      self.train_macro_recall(outputs, labels)
      self.log('train_macro_recall', self.train_macro_recall, on_epoch=True, on_step= False)

      self.train_macro_precision(outputs, labels)
      self.log('train_macro_precision', self.train_macro_precision, on_epoch=True, on_step= False)



      return loss

    def validation_step(self, val_batch, batch_idx):
      inputs, labels = val_batch["pixel_values"], val_batch["label"]

      outputs = self.forward(inputs.float())
      loss = self.loss_function(outputs, labels)

      self.log('val_loss', loss,  on_step= True, on_epoch = True, sync_dist=True)

      outputs = F.softmax(outputs, dim =1)

      self.val_acc(outputs, labels)
      self.log('val_acc', self.val_acc, on_epoch=True, on_step= False)

      self.val_macro_f1(outputs, labels)
      self.log('val_macro_f1', self.val_macro_f1, on_epoch=True, on_step= False)

      self.val_macro_recall(outputs, labels)
      self.log('val_macro_recall', self.val_macro_recall, on_epoch=True, on_step= False)

      self.val_macro_precision(outputs, labels)
      self.log('val_macro_precision', self.val_macro_precision, on_epoch=True, on_step= False)

      return loss


    def test_step(self, batch, batch_idx):
        # this is the test loop
        inputs, labels = batch["pixel_values"], batch["label"]
        outputs = self.forward(inputs.float())
        
        loss = self.loss_function(outputs, labels)
        self.log("test_loss", loss)

        self.test_acc(outputs, labels)
        self.log('test_acc', self.test_acc)
        
        self.test_f1(outputs, labels)
        self.log('test_f1', self.test_f1)

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        inputs = batch["pixel_values"]
        logits = self(inputs.float())
        probabilities = F.softmax(logits, dim=1)
        return probabilities