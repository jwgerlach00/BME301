function locGUI(repetitions,subjectID,fback, numshared, test, offset)
% GUI for localization
%%%%% WARNING - HRTF only works for angle multiples of 5 %%%%%%
locparams.sharing = numshared; % a string representing the sharing patern. either '44' or '62'
locparams.test = test; % either 'coop' or 'mism'
locparams.offset = offset; % either 0 for standard case, 2.5 or 5
locparams.repetitions = repetitions; % the number of repitions for each speaker
locparams.feedback = fback;

%% angle variables
numspkrs = 8; % eight speakers set 20 degrees apart
angles = linspace(20,160,numspkrs);
% generates the angles for the sounds
indices = zeros(1,numspkrs*repetitions);
for i = 1:repetitions
    indices((i-1)*numspkrs+1:i*numspkrs) = 1:numspkrs;
end
randindices = [rand(1,numspkrs*repetitions);indices]';
% generates a matrix with indicies and random numbers
randindices = sortrows(randindices,1);
% randomizes the indicies by sorting the matrix according to the random numbers

angresp = zeros(repetitions*numspkrs,1);
angreal = zeros(repetitions*numspkrs,1);
% initializes the variables
 
round = 0; done = 0;
if test=='coop'
    endstr = numshared;
else
    if strcmp(offset,'0')
        endstr = 'STD';
    else
        endstr = ['off' offset];
    end
end
filename = strcat('pnb',endstr,'.mat');
% generates the filename according to which specific test is being run
S = load(filename); % creates a structure
pnb = eval(['S.pnb' endstr]);
% assigns the variable pnb (pink noise bursts) from the structure

filename = strcat('results/',subjectID,endstr,datestr(clock,5),datestr(clock,7),datestr(clock,10),'.mat');
% creates the results file name for the subject, date, and task


%% Visual Elements
fig = figure('Position',[300,300,500,500],...
    'Color',[1,1,1],...
    'Name','Localization',...
    'MenuBar','none',...
    'NumberTitle','off'); % generates the GUI

pb = uicontrol('Style','pushbutton',...
    'String','Start',...
    'position',[150 100 200 75],...
    'Callback',{@pbCB},...
    'FontSize',20); % creates the start button

r = 200; % radius of the semi-circle of speakers
th = linspace(20/360*2*pi,160/360*2*pi,numspkrs); 
% generates the angles for the spacing of the buttons
x = r*cos(th)+235; % creates the horizontal position for each speaker
y = r*sin(th)+250; % creates the vertical position for each speaker

%% speaker buttons
spkrs=zeros(numspkrs,1);
for i = 1:numspkrs
    spkrs(i) = uicontrol('Style','pushbutton',...
        'String',num2str(uint8(numspkrs-i+1)),...
        'pos',[x(i) y(i) 30 30],...
        'HandleVisibility','off',...
        'Callback',{@rbCB},...
        'Tag',num2str(i));
end % creates the 8 speakers

%% Nadeem's Head
% generates the picture of a man's head to give the subject a feel for
% their locations relative to the virtual speakers.
rN = 0.05; % head radius
xc = 0.4728; % center x-position
yc = 0.4797; % center y-position
rectangle('Position', [xc-rN yc-rN 2*rN 2*rN], 'Curvature', [1 1]);
rectangle('Position', [xc+rN yc-7*rN/10/2 3*rN/20, 7*rN/10], 'Curvature', [1 0.5])
rectangle('Position', [xc-rN-3*rN/20 yc-7*rN/10/2 3*rN/20, 7*rN/10], 'Curvature', [1 0.5])
noseL = 1/5;
noseW = 1/5;
line([xc-rN*noseW xc; xc xc+rN*noseW], [yc+rN yc+rN+rN*noseL; yc+rN+rN*noseL yc+rN], zeros(2, 2), 'Color', 'k','LineWidth',1.2)
axis equal
axis([0 1 0 1])
axis off

%% Initial Conditions
set(spkrs,'Enable','off'); % turns the push buttons off

%% Callback functions
    function pbCB(pb,eventdata)
        if done == 0
            set(pb,'Enable','off'); % turns off the speaker response buttons
            playsnd()
            set(spkrs,'Enable','on');
            % enables the speakers to allow the subject to respond
        else
            close(fig);
        end
    end

    function rbCB(rb,eventdata)
        tagnum = str2num(get(rb,'Tag'));
        angresp(round) = 90 - angles(tagnum);
        if exist(filename, 'file')
            save(filename,'angreal','angresp','locparams','-append');
            % saves the real and response data to an existing file
        else
            save(filename,'angreal','angresp','locparams');
            % creates a file and saves the real and response data
        end
        if fback
            if angresp(round)==angreal(round) % if the answer is correct
                set(spkrs(tagnum),'BackgroundColor',[0 1 0]); % turns the answer green
                pause(0.1);
                set(spkrs(tagnum),'BackgroundColor','default'); 
                % returns the button to default color
            else % if the answer is incorrect
                set(spkrs(9-randindices(round,2)),'BackgroundColor',[0 1 0]);
                % makes the correct answer green
                set(spkrs(tagnum),'BackgroundColor',[1 0 0]);
                % makes the response red
                pause(0.1);
                set(spkrs(9-randindices(round,2)),'BackgroundColor','default');
                set(spkrs(tagnum),'BackgroundColor','default');
                % returns the buttons to the default color
            end
        end
        if round==numspkrs*repetitions
            set(pb,'String','Finish'); % Creates a finish button to close the window
            done = 1;
            set(pb,'Enable','on'); % enables the finish button
            set(spkrs,'Enable','off'); % disables the speaker buttons
        else
            set(spkrs,'Enable','off');
            playsnd();
            set(spkrs,'Enable','on');
            % enables the speakers to allow the subject to respond
        end
    end

    function playsnd()
        round = round+1; % keeps track of the number of stimuli that have been played
        angreal(round) = angles(randindices(round,2))-90;
        % records the actual angle values
        track = pnb{randindices(round,2)};
        roving(track,44100); 
        % calls the roving function to loudness rove the sound
        % roving also plays the stimuli
        tmax = length(track)/44100;
        pause(tmax);
    end
end