## Instructions:

### REDO:
To run the explicit controller.
```py
python redo.py
```

### To train reinforcement controller:
```py
python train.py
```

### To demo reinforcement controller:
```py
python demo.py
```

## Description:
The explicit controller code is in `redo.py`, which uses a PID controller to keep the pole upright.

The reinforcement controller code is in `agent.py` while the modified variable parameters are found in `cartpoleEnv.py`. `cartpole-model.pth` is the last generated model. The agent is a QNN (Q-table neural network) reinforcement learner. The environment comes courtesy of [Open AI's Gym Program](https://github.com/openai/gym). 