# YouTube Shorts Machine: AI-Powered Viral Shorts Generator

**Transform long videos into viral-ready shorts automatically.**

This tool combines intelligent vertical video cropping with AI-powered viral moment detection to create engagement-optimized clips for TikTok, Instagram Reels, and YouTube Shorts.

## 🎯 Project Vision

**Current Phase:** Smart vertical video conversion with AI face tracking
**End Goal:** Fully automated viral shorts generation pipeline

### What It Does Now:
- ✅ Automatically converts horizontal → vertical (9:16) format
- ✅ AI-powered scene analysis (YOLOv8) to detect and track people
- ✅ Smart cropping: tracks subjects or adds letterbox based on scene content
- ✅ Transcription generation with word-level timestamps (faster-whisper)
- ✅ **AI viral moment detection (Google Gemini API)** - identifies 3-15 engaging clips (15-60s each)
- ✅ Platform-specific metadata generation (YouTube Shorts, TikTok, Instagram Reels)
- ✅ Viral hook text suggestions for each clip

### Coming Soon (Remaining Features):
- 📹 Automated clip extraction from viral moments
- 📝 Auto-generated subtitles with TikTok-style formatting
- ✨ AI video effects (dynamic zooms, visual enhancements)
- 📅 Multi-clip batch processing with performance analytics

**Philosophy:** Instead of manual editing, let AI analyze your content, find viral moments, and create polished shorts ready to post.

---

## 🗺️ Implementation Roadmap

See [VIRAL_SHORTS_ROADMAP.md](VIRAL_SHORTS_ROADMAP.md) for detailed implementation plan.

### ✅ Phase 1: Core Infrastructure (Completed)
- [x] Vertical video conversion with AI tracking
- [x] Transcript generation (faster-whisper)
- [x] Word-level timestamp extraction

### ✅ Phase 2: Viral Detection (Completed)
- [x] **Google Gemini API integration** for viral moment detection
- [x] **Metadata generation** (titles, descriptions, hooks)
- [ ] Clip extraction (FFmpeg-based)

### 📅 Phase 3: Enhancement Features (Upcoming)
- [ ] Auto-generated subtitles
- [ ] Viral hook text overlays
- [ ] AI video effects
- [ ] Batch processing & reporting

---

### Quick Start

**Current Features: Vertical Video Conversion**

```bash
git clone https://github.com/lingxi-zhou-dev/YouTube-Shorts-Machine.git
cd YouTube-Shorts-Machine
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Convert horizontal video to vertical
python3 main.py -i video.mp4 -o vertical.mp4

# Generate transcript with word-level timestamps
python3 transcribe.py video.mp4 transcript.json

# Detect viral moments from transcript (requires Gemini API key)
python3 viral_detector.py video.mp4
```

The `yolov8n.pt` model weights and Whisper models are downloaded automatically on first run.

**For Viral Detection:** Get a free API key at https://aistudio.google.com/app/apikey and add it to a `.env` file:
```bash
GEMINI_API_KEY=your_api_key_here
```

**Prerequisites:** 
- Python 3.8+ 
- [FFmpeg](https://ffmpeg.org/) (`ffmpeg` + `ffprobe`) in your PATH
- Google Gemini API key (free) for viral moment detection - get one at https://aistudio.google.com/app/apikey

---

### Usage Examples

**Vertical Video Conversion (Available Now):**

```bash
# Basic — 9:16 vertical, balanced quality
python3 main.py -i video.mp4 -o vertical.mp4

# Instagram feed (4:5) with high quality
python3 main.py -i video.mp4 -o vertical.mp4 --ratio 4:5 --quality high

# Fast encode, square format
python3 main.py -i video.mp4 -o vertical.mp4 --ratio 1:1 --quality fast

# Preview the processing plan without encoding
python3 main.py -i video.mp4 -o vertical.mp4 --plan-only

# Full control over encoding parameters
python3 main.py -i video.mp4 -o vertical.mp4 --crf 20 --preset medium

# Use hardware encoder (macOS VideoToolbox / NVIDIA NVENC)
python3 main.py -i video.mp4 -o vertical.mp4 --encoder hw

# Maximum accuracy scene detection (slower)
python3 main.py -i video.mp4 -o vertical.mp4 --frame-skip 0
```

**Viral Shorts Generation (Partial - Detection Available Now):**

```bash
# Current: Detect viral moments and generate metadata
python3 viral_detector.py long_video.mp4

# This will:
# 1. Transcribe the video ✅
# 2. Use AI to detect 3-15 viral moments ✅
# 3. Generate platform-specific metadata ✅
# 4. Save results to long_video_viral_clips.json ✅

# Coming soon: Full pipeline with automatic extraction
python3 main.py -i long_video.mp4 -o clips/ \
  --detect-viral \
  --add-subtitles \
  --add-hooks \
  --platforms tiktok,instagram,youtube

# This will also:
# 5. Extract each clip to vertical format 🚧
# 6. Add subtitles and hook text overlays 🚧
# 7. Output ready-to-post clips 🚧
```

# Maximum accuracy scene detection (slower)
python3 main.py -i video.mp4 -o vertical.mp4 --frame-skip 0
```

---

### All Flags

**Output:**

| Flag | Default | Description |
|------|---------|-------------|
| `-i`, `--input` | *(required)* | Path to input video |
| `-o`, `--output` | *(required)* | Path to output video (`.mp4` appended if no extension) |
| `--ratio` | `9:16` | Output aspect ratio. Examples: `9:16`, `4:5`, `1:1` |

**Encoding quality:**

| Flag | Default | Description |
|------|---------|-------------|
| `--quality` | `balanced` | Preset: `fast`, `balanced`, or `high` (see table below) |
| `--encoder` | `auto` | `auto` = libx264 (software), `hw` = hardware if available, or explicit name like `h264_videotoolbox` |
| `--crf` | *(from quality)* | Override CRF directly, 0-51 lower = better (libx264 only) |
| `--preset` | *(from quality)* | Override x264 preset directly: `ultrafast`..`veryslow` (libx264 only) |

**Quality presets (libx264):**

| `--quality` | CRF | Preset | Typical use |
|-------------|-----|--------|-------------|
| `fast` | 28 | veryfast | Quick previews, drafts |
| `balanced` | 23 | fast | Good quality, reasonable speed |
| `high` | 18 | slow | Best quality, largest file, slowest |

**Scene detection tuning:**

| Flag | Default | Description |
|------|---------|-------------|
| `--frame-skip` | `0` | Frames to skip during scene detection. `0` = every frame (most accurate). `1` = every other frame (~2x faster). Higher = faster but may miss cuts |
| `--downscale` | `0` (auto) | Downscale factor for scene detection. `0` = auto. `2`-`4` = faster but may miss subtle cuts |

**Other:**

| Flag | Default | Description |
|------|---------|-------------|
| `--plan-only` | off | Run scene detection + analysis only, print the plan, exit without encoding |

---

### Transcript Generation

Generate accurate transcripts with word-level timestamps using the `transcribe.py` module powered by faster-whisper.

**Quick Start:**

```bash
# Basic usage - prints transcript summary
python3 transcribe.py video.mp4

# Save transcript to JSON file
python3 transcribe.py video.mp4 output.json

# Choose model size (tiny, base, small, medium, large)
# Smaller = faster, Larger = more accurate
python3 transcribe.py video.mp4 output.json  # uses 'base' by default
```

**What it generates:**

The JSON file generated by `transcribe.py` contains:
- Full transcript text
- Word-level timestamps (precise to 0.01s)
- Segment information with start/end times
- Detected language

**Usage in Python:**

```python
from transcribe import transcribe_video, extract_words_in_range, get_transcript_text_in_range

# Transcribe video
transcript = transcribe_video('video.mp4', model_size='base')

# Extract words between 10-20 seconds
words = extract_words_in_range(transcript, 10.0, 20.0)

# Get text for a specific time range
text = get_transcript_text_in_range(transcript, 10.0, 20.0)
```

**Model Sizes & Performance:**

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| `tiny` | ~20x faster | Good | Quick drafts, simple speech |
| `base` | ~10x faster | **Recommended** | General use (default) |
| `small` | ~5x faster | High quality | Complex terminology |
| `medium` | ~3x faster | Very high | Professional transcription |
| `large` | ~1.5x faster | Best | Maximum accuracy needed |

*Example: 6-minute video transcribed in ~20 seconds with the `base` model on Apple Silicon.*

**Testing:**

Run the test script to verify transcription is working:

```bash
# Place a test video in the directory (named test_video.mp4 or sample.mp4)
python3 test_stage_1_1.py
```

The `test_stage_1_1.py` script verifies that:
- faster-whisper is properly installed
- Transcription runs without errors
- Word-level timestamps are accurate
- Helper functions work correctly

---

### Viral Moment Detection

Automatically identify the most engaging clips from your video transcripts using AI.

**Setup:**

1. Get a free Google Gemini API key: https://aistudio.google.com/app/apikey
2. Create a `.env` file in the project directory:
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

**Quick Start:**

```bash
# Analyze video and detect viral moments
python3 viral_detector.py video.mp4

# This will:
# 1. Transcribe the video (if not already done)
# 2. Send transcript to Gemini API for analysis
# 3. Identify 3-15 viral clips (15-60 seconds each)
# 4. Save results to video_viral_clips.json
```

**What It Generates:**

The output JSON file contains for each identified clip:
- **Precise timestamps** (start/end times in seconds)
- **Viral hook text** (catchy 10-word overlay suggestion)
- **YouTube Shorts title** (optimized for YouTube)
- **TikTok description** (with trending hashtags)
- **Instagram Reels description** (with relevant hashtags)

**Example Output:**
```json
{
  "clips": [
    {
      "start": 106.02,
      "end": 138.74,
      "viral_hook_text": "Keto beats Ozempic for hunger?",
      "video_title_for_youtube_short": "Keto vs Ozempic: The ULTIMATE Hunger Hormone Showdown! 🔥",
      "video_description_for_tiktok": "Keto isn't just about fat! It naturally boosts GLP1...",
      "video_description_for_instagram": "Forget Ozempic! Learn how keto naturally..."
    }
  ]
}
```

**Usage in Python:**

```python
from transcribe import transcribe_video
from viral_detector import detect_viral_clips

# Step 1: Transcribe video
transcript = transcribe_video('video.mp4')

# Step 2: Detect viral moments
clips = detect_viral_clips(transcript, video_duration=300)

# Step 3: Use the clips
for clip in clips:
    print(f"Clip: {clip['start']:.1f}s - {clip['end']:.1f}s")
    print(f"Hook: {clip['viral_hook_text']}")
    print(f"YouTube: {clip['video_title_for_youtube_short']}")
```

**Model Options:**

```python
from viral_detector import ViralDetector

# Use default model (gemini-2.5-flash - fast & free)
detector = ViralDetector()

# Use higher quality model
detector = ViralDetector(model="gemini-2.5-pro")

clips = detector.detect_viral_clips(transcript, video_duration=300)
```

**What the AI Looks For:**
- Strong hooks (first 3 seconds are critical)
- Jaw-dropping facts or revelations
- Emotional moments and plot twists
- Actionable tips and life hacks
- Controversial or debate-worthy content
- Natural cutting points (pauses, topic changes)

**Testing:**

```bash
# Run the test suite (requires Gemini API key in .env)
python3 test_stage_1_2.py
```

The test validates:
- API connection works
- JSON responses are properly formatted
- Clip durations are within valid range (15-60s)
- All required metadata fields are present

---

### Key Features

**Current Features (Vertical Conversion):**

*   **Content-Aware Cropping:** YOLOv8 detects people and centers the vertical frame on them.
*   **Automatic Letterboxing:** When people are too spread out for a vertical crop, black bars are added to preserve the full shot.
*   **Scene-by-Scene Processing:** Decisions are made per scene for consistent, logical edits.
*   **Native Resolution:** Output height matches the source to prevent quality loss from upscaling.
*   **Frame-Accurate Processing:** Every frame is processed individually with the correct per-scene strategy — no timestamp rounding or scene boundary drift.
*   **Hardware Encoder Support:** Optional `--encoder hw` auto-detects VideoToolbox (macOS) or NVENC (NVIDIA) with automatic fallback to libx264.
*   **VFR Handling:** Variable frame rate sources are automatically normalized before processing.
*   **Audio Sync:** Non-zero stream start times are detected and compensated to keep audio/video aligned.
*   **Transcription:** faster-whisper generates word-level timestamps for precise subtitle timing.

**Planned Features (Viral Shorts Pipeline):**

*   **AI Viral Moment Detection:** Gemini API analyzes transcripts to identify 3-15 high-engagement clips (15-60s each)
*   **Auto Subtitles:** TikTok-style captions with word-level timing, customizable fonts and colors
*   **Hook Text Overlays:** AI-generated attention-grabbing text ("Did you know?", "Stop doing this!")
*   **AI Video Effects:** Context-aware zooms, visual enhancements based on speech content
*   **Platform Optimization:** Auto-generate titles, descriptions, hashtags for TikTok/Instagram/YouTube
*   **Batch Processing:** Process multiple videos, generate analytics reports
*   **Social Auto-Publishing:** Direct posting to platforms via Upload-Post API (optional)

---

### How It Works

**Current Pipeline (Vertical Conversion):**

```
Input Video
    |
    v
+-------------------------------+
| 1. Scene Detection            |  PySceneDetect splits the video into scenes
|    (--frame-skip, --downscale)|
+---------------+---------------+
                |
                v
+-------------------------------+
| 2. Content Analysis           |  YOLOv8 detects people in each scene's
|    (middle frame per scene)   |  middle frame; Haar cascade finds faces
+---------------+---------------+
                |
                v
+-------------------------------+
| 3. Strategy Decision          |  Per scene: TRACK (crop on subject)
|                               |  or LETTERBOX (scale + black bars)
+---------------+---------------+
                |
                v
+-------------------------------+
| 4. Frame Processing           |  Per-frame crop/scale/pad via OpenCV
|    (--quality, --encoder)     |  piped to FFmpeg for encoding
+---------------+---------------+
                |
                v
+-------------------------------+
| 5-6. Audio extract + merge    |  Audio synced with start-time offset
+---------------+---------------+
                |
                v
          Output Video
```

**Viral Shorts Pipeline (Partially Complete):**

```
Long Video Input (10-60 min)
    |
    v
+-------------------------------+
| 1. Transcription ✅           |  faster-whisper: word-level timestamps
+---------------+---------------+
                |
                v
+-------------------------------+
| 2. AI Viral Detection ✅      |  Google Gemini analyzes transcript
|    (Google Gemini API)        |  Identifies 3-15 viral moments (15-60s)
|                               |  Generates hooks & metadata
+---------------+---------------+
                |
                v
+-------------------------------+
| 3. Clip Extraction 🚧         |  FFmpeg cuts precise clips
+---------------+---------------+
                |
                v
+-------------------------------+
| 4. Vertical Conversion        |  Existing pipeline (steps 1-6 above)
+---------------+---------------+
                |
                v
+-------------------------------+
| 5. Enhancement                |  Add subtitles, hooks, AI effects
+---------------+---------------+
                |
                v
+-------------------------------+
| 6. Metadata Generation        |  Platform-specific titles/descriptions
+---------------+---------------+
                |
                v
    Multiple Viral Clips Ready to Post
    (with metadata JSON per clip)
```

Steps 1-3 are the "analysis" phase (AI-powered). Steps 4-6 apply enhancements and prepare for distribution.

Steps 1-3 are the "planning" phase (Python + AI). Step 4 applies the plan frame-by-frame and encodes via FFmpeg.

---

### Performance

Benchmarks on Apple M1 MacBook Pro (AC power):

| Resolution | Duration | Total time | Speed |
|-----------|----------|-----------|-------|
| 1280x720 | 49s | ~6s | 8.3x real-time |
| 1920x1080 | 12 min | ~51s | 13.7x real-time |

Scene detection is the dominant bottleneck (~50% of total time).

---

### Technical Details

This tool is built on a pipeline that uses specialized libraries for each step:

*   **Current Stack (Vertical Conversion):**
    *   `PySceneDetect`: For accurate, content-aware scene cut detection.
    *   `Ultralytics (YOLOv8)`: For fast and reliable person detection.
    *   `OpenCV`: Used for frame manipulation, face detection (as a fallback), and reading video properties.
    *   `FFmpeg` / `ffprobe`: The backbone of video encoding, audio extraction, and media stream analysis.
    *   `tqdm`: For clean and informative progress bars in the console.
    *   `faster-whisper`: CPU-optimized Whisper implementation for transcription.

*   **Implemented Stack (Viral Detection):**
    *   `Google Gemini API` ✅: AI-powered viral moment detection and content analysis.
    *   `google-genai` ✅: Official Google Gemini Python SDK.
    *   `python-dotenv` ✅: Environment variable management for API keys.

*   **Planned Stack (Remaining Features):**
    *   `Pillow (PIL)`: For generating hook text overlay images with styling.
    *   `Upload-Post API` (optional): Multi-platform social media publishing.

*   **Current Processing Pipeline:**
    1.  **(Pre-processing)** If the source is VFR, it is normalized to constant frame rate.
    2.  `PySceneDetect` scans the video and returns a list of scene timestamps.
    3.  For each scene, `OpenCV` extracts a sample frame and `YOLOv8` detects people in it.
    4.  A set of rules determines the strategy (`TRACK` or `LETTERBOX`) for each scene based on the number and position of detected people.
    5.  OpenCV reads every frame sequentially. Each frame is cropped/resized (TRACK) or scaled/padded (LETTERBOX) according to its scene's strategy, then piped as raw pixels to FFmpeg for encoding. This frame-by-frame approach guarantees frame-accurate scene boundaries with no timestamp rounding errors.
    6.  Audio is extracted separately (with start-time offset correction), then merged with the processed video.

---

### Changelog

#### v1.5.0 (2026-04-03) — AI Viral Moment Detection

**New Features:**

*   **Google Gemini API Integration.** New `viral_detector.py` module identifies 3-15 viral moments (15-60s each) from video transcripts. Uses Google Gemini 2.5 Flash for fast, free analysis or Gemini 2.5 Pro for higher quality results.
*   **Platform-specific metadata generation.** Automatically creates optimized titles and descriptions for YouTube Shorts, TikTok, and Instagram Reels, including trending hashtags.
*   **Viral hook text suggestions.** AI generates catchy 10-word overlay text for each clip to maximize engagement.
*   **Environment-based API key management.** Secure `.env` file support via `python-dotenv` for API credentials.
*   **Comprehensive viral detection testing.** New `test_stage_1_2.py` validates API integration, JSON formatting, and clip validation logic.

**What the AI Analyzes:**
*   Strong hooks and attention-grabbing openings
*   Jaw-dropping facts, emotional moments, plot twists
*   Actionable tips and controversial content
*   Natural cutting points at pauses or topic changes

**Usage:**
```bash
# Get free API key from https://aistudio.google.com/app/apikey
echo "GEMINI_API_KEY=your_key_here" > .env

# Detect viral moments
python3 viral_detector.py video.mp4

# Run tests
python3 test_stage_1_2.py
```

**Technical Details:**
*   Uses `google-genai` SDK (latest, non-deprecated version)
*   JSON-mode response for reliable parsing
*   Validates clip durations (15-60s), timestamps, and required fields
*   Free tier: 60 requests/minute with Gemini 2.5 Flash

#### v1.4.1 (2026-02-15) — Cropping Accuracy Fix

*   **Fixed incorrect crop/letterbox decisions near scene boundaries.** The v1.3 `filter_complex` pipeline used seconds-based `trim` filters, which caused floating-point misalignment with the frame-based scene boundaries from PySceneDetect. This led to frames at scene transitions receiving the wrong strategy (e.g., a properly tracked person switching to letterbox mid-scene, or a group shot being cropped instead of letterboxed). Restored the original frame-by-frame processing pipeline which uses exact frame numbers for scene boundary matching, guaranteeing frame-accurate results.

#### v1.4.0 (2026-02-15) — Hardware Encoding & Scene Detection Tuning

**New Features:**

*   **Hardware encoder support (`--encoder`).** New flag with three modes: `auto` (libx264, default for best quality/compatibility), `hw` (auto-detect VideoToolbox on macOS or NVENC on NVIDIA), or an explicit encoder name. Quality presets (`--quality`) map automatically per encoder type.
*   **Configurable scene detection (`--frame-skip`, `--downscale`).** Power users can tune the speed/accuracy trade-off. Default `--frame-skip 0` processes every frame for maximum accuracy; increase for faster detection on longer videos.

#### v1.3.0 (2026-02-15) — Configurable Output & Quality Presets

**New Features:**

*   **Configurable aspect ratio (`--ratio`).** Output is no longer locked to 9:16. Use `--ratio 4:5` for Instagram feed, `--ratio 1:1` for square, or any custom W:H ratio.
*   **Quality presets (`--quality`).** Choose between `fast` (CRF 28, veryfast), `balanced` (CRF 23, fast — default), or `high` (CRF 18, slow). Power users can override directly with `--crf` and `--preset`.
*   **Dry-run mode (`--plan-only`).** Runs scene detection and analysis only, prints the processing plan, and exits without encoding. Useful for previewing decisions before committing to a long encode.
*   **Fixed output pixel format.** Encoder now outputs `yuv420p` instead of `yuv444p`, which is compatible with all players and platforms and produces smaller files.
*   **Improved logging and progress reporting.** Input file summary upfront (resolution, duration, fps, codec, file size, frame count), progress bars on all slow operations, and a final summary with output size, compression ratio, and processing speed.

#### v1.1.0 (2026-02-14)

**Bug Fixes:**

*   **Fixed audio/video desynchronization.** This was caused by two separate issues:
    *   The frame rate was being read from PySceneDetect while frames were read by OpenCV. A mismatch between the two (e.g. 29.97 vs 30.0) caused the encoded video duration to drift from the audio. FPS is now read from OpenCV (the same backend that reads the frames) with explicit `-vsync cfr` enforcement.
    *   Many source files (especially YouTube downloads) have a non-zero `start_time` on the video stream (e.g. audio at 0.0s, video at 1.8s). The script now detects this offset via `ffprobe` and trims the extracted audio to match, so the two streams stay aligned.
*   **Fixed crash on videos without an audio stream.** The script now detects whether audio exists using `ffprobe` and skips the audio extraction/merge steps gracefully.
*   **Fixed hardcoded `.aac` temp audio file.** The temp audio container is now `.mkv`, which accepts any audio codec. Previously, source files with non-AAC audio (MP3, Opus, AC3, etc.) could fail or produce corrupt output.
*   **Fixed crash when output path has no file extension.** The script now auto-appends `.mp4` if no extension is provided.
*   **Fixed orphaned temp files on failure.** Temporary files are now cleaned up on all exit paths, not just on success.

**Improvements:**

*   **Variable frame rate (VFR) handling.** Phone-recorded videos often use VFR, which caused frame timing drift. The script now detects VFR sources via `ffprobe` and normalizes them to constant frame rate before processing.
*   **Corrupt frame resilience.** If a frame fails to process (bad crop, corrupt data), it is duplicated from the previous good frame instead of being dropped. This preserves the total frame count and prevents audio drift.
*   **Lazy model loading.** YOLO and Haar cascade models are now loaded on first use instead of at import time. Heavy library imports (`torch`, `ultralytics`, `cv2`, etc.) are deferred until after argument parsing, so `--help` is instant.
*   **Pinned dependency versions.** `requirements.txt` now specifies compatible version ranges to prevent breakage from upstream changes.
*   **Replaced `exit()` with `sys.exit(1)`.** Ensures proper exit codes and reliable behavior in all environments.
