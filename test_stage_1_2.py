"""
Test script for Stage 1.2: Viral Clip Detection with Google Gemini
Tests the viral_detector.py module
"""

import os
import json
from viral_detector import detect_viral_clips, ViralDetector


def test_with_sample_transcript():
    """Test viral detection with a sample transcript."""
    
    print("=" * 70)
    print("🧪 TEST 1: Sample Transcript (Health/Wellness Topic)")
    print("=" * 70)
    
    # Sample transcript with word-level timestamps
    sample_transcript = {
        'text': """
        Did you know that walking just 30 minutes a day can dramatically reduce your 
        risk of heart disease? This is something that most people don't realize. 
        A recent study from Harvard Medical School found that regular walking can 
        reduce your risk by up to 35 percent. That's almost as effective as many 
        medications, but completely free and with zero side effects. 
        
        Here's the crazy part - it doesn't even have to be intensive exercise. 
        Just a simple walk around your neighborhood, listening to music or a podcast, 
        can make this huge difference. The key is consistency. You need to do it 
        most days of the week. 
        
        Now, if you want to take it to the next level, try adding some intervals. 
        Walk at your normal pace for two minutes, then speed up for 30 seconds. 
        This interval training can boost your metabolism and help you burn more 
        calories throughout the day. Some studies show you can burn up to 50 percent 
        more fat this way.
        """,
        'segments': [
            {
                'start': 0.0,
                'end': 15.5,
                'text': 'Did you know that walking just 30 minutes a day can dramatically reduce your risk of heart disease?',
                'words': [
                    {'word': 'Did', 'start': 0.0, 'end': 0.2},
                    {'word': 'you', 'start': 0.2, 'end': 0.35},
                    {'word': 'know', 'start': 0.35, 'end': 0.6},
                    {'word': 'that', 'start': 0.6, 'end': 0.8},
                    {'word': 'walking', 'start': 0.8, 'end': 1.2},
                    {'word': 'just', 'start': 1.2, 'end': 1.5},
                    {'word': '30', 'start': 1.5, 'end': 2.0},
                    {'word': 'minutes', 'start': 2.0, 'end': 2.5},
                ]
            },
            {
                'start': 15.5,
                'end': 25.0,
                'text': 'This is something that most people do not realize.',
                'words': [
                    {'word': 'This', 'start': 15.5, 'end': 15.8},
                    {'word': 'is', 'start': 15.8, 'end': 16.0},
                    {'word': 'something', 'start': 16.0, 'end': 16.6},
                ]
            },
            {
                'start': 45.0,
                'end': 58.2,
                'text': "Here's the crazy part - it doesn't even have to be intensive exercise.",
                'words': [
                    {'word': "Here's", 'start': 45.0, 'end': 45.5},
                    {'word': 'the', 'start': 45.5, 'end': 45.7},
                    {'word': 'crazy', 'start': 45.7, 'end': 46.2},
                    {'word': 'part', 'start': 46.2, 'end': 46.6},
                ]
            }
        ],
        'language': 'en'
    }
    
    video_duration = 120.0  # 2 minutes
    
    try:
        print(f"\n📊 Video Duration: {video_duration}s")
        print(f"📝 Transcript Length: {len(sample_transcript['text'])} characters")
        print(f"🌍 Language: {sample_transcript['language']}")
        
        print("\n🔍 Calling Gemini API to detect viral moments...")
        clips = detect_viral_clips(sample_transcript, video_duration)
        
        print(f"\n✅ SUCCESS! Found {len(clips)} viral clips\n")
        
        for i, clip in enumerate(clips, 1):
            duration = clip['end'] - clip['start']
            print(f"{'=' * 70}")
            print(f"🎥 CLIP {i}")
            print(f"{'=' * 70}")
            print(f"⏱️  Timing: {clip['start']:.2f}s → {clip['end']:.2f}s ({duration:.1f}s)")
            print(f"🎣 Hook: {clip['viral_hook_text']}")
            print(f"📺 YouTube: {clip['video_title_for_youtube_short']}")
            print(f"🎵 TikTok: {clip['video_description_for_tiktok']}")
            print(f"📸 Instagram: {clip['video_description_for_instagram']}")
            print()
        
        # Validate clips
        print(f"{'=' * 70}")
        print("🔬 VALIDATION")
        print(f"{'=' * 70}")
        
        all_valid = True
        for i, clip in enumerate(clips, 1):
            duration = clip['end'] - clip['start']
            
            # Check duration
            if not (15 <= duration <= 60):
                print(f"❌ Clip {i}: Duration {duration:.1f}s not in 15-60s range")
                all_valid = False
            
            # Check bounds
            if clip['start'] < 0 or clip['end'] > video_duration:
                print(f"❌ Clip {i}: Timestamps out of bounds")
                all_valid = False
            
            # Check hook length
            hook_words = len(clip['viral_hook_text'].split())
            if hook_words > 10:
                print(f"⚠️  Clip {i}: Hook has {hook_words} words (max 10)")
            
            # Check required fields
            required = [
                'start', 'end', 'viral_hook_text',
                'video_title_for_youtube_short',
                'video_description_for_tiktok',
                'video_description_for_instagram'
            ]
            missing = [f for f in required if f not in clip]
            if missing:
                print(f"❌ Clip {i}: Missing fields: {missing}")
                all_valid = False
        
        if all_valid:
            print("✅ All clips passed validation!")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_with_json_transcript():
    """Test with actual JSON transcript file if available."""
    
    print("\n" + "=" * 70)
    print("🧪 TEST 2: Real Transcript File (if available)")
    print("=" * 70)
    
    # Look for the sample transcript
    transcript_file = "better_than_ozempic_transcript.json"
    
    if not os.path.exists(transcript_file):
        print(f"⏭️  Skipping - {transcript_file} not found")
        return None
    
    print(f"\n📂 Loading: {transcript_file}")
    
    try:
        with open(transcript_file, 'r', encoding='utf-8') as f:
            transcript = json.load(f)
        
        # Get duration from last segment
        video_duration = transcript['segments'][-1]['end'] if transcript['segments'] else 0
        
        print(f"📊 Video Duration: {video_duration:.1f}s ({video_duration/60:.1f} min)")
        print(f"📝 Transcript Length: {len(transcript['text'])} characters")
        print(f"🌍 Language: {transcript['language']}")
        
        print("\n🔍 Calling Gemini API to detect viral moments...")
        print("⏳ This may take 10-30 seconds...")
        
        clips = detect_viral_clips(transcript, video_duration)
        
        print(f"\n✅ SUCCESS! Found {len(clips)} viral clips\n")
        
        for i, clip in enumerate(clips, 1):
            duration = clip['end'] - clip['start']
            print(f"🎥 Clip {i}: {clip['start']:.1f}s → {clip['end']:.1f}s ({duration:.1f}s)")
            print(f"   🎣 {clip['viral_hook_text']}")
            print()
        
        # Save results
        output_file = transcript_file.replace('.json', '_viral_clips.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump({
                'source_file': transcript_file,
                'video_duration': video_duration,
                'language': transcript['language'],
                'num_clips': len(clips),
                'clips': clips
            }, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_api_connection():
    """Test basic Gemini API connection."""
    
    print("\n" + "=" * 70)
    print("🧪 TEST 0: Gemini API Connection")
    print("=" * 70)
    
    try:
        print("\n🔑 Checking API key...")
        detector = ViralDetector()
        
        if detector.api_key and detector.api_key.startswith('AIza'):
            print("✅ API key found and looks valid")
            print(f"🤖 Using model: {detector.model}")
            return True
        else:
            print("❌ API key invalid or missing")
            return False
            
    except Exception as e:
        print(f"❌ Failed to initialize: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "🚀" * 35)
    print("STAGE 1.2 TEST SUITE: VIRAL CLIP DETECTION (Google Gemini)")
    print("🚀" * 35)
    
    # Test 0: API Connection
    if not test_api_connection():
        print("\n⚠️  Cannot proceed without valid API key")
        print("💡 Make sure your .env file contains GEMINI_API_KEY")
        exit(1)
    
    # Test 1: Sample transcript
    test1_passed = test_with_sample_transcript()
    
    # Test 2: Real transcript (if available)
    test2_result = test_with_json_transcript()
    
    # Summary
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    print(f"Test 1 (Sample Transcript): {'✅ PASSED' if test1_passed else '❌ FAILED'}")
    if test2_result is not None:
        print(f"Test 2 (Real Transcript):   {'✅ PASSED' if test2_result else '❌ FAILED'}")
    else:
        print(f"Test 2 (Real Transcript):   ⏭️  SKIPPED")
    
    print("\n" + "=" * 70)
    
    if test1_passed:
        print("🎉 Stage 1.2 is working correctly!")
        print("\n📝 Next steps:")
        print("   1. Test with actual video files")
        print("   2. Proceed to Stage 2.1 (Clip Extraction)")
    else:
        print("❌ Some tests failed. Please review the errors above.")
    
    print("=" * 70)
