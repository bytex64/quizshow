# QUIZ SHOW!

Quiz Show is a curses-based game show program written in python.  It
loads questions defined in a YAML file, displays answers, and allows the
host to keep track of the contestants' scores.  It also display images
using the framebuffer viewer fbv, and video using omxplayer for
Raspberry Pi, though these are external and any other image/video
programs can be substituted in their place.

## Installing

Quiz Show will run directly from the git checkout (and indeed there is
currently no way to install it).  It requires Python YAML, installable
on debian systems with:

$ sudo apt-get install python-yaml

## Running

Once you have that installed, it's as simple as

$ ./quizshow.py

After each item in the quiz script is run, Quiz Show will write its
state to a file called 'state.yml'.  To resume a previous game, specify
a state yaml file as the only argument.

$ ./quizshow.py state.yml

## Data format

The program automatically loads `dino-jack.yml`, the provided example
dinosaur quiz game.  The format is a YAML list of steps to display.

### q

The question format has a question, which is automatically wrapped, a
set of up to four answers, and which answer is the correct one.
Optionally, you can specify the point value, which defaults to 10.

    - q: This is the question
      a:
        - First answer
        - Second answer
        - Third answer
      # Base zero.  This is the first answer
      w: 0
      points: 30

### title

The title shows a standalone title card.

    - title:
        head: This is in bold
        text: This text is below the title

### image

Displays an image with an external player.

    - image: images/YDKDJ title.png

### video

Plays a video with an external player.

    - video: videos/Jurassic Park.mp4

## You Don't Know Dino-Jack

The included dinosaur trivia game uses a number of external video files
that are not included here because they're just too big, in addition to
having questionable copyright status.  The script is still usable
without them, but some of the context is lost.  In particular: 

- Question three was a short clip of Dino greeting Fred Flintstone as he
  comes home from work.

- Question five was an excerpt from the music video from "Walk the
  Dinosaur" by Was (Not Was).

- Question 13 was this youtube video:
  http://youtube.com/watch?v=ZlPoPMbiffU
