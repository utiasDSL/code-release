# code-release

This repository contains all the data and plotting scripts required to reproduce the plots in our paper ["What is the Impact of Releasing Code with Publications? Statistics from the Machine Learning, Robotics, and Control Communities"](https://ieeexplore.ieee.org/document/10621946). The preprint is available [here]((https://arxiv.org/abs/2308.10008)).

## Installation

Install/upgrade Python3 dependencies:

```sh
pip3 install --upgrade pip
pip3 install pyyaml
pip3 install tikzplotlib
pip3 install matplotlib --upgrade
```

This was tested on macOS 13.3 with the following:

```sh
anaconda                  2022.10  
matplotlib                3.7.1
pip                       23.0.1
python                    3.9.13 
pyyaml                    6.0
tikzplotlib               0.10.1
```

## Use

Clone this repository and run its `main.py` script:

```sh
git clone https://github.com/utiasDSL/code-release.git
cd code-release/
python3 main.py
```

## Output

The script will sequentially generate the following figures:

![fig1](./readme-figures/Figure_1.png)
![fig2](./readme-figures/Figure_2.png)

![fig3](./readme-figures/Figure_3.png)
![fig4](./readme-figures/Figure_4.png)

![fig5](./readme-figures/Figure_5.png)
![fig6](./readme-figures/Figure_6.png)

![fig7](./readme-figures/Figure_7.png)

## Contribution

Our determination of available open-source code for publications is not perfect. If we incorrectly associated your publication with or without code, please open a pull request with the correction. We appreciate your contributions! 

## Citation

Please cite our work [(paper)](https://ieeexplore.ieee.org/document/10621946) or [(preprint)](https://arxiv.org/abs/2308.10008) as:

```bibtex
@ARTICLE{oscrelease2024,
      author={Zhou, Siqi and Brunke, Lukas and Tao, Allen and Hall, Adam W. and Bejarano, Federico Pizarro and Panerati, Jacopo and Schoellig, Angela P.},
      journal={IEEE Control Systems Magazine}, 
      title={What Is the Impact of Releasing Code With Publications? Statistics from the Machine Learning, Robotics, and Control Communities}, 
      year={2024},
      volume={44},
      number={4},
      pages={38-46},
      doi={10.1109/MCS.2024.3402888}
}
```

-----
>  [Learning Systems and Robotics Lab](https://www.learnsyslab.org/) at the Technical University of Munich (TUM) and the University of Toronto
