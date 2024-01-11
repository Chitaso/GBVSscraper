# GBVS Scraper

This project is being discontinued.

I initially created these scripts in order to create youtube videos of the game `Granblue Fantasy Versus` by scraping the top replays list for top level replays to show to the public. With the new installment `Granblue Fantasy Versus Rising` and varioius other personal factors, I feel that this project has run its due course and so I have discontinued it.

---

This was made for my personal use so a lot of things are hardcoded in & assumed (i.e. 1920 x 1080, OBS setup correctly, etc)

---

- Run `clean.py` to clean out the replays
- Run `save_replays.py` to save the replays (probably optional?)
- Run `record_replays.py` to record the replays (OBS must be opened)
- Run `video_renamer.py` to fix the names 
- Run `video_trimmer.py` to trim the videos
- Run `ending_anim_fixer.py` to fix the ending animations
- Run `video_analyzer.py` to find out who wins
- Run `analysis_compiler.py` to compile the videos
- Run `video_maker.py` to create the final video

Run `clean.py` to clean up the directory for a new scraping

---

I use `.replace` in certain parts of the code so make sure paths don't get fucked up

Also make sure there aren't any spaces in your file names

The GBVS scraper requires your cursor to not select the top element -> highlighting changes some pixel colors which is annoying :I

---

Create a `config.toml` that looks like

```toml
[connection]
host = "localhost"
port = 4455
password = "PASSWORD_HERE"
```
