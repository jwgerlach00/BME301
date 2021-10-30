function roving(track,fs)
% computer volume at 4/10 of max
sqT = track.^2;
avgT = mean(sqT,1);
sqrtAvgT = sqrt(avgT);
rmsTrack = mean(sqrtAvgT,2);
% finds the rms value
scale = rand(1,1)*0.14+0.034;
% shifting the amplitude so that the output is within a range of 59 to 71dB
% the values will be randomly distributed within this range
track2 = track*scale/rmsTrack;
% creates the new loudness roved track
sound(track2,fs);
% plays the track
end