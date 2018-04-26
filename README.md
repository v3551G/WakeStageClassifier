### Wake Stage Classifier using Logistic Regression from EEG

Watch the presentation here: 
<a href="http://www.youtube.com/watch?feature=player_embedded&v=uUgaKNPIZF8&t
" target="_blank"><img src="http://img.youtube.com/vi/uUgaKNPIZF8&t/0.jpg" 
width="240" height="180" border="10" /></a>

Get SHHS dataset from [NSRR website](https://sleepdata.org/datasets/shhs)

Important: Do not change the directories, folder names, file names!!

Dependancies needed:
	1. Python 2.7
	2. Spark 2.3.0
	3. MNE 0.15.2
		* Follow installation [here](https://www.martinos.org/mne/stable/install_mne_python.html)
	4. Scikit-learn 0.18.1

Follow these tasks in order:

	1. Ground truths extraction:
			Run below command in Terminal
			```
			spark-submit extract_ground_truths.py full-path-to/shhs/polysomnography/annotations-events-nsrr/shhs1
			```

	2. Feature extraction:
			Run below command in Terminal
			```
			spark-submit extract_features.py full-path-to/shhs/polysomnography/edfs/shhs1/
			```

	3. Create model:
			Run below command in Terminal
			```
			python create_model.py
			```

Check "log.txt" if there is any error. If there is, it might just be an inconsistent data and it was ignored.
Models will be found in "models/"
Final best model will be found in "models/KF45_TunedSVM_4000.sav"
Metrics can be found in "scores_KF45_TunedSVM.txt"

Try this!
Prototype App:
	Run below command in Terminal
	```
	python app/app.py
	```

	Few notes about the app:
		* It is simply loading one of the test set as a test run, instead of recording your EEG, because such tools is not available.
		* To make the alarm ring, input from = '0700', until = '0800'
		* To not make the alarm ring, input from = '0730', until = '0830'
