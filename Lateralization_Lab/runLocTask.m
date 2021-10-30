function runLocTask(subjectID)
%subjectID is a string identifying the test subject. E.g. 'JD' for Jane Doe
repetitions= 1;
numConditions= 5; % Number of conditions to test: baseline, 4 shared and 4 unshared, 
% 6 shared and 2 unshared, 2.5 mm mismatch, 5.0 mm mismatch
% locGUI(repetitions,subjectID,fback, numshared, test, offset)
% Training on standard condition. No cooperating strategy, no pitch
% mismatch. 
locGUI(repetitions,subjectID,1, '62','mism', '0')
fprintf('After you complete a task, click on Finish and press any key when ready for next task\n')
pause
% Testing
%Set up conditions
cond{1}.test='mism'; cond{1}.numshared='44';  cond{1}.offset='0'; % Baseline condition
cond{2}.test='coop'; cond{2}.numshared='44';  cond{2}.offset='0'; % 4 shared, 4 unshared
cond{3}.test='coop'; cond{3}.numshared='62';  cond{3}.offset='0'; % 6 shared, 5 unshared
cond{4}.test='mism'; cond{4}.numshared='44';  cond{4}.offset='25'; % 2.5 mm depth mismatch
cond{5}.test='mism'; cond{5}.numshared='44';  cond{5}.offset='5'; % 5.0 mm mismatch
condOrder= randperm(numConditions);
filename = strcat('results/ConditionOrder',subjectID,datestr(clock,5),datestr(clock,7),datestr(clock,10),'.mat');
save(filename, 'condOrder')
for i=1: numConditions
    ind= condOrder(i);
    locGUI(repetitions,subjectID,0, cond{ind}.numshared,cond{ind}.test, cond{ind}.offset)
    pause
end
fprintf('Test completed\n');
