{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "239c5d4c-7619-4829-8939-bbd5868db4b0",
   "metadata": {},
   "outputs": [],
   "source": [
    "import numpy as np\n",
    "import pandas as pd\n",
    "from sklearn.model_selection import StratifiedKFold\n",
    "from tensorflow.keras.layers import concatenate, Dense, Dropout, Conv2D, MaxPooling2D, Flatten, Input\n",
    "from tensorflow.keras.models import Model, Sequential\n",
    "from tensorflow.keras.applications.efficientnet import EfficientNetB0\n",
    "from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score\n",
    "\n",
    "\n",
    "def create_MLP(dim, regress=False):\n",
    "    model = Sequential()\n",
    "    model.add(Dense(800, input_dim=dim, activation=\"relu\"))\n",
    "    model.add(Dense(256, activation=\"relu\"))\n",
    "    model.add(Dense(128, activation=\"relu\"))\n",
    "    return model\n",
    "\n",
    "n_splits = 10\n",
    "skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=0)\n",
    "\n",
    "epochs_list =  [15]\n",
    "results_list = [] \n",
    "\n",
    "for num_epochs in epochs_list:\n",
    "    accuracy_list = []  \n",
    "    precision_list = [] \n",
    "    recall_list = []  \n",
    "    auc_list = []  \n",
    "    for fold, (train_index, test_index) in enumerate(skf.split(X_tda_np, y_combined.argmax(axis=1))):\n",
    "        X_train_tda, X_test_tda = X_tda_np[train_index], X_tda_np[test_index]\n",
    "        X_train_images, X_test_images = data_array_images[train_index], data_array_images[test_index]\n",
    "        y_train, y_test = y_combined[train_index], y_combined[test_index]\n",
    "\n",
    "        mlp = create_MLP(X_tda_np.shape[1], regress=False)\n",
    "\n",
    "        model_cnn = Sequential([\n",
    "             EfficientNetB0(weights='imagenet', include_top=False, input_shape=(224, 224, 3)),\n",
    "        ])\n",
    "\n",
    "        for layer in model_cnn.layers:\n",
    "            layer.trainable = False\n",
    "        model_cnn.add(Conv2D(64, (3, 3), activation='relu'))\n",
    "        model_cnn.add(MaxPooling2D(2, 2))\n",
    "        model_cnn.add(Flatten())\n",
    "        model_cnn.add(Dense(64, activation='relu'))\n",
    "        combinedInput = concatenate([mlp.output, model_cnn.output])\n",
    "        x = Dense(256, activation=\"relu\")(combinedInput)\n",
    "        x = Dense(128, activation='relu')(x)\n",
    "        x = Dense(128, activation='relu')(x)\n",
    "        x = Dropout(0.2)(x)\n",
    "        x = Dense(n_classes, activation='sigmoid')(x)\n",
    "        model = Model(inputs=[mlp.input, model_cnn.input], outputs=x)\n",
    "        model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy', 'Precision', 'Recall', 'AUC'])\n",
    "\n",
    "        print(f\"Training Fold {fold + 1}/{n_splits} with {num_epochs} epochs...\")\n",
    "        model.fit(x=[X_train_tda, X_train_images], y=y_train,\n",
    "                  validation_data=([X_test_tda, X_test_images], y_test),\n",
    "                  epochs=num_epochs, batch_size=64)\n",
    "\n",
    "        y_pred = model.predict([X_test_tda, X_test_images])\n",
    "        accuracy = accuracy_score(y_test, (y_pred > 0.5).astype(int))\n",
    "        precision = precision_score(y_test, (y_pred > 0.5).astype(int), average='micro')\n",
    "        recall = recall_score(y_test, (y_pred > 0.5).astype(int), average='micro')\n",
    "        auc = roc_auc_score(y_test, y_pred, average='micro')\n",
    "\n",
    "        accuracy_list.append(accuracy)\n",
    "        precision_list.append(precision)\n",
    "        recall_list.append(recall)\n",
    "        auc_list.append(auc)\n",
    "\n",
    "    avg_metrics = {\n",
    "        'Epochs': num_epochs,\n",
    "        'Average Accuracy': np.mean(accuracy_list),\n",
    "        'Average Precision': np.mean(precision_list),\n",
    "        'Average Recall': np.mean(recall_list),\n",
    "        'Average AUC': np.mean(auc_list),\n",
    "    }\n",
    "\n",
    " \n",
    "    results_list.append(avg_metrics)\n",
    "results_df = pd.DataFrame(results_list)\n",
    "print(results_df)\n"
   ]
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.18"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}