<h1>PomoLocker</h1>
<img src="./github/presentation.gif" width="657" height="640" />

<h2>Description</h2>
This is a project I created because I could not find a Pomodoro app that would lock my screen automatically once the timer's up, so here it
is! <br />
This app is not published anywhere because I did not want to deal with apple's review process (I think they would not approve this app since
it locks the screen automatically) and also because I did not want to pay for
an Apple developer account. But if you are willing to go through all of this stuff, feel free to publish it, the only thing I would like to ask is to make
the app free! <br />
I use this app daily so I will probably keep it updated, but I can't promise anything.

<h2>Building the App</h2>
To build this app you must have Python installed, version 3.13.5 or later (I have tried older versions, and it did not work), and MacOS
Sequoia 15.6.1 or later.

All you have to do is clone the repository and run the following commands: <br />
```
python3.13 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python setup.py py2app
```
After everything is done, you should be able to find the app in the dist folder inside the project, you can move it to your `~/Applications`
folder for example.

<h2>Compatibility</h2>
<ul>
  <li>MacOS Sequoia 15.6.1</li>
  <li>Python 3.13.5 (I have tried older versions, and it did not work)</li>
</ul>

<h2>Plans for the Future</h2>
I want to make the icon look better but so far I wasn't able to figure it out how to do it. For some reason, it is bigger than other app
icons. <br /> 
I would like to make this app work on Linux and Windows as well, but nothing has been done on this topic yet.
