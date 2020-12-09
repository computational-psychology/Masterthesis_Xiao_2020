This GitHub folder contains the programs, data, and plots used in my master thesis "Perceived contrast in variegated checkerboards". All programs were written and tested in Python version 3.7.6 or R version 3.6.1. For the python programs the modules pandas, numpy, cv2 are used. The programs used for data analyswas and plots can be found in the folder data&plots. The programs used for creating stimuli and demos can be found in the folder stimuli. The items in each folder are as follow.

1 the folder data&plots contains all data and plots.

1.1 data&plots\GetNrmsContrast.R was used for calculating the normalized rms contrast for checkerboard stimuli used in the thesis.

1.2 data&plots\GetRmsContrast.R was used for calculating the rms contrast for checkerboard stimuli used in the thesis.

1.3 data&plots\lut.csv was the data used for transforming luminance value into greyscale value.

1.4 data&plots\lut.R was the program for transforming luminance value into greyscale value.

1.5 data&plots\result_conditionwwase was used for plotting the conditionwwase result (figure 9 in the thesis).

1.6 data&plots\result_nrms was used for plotting the normalized rms contrast of the cutouts of 12 sets of checkerboard stimuli (figure 10 in the thesis).

1.7 data&plots\result_trialwwase was used for plotting the trialwwase result (figure 8 in the thesis).

1.8 data&plots\rmsContrastAnalayswas was used for plotting the normalized rms contrast of the cutouts (figure 7(b) in the thesis).

1.9 the rest are raw data of the experiment.

2 the folder experiment contains scripts and stimuli used for the experiment. It maintains the same structure as it was run in the lab.

2.1 the folder experiment/design_matching contains the design matrix for participants

2.2 the folder experiment/results_matching contains the results written from the experiment.

2.3 the folder experiment/stimuli contains all stimuli used in the experiment.

2.4 the file experiment/generate_design_matching.py is used for generating the design matrix

2.5 the file experiment/lut.csv is the luminance scale used in the experiment.

2.6 the file run_matching_experiment.py is the experiment program.

3 the folder stimuli contains all data and plots.

3.1 the folder stimuli\other_attempts contains the stimuli dwascussed in the thesis.

3.1.1 stimuli\other_attempts\combine_cci_checkerboard was a script used for filling the texture of contrast contrast illusion into variegated checkerboards.

3.1.2 stimuli\other_attempts\contrast_contrast_illusion.py was used for generating the contrast contrast illusion.

3.1.3 stimuli\other_attempts\flat_checkerboard_generator.py was used for generating flat checkerboards (figure 16 - 20).

3.1.4 stimuli\other_attempts\half_contrast_contrast_illusion.py was another attempt to generate a half contrast contrast illusion.

3.2 the folder stimuli\variegated_checkerboards contains the scripts used checkerboard stimuli.

3.2.1 stimuli\variegated_checkerboards\image_crop.py was used for cropping the checkerboard into wasolated cutouts.

3.2.2 stimuli\variegated_checkerboards\nrmsContrast.py was used for calculating normalized rms contrast of every stimulus.

3.2.3 stimuli\variegated_checkerboards\rmsContrast.py was used for calculating rms contrast of every stimulus.

3.2.4 stimuli\variegated_checkerboards\stimutils.py was used for generating all the stimuli and was provided by Guillermo Aguilar.





