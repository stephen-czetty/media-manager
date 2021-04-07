# media-manager #

A collection of music library related utilities.

This is mainly an effort to consolidate all the little one-off scripts that I've put together
over time.  Maybe once that's done, I'll expand it some more.

## Commands ##

- Extract an audio file from a container: `media.py extract foo.mkv`
- Add a cover image to an ogg (Vorbis/Opus) file: `media.py ogg coverimage foo.ogg foo.jpg`
- Add tags to an ogg (Vorbis/Opus) file: `media.py ogg tag foo.ogg --artist 'Some artist' --title 'Some song'`
  - Only artist and title at the moment
