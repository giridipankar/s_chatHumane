import soundfile as sf
import torchaudio
import torch
from espnet2.bin.asr_inference import Speech2Text

print("Starting ASR model load...")
model = Speech2Text.from_pretrained("espnet/kamo-naoyuki_librispeech_asr_train_asr_conformer6_n_fft512_hop_length2-truncated-a63357")  # or use Hugging Face ID if online
print("ASR model loaded.")

def audio_to_text(file_path):
    print(f"Loading audio file: {file_path}")
    waveform, sample_rate = torchaudio.load(file_path)
    print(f"Original waveform shape: {waveform.shape}, sample rate: {sample_rate}")

    # Convert to mono if stereo
    if waveform.shape[0] > 1:
        print("Converting stereo to mono...")
        waveform = torch.mean(waveform, dim=0, keepdim=True)
        print(f"Mono waveform shape: {waveform.shape}")

    # Resample if not 16kHz
    if sample_rate != 16000:
        print(f"Resampling from {sample_rate} to 16000 Hz...")
        resampler = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=16000)
        waveform = resampler(waveform)
        print(f"Resampled waveform shape: {waveform.shape}")

    # Convert from Torch Tensor to NumPy array (ESPnet expects NumPy)
    speech = waveform.squeeze().numpy()
    print(f"Speech array shape: {speech.shape}")

    # Inference
    print("Running ASR inference...")
    try:
        text, *_ = model(speech)[0]
        print("Recognized Text:", text)
    except Exception as e:
        print(f"ASR inference error: {e}")
    return text
