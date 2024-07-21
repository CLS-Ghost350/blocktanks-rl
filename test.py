import os

from sb3_plus import MultiOutputPPO

model_path = os.path.abspath(os.path.join("Training", "SavedModels", "A"))
model = MultiOutputPPO.load(model_path)
