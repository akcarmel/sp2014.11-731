#Calculating training features
echo 'Now calculating Training features'
python calculate_features.py -b100 experimental_data/dev.100best -s experimental_data/dev.src -o train.features
#Calculating training features
echo 'Now calculating test features'
python calculate_features.py -b100 experimental_data/test.100best -s experimental_data/test.src -o test.features
#Sampling and Prediction
echo 'Now sampling and prediction'
python sampling.py -tra train.features -tst test.features -mf meteor.out.final 
sudo ./score-meteor < output.log.txt >> 'log.unclean.score'
sudo ./score-meteor < output.lin.txt >> 'lin.unclean.score'
#sudo ./score-meteor < output.log.txt.clean >> 'log.clean.score'
#sudo ./score-meteor < output.lin.txt.clean >> 'lin.clean.score'
tail -n 2 *score
