This was made for my personal use so a lot of things are hardcoded in & assumed (i.e. 1920 x 1080, OBS setup correctly, etc)

---

- Run `save_replays.py` to save the replays (probably optional?)
- Run `record_replays.py` to record the replays (OBS must be opened)
- Run `video_renamer.py` to fix the names 
- Run `video_trimmer.py` to trim the videos
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