import re, json, wave, sys, numpy as np
from piper import PiperVoice
voice = PiperVoice.load(sys.argv[1])
text = open("script.txt").read()
sents = [s.strip() for s in re.split(r'(?<=[.?!:])\s+', text.replace("\n", " ")) if s.strip()]
sr = voice.config.sample_rate
gap = np.zeros(int(sr * 0.22), dtype=np.int16)
pcm, t, out = [], 0.0, []
from piper import SynthesisConfig
cfg = SynthesisConfig(length_scale=0.97)
for i, s in enumerate(sents):
    a = np.concatenate([np.frombuffer(c.audio_int16_bytes, dtype=np.int16) for c in voice.synthesize(s, syn_config=cfg)])
    # trim leading/trailing near-silence
    nz = np.where(np.abs(a) > 300)[0]
    a = a[max(nz[0]-200,0):nz[-1]+800]
    dur = len(a) / sr
    words = s.split()
    w = np.array([len(x.strip(".,?!:")) + 2 for x in words], float); w = w / w.sum() * dur
    ts = t
    for x, d in zip(words, w):
        out.append({"text": x, "start": round(ts, 3), "end": round(ts + d, 3), "sent": i}); ts += d
    pcm += [a, gap if not s.endswith(("?", ":")) else np.zeros(int(sr*0.32), dtype=np.int16)]
    t += dur + (0.22 if not s.endswith(("?", ":")) else 0.32)
    if s in ("Entscheide dich.",): pcm.append(np.zeros(int(sr*2.4), dtype=np.int16)); t += 2.4
    print(f"{i:2d} {out[-len(words)]['start']:6.2f} {s}")
with wave.open("assets/voice-raw.wav", "wb") as f:
    f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes(np.concatenate(pcm).tobytes())
json.dump(out, open("assets/words.json", "w"), ensure_ascii=False, indent=0)
print("total", t)
