---
name: remotion
description: "Remotion video creation best practices and domain knowledge. React-based programmatic video framework. Covers animations (useCurrentFrame, interpolate, spring), compositions, sequencing, timing, audio/video embedding, captions/subtitles, 3D (Three.js), charts, fonts, TailwindCSS, transitions, FFmpeg, Lottie, maps (Mapbox), voiceover (ElevenLabs TTS), light leaks, transparent video, text animations, audio visualization, and asset management. Use when writing or reviewing Remotion code."
metadata:
  tags: remotion, video, react, animation, composition, programmatic-video
---

# Remotion - Video Creation in React

Best practices and domain-specific knowledge for building video compositions with Remotion.

<args>$ARGUMENTS</args>

## When to Use

This skill should be invoked when:

- Writing or modifying Remotion video compositions
- Creating animations with `useCurrentFrame()` and `interpolate()`
- Working with `<Composition>`, `<Sequence>`, `<Series>` components
- Embedding audio, video, images, or GIFs in Remotion
- Adding captions, subtitles, or voiceover
- Using transitions between scenes
- Working with 3D content (Three.js) in Remotion
- Building charts or data visualizations for video
- Using FFmpeg operations within Remotion projects
- Handling fonts, TailwindCSS, or text animations
- Rendering transparent videos or light leak effects
- Measuring text or DOM nodes in video compositions

## Critical Rules

1. **Never use CSS animations** - Always use `useCurrentFrame()` for all animations
2. **Never use HTML `<img>`** - Always use Remotion's `<Img>` component
3. **Never use HTML `<video>` or `<audio>`** - Use Remotion's `<Video>` and `<Audio>` components
4. **Spring animations** - Use `spring()` from `remotion` for natural motion, not CSS transitions
5. **Static files** - Use `staticFile()` for assets in the `public/` folder

## Domain Knowledge Files

Load relevant rule files based on the task:

### Core Animation & Composition
- [rules/animations.md](rules/animations.md) - `useCurrentFrame()`, frame-based animation patterns
- [rules/timing.md](rules/timing.md) - `interpolate()`, `spring()`, easing functions
- [rules/compositions.md](rules/compositions.md) - `<Composition>`, stills, folders, default props
- [rules/sequencing.md](rules/sequencing.md) - `<Sequence>`, `<Series>`, timing control
- [rules/trimming.md](rules/trimming.md) - Cutting animation start/end points

### Media
- [rules/audio.md](rules/audio.md) - Audio playback, trimming, volume, speed, pitch
- [rules/videos.md](rules/videos.md) - Video embedding, trimming, volume, speed, looping
- [rules/images.md](rules/images.md) - `<Img>` component
- [rules/gifs.md](rules/gifs.md) - Animated GIF/APNG/AVIF/WebP display
- [rules/assets.md](rules/assets.md) - `staticFile()` asset management

### Captions & Subtitles
- [rules/subtitles.md](rules/subtitles.md) - Caption JSON format specification
- [rules/display-captions.md](rules/display-captions.md) - Rendering captions with word highlighting
- [rules/transcribe-captions.md](rules/transcribe-captions.md) - Audio transcription (Whisper.cpp)
- [rules/import-srt-captions.md](rules/import-srt-captions.md) - Importing .srt files

### Visual Effects & Transitions
- [rules/transitions.md](rules/transitions.md) - `<TransitionSeries>`, scene transitions
- [rules/text-animations.md](rules/text-animations.md) - Typewriter, text highlighting
- [rules/light-leaks.md](rules/light-leaks.md) - WebGL light leak overlays
- [rules/transparent-videos.md](rules/transparent-videos.md) - Alpha channel rendering (ProRes, VP9)
- [rules/lottie.md](rules/lottie.md) - Lottie animation embedding

### Audio Features
- [rules/audio-visualization.md](rules/audio-visualization.md) - Spectrum bars, waveforms, bass-reactive
- [rules/sfx.md](rules/sfx.md) - Sound effects library
- [rules/voiceover.md](rules/voiceover.md) - ElevenLabs TTS voiceover

### Styling & Fonts
- [rules/fonts.md](rules/fonts.md) - Google Fonts, local font loading
- [rules/tailwind.md](rules/tailwind.md) - TailwindCSS (with animation restrictions)

### Data & Charts
- [rules/charts.md](rules/charts.md) - Bar, pie, line, stock chart patterns
- [rules/3d.md](rules/3d.md) - Three.js / React Three Fiber with `<ThreeCanvas>`
- [rules/maps.md](rules/maps.md) - Mapbox map animations

### Measurement & Metadata
- [rules/measuring-text.md](rules/measuring-text.md) - Text dimension measurement, fitting
- [rules/measuring-dom-nodes.md](rules/measuring-dom-nodes.md) - DOM measurement with scale correction
- [rules/calculate-metadata.md](rules/calculate-metadata.md) - Dynamic duration, dimensions, props
- [rules/parameters.md](rules/parameters.md) - Zod schema parametrization
- [rules/get-video-duration.md](rules/get-video-duration.md) - Video duration extraction
- [rules/get-video-dimensions.md](rules/get-video-dimensions.md) - Video dimensions extraction
- [rules/get-audio-duration.md](rules/get-audio-duration.md) - Audio duration extraction
- [rules/extract-frames.md](rules/extract-frames.md) - Frame extraction at timestamps
- [rules/can-decode.md](rules/can-decode.md) - Codec compatibility checking

### Video Processing
- [rules/ffmpeg.md](rules/ffmpeg.md) - FFmpeg/FFprobe operations

## Quick Reference

### Basic Animation Pattern
```tsx
import { useCurrentFrame, interpolate } from "remotion";

const MyComp: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 30], [0, 1], {
    extrapolateRight: "clamp",
  });
  return <div style={{ opacity }}>Hello</div>;
};
```

### Spring Animation
```tsx
import { useCurrentFrame, useVideoConfig, spring } from "remotion";

const scale = spring({
  frame,
  fps,
  config: { damping: 200 },
});
```

### Composition Setup
```tsx
import { Composition } from "remotion";

<Composition
  id="MyVideo"
  component={MyComp}
  durationInFrames={150}
  fps={30}
  width={1920}
  height={1080}
/>
```
