# Automatic liquid water isotope calibration tool : ALWIC-tool
![alt text](link_image_here)
A python workflow integrated with a user interface to process liquid injections of water stable istopes. Usually the processing i.e. memory correction and calibration is done by hand with a non-negligeable probability of human mistakes. We try to adress this issue with a limited number of inputs made by hand. This tool provide also a large number of graphs to improve the visualisation of the dataset at each step of the processing. 

The idea behind this code is to make it accessible for everyone, from the undergraduate student to the recognized scientist including the high-level programmer. It can used "as is" but can also be customized to the infinite due to it's architecture in module. 

# Getting started
## Download ALWIC-tool
In order to download ALWIC you can click [here](https://github.com/baptistebordet1/ALWIC-tool/archive/refs/heads/main.zip). This will download a zip file with all the modules. 
If you are familiar with github you can clone the project with the following link : link_git_clone_here. 

## Install ALWIC-tool
### Using annaconda 

The first recommendation is to create a new environment to avoid any conflicts of the installed packages with your previous configuration. In Anaconda a new environment is created in the Annaconda prompt with the following command : 

```
 conda create -n your_environment_name
```
   
Then the environment is activated with the command :

```
  activate your_environment_name
```

To install necessary packages for the programm open a prompt window and navigate into the directory where you downloaded the programm. Then run the following command :

```
  conda env update -n your_environment_name -f requirements.yaml
```

After this you can open the file called GUI\_main.py in Spyder and run it. The [documentation](link_to_doc) contains more information on how to run ALWIC.

### With another Python distribution

You will need to install the packages included in the requirements.txt file. This file is included in the file you downloaded. The method to install it is yours, depending on your IDE but the command to install all the required packages is :
```
pip install requirements.txt
```
Then you can run the GUI\_main.py file and start processing. The [documentation](link_to_doc) contains more information on how to use ALWIC.

## Licence 
ALWIC-tool is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

ALWIC-tool is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License is available [here](https://github.com/baptistebordet1/ALWIC-tool/blob/main/LICENSE). If you can not see it, see <https://www.gnu.org/licenses/>.

## Credits 

Thanks to Hans Christian Steen Larsen who initiated the project; Daniele Zannoni for all the support during the development of this tool; Arny Sveinbjörnsdottir for the comments made from a user perspective. 
Thanks to Melanie Behrens and Manfred Gröning for the help in the implementation of one of the method. 
Thanks to the teams at AWI, EPFL and LSCE who tested the code, your feedbacks were precious. 
Finally a special thanks to Pauline Gayrin and Clara Berneuil for the emotional support a well as usefull discussion. 

## Contribution Guidelines 

Contributions to the code are encouraged. 

You can do it either by opening an issue to notify problems in the code (https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) or a pull request if you want to fix or add features (https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) 

## Citation 
If you use this programm in your worl, please use the following BibTeX entry.
```
@misc{ALWIC_tool_2023,
  author =       {Baptiste Bordet, Hans-Christian Steen Larsen, Daniele Zannoni, Arny Sveinbjörnsdottir},
  title =        {{Automatic liquid water isotope calibration tool (ALWIC-tool)}},
  howpublished = {\url{link_git_hub}},
  year =         {2023}
}
```
