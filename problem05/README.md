# Problem 5

## Part A

This entire part is found in Report.pdf

## Part B

This entire part is also found in Report.pdf

## Part C

This part uses the following programs that you need installed:
  * Cartpole environment from OpenAI Gym
  * pytorch to power the neural network
  * seaborn to help render graphs
  * numpy to aid in calculations

If you don't already have those installed, you can do so by running the command:

```
pip install numpy gym[classic_control] torch seaborn 
```

You may need to install gym proper to have videos recorded:

```
pip install gym
```

After the required packages are installed, you can run the code for this part with:

```
python3 c.py
```

If there is no [videos](videos/) directory, one will be created after running this program, containing
the video of the last runthrough of the cartpole game.

## Part D

This part requires mujoco to be installed on your system, which can be a bit of a process. A full
description to help get it installed can be found [here](https://github.com/openai/mujoco-py).

This part also requires all of the packages required for Part C, so be sure to have all those installed
as well.

After everything is installed and working properly, this part's code can be run with:

```
python3 d.py
```

You can find videos output by this program in the [cheetah_vids](cheetah_vids/) directory
