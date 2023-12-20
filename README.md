# Community Automatic liquid water isotope calibration tool : CALWIC
![alt text](https://github.com/baptistebordet1/CALWIC/blob/main/image_read_me.jpg)
A python workflow integrated with a user interface to process liquid injections of water stable isotopes. Usually the processing i.e. memory correction and calibration is done by hand with a non-negligeable probability of human mistakes. We try to adress this issue with a limited number of inputs made by hand. This tool provides also a large number of graphs to improve the visualisation of the dataset at each step of the processing. 

The idea behind this code is to make it accessible for everyone, from the undergraduate student to the recognized scientist including the high-level programmer. It can used "as is" but can also be customized to the infinite due to it's architecture in module. 

# Getting started
## Download CALWIC
In order to download ALWIC you can click [here](https://github.com/baptistebordet1/CALWIC/archive/refs/heads/main.zip). This will download a zip file with all the modules. 
If you are familiar with github you can clone the project with the following link : https://github.com/baptistebordet1/CALWIC. 

## Install CALWIC
### Using Anaconda 

The first recommendation is to create a new environment to avoid any conflicts of the installed packages with your previous configuration.
Open an Anaconda prompt. Use the following command to go to the unzipped folder of CALWIC : 

```
cd path_to_the_folder
```

To create the new environment use the command below : 

```
 conda env create -f requirements.yml
```

Note : This command might take a few minutes to run since all the packages required for CALWIC will be downloaded and installed. 

This will create an environment called ALWIC_env which can be activated with the command :

```
 conda activate ALWIC_env
```

The environment has to be activated each time you want to run CALWIC. It can also be done in Anaconda Navigator by choosing it instead of base on top left of the window. After this you can open the file called GUI\_main.py in Spyder and run it. The [documentation](https://github.com/baptistebordet1/CALWIC/raw/main/project/files/user_documentation.pdf) contains more information on how to run ALWIC.

### With another Python distribution

You will need to install the packages included in the requirements.txt file. This file is included in the file you downloaded. The method to install it is yours, depending on your IDE but the command to install all the required packages is :

```
pip install requirements.txt
```

Then you can run the GUI\_main.py file and start processing. The [documentation](https://github.com/baptistebordet1/CALWIC/raw/main/project/files/user_documentation.pdf) contains more information on how to use ALWIC.

## Licence 
CALWIC is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.

CALWIC is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License is available [here](https://github.com/baptistebordet1/CALWIC/blob/main/LICENSE). If you can not see it, see <https://www.gnu.org/licenses/>.

## Credits 

Thanks to Hans Christian Steen Larsen who initiated the project; Daniele Zannoni for all the support during the development of this tool; Arny Sveinbjörnsdottir for the comments made from a user perspective. 
Thanks to Manfred Gröning for the help provided in the implementation of his method.
Thanks to Melanie Behrens for providing files for the tests.
Finally a special thanks to Pauline Gayrin and Clara Berneuil for the emotional support as well as usefull discussion. 

## Contribution Guidelines 

Contributions to the code are encouraged especially adding new method for memory correction. 

You can do it either by opening an issue to notify problems in the code (https://docs.github.com/en/issues/tracking-your-work-with-issues/creating-an-issue) or a pull request if you want to fix or add features (https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request) 

## Citation 
If you use this programm in your worl, please use the following BibTeX entry.
```
@misc{ALWIC_tool_2023,
  author =       {Baptiste Bordet, Hans-Christian Steen Larsen, Daniele Zannoni, Arny Sveinbjörnsdottir},
  title =        {{Automatic liquid water isotope calibration tool (CALWIC)}},
  howpublished = {\url{https://github.com/baptistebordet1/CALWIC}},
  year =         {2023}
}
```
