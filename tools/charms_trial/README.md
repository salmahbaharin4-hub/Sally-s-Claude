# Set Asas Percubaan (Trial) Charms: skrip video

Jalankan dari folder ini (input: `../../videos/charms_skin_refining_set_gabung.mp4`, 15s klip kotak + 10.6s klip isi set):

- `python3 track_box.py ../../videos/charms_skin_refining_set_gabung.mp4 box.json`: kesan kedudukan/kecondongan kotak (15s pertama)
- `python3 video1_render.py ../../videos/charms_skin_refining_set_gabung.mp4 out1.mp4 box.json`, kemudian ambil 448 frame pertama, tanpa audio → `videos/charms_trial_video1_kotak.mp4`
- `python3 video2_render.py ... full.mp4 box.json`, kemudian ambil dari frame 448 → `videos/charms_trial_video2_isi_set.mp4`

Fon: Liberation Serif Bold. Video 2 render juga perlukan `cand10.3.png` tidak (tiada thumbnail dalam video 2).
