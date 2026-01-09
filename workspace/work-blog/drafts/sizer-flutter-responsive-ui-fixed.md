# Flutter sizer Package: Build Responsive UI the Easy Way

Hey, I'm woogi, and today I want to share one of my favorite Flutter packages for building responsive UIs - the **sizer** package.

Have you ever found yourself writing `MediaQuery.of(context).size.width * 0.5` over and over again? I've been there. It's verbose, repetitive, and honestly, it just clutters up your code. What if I told you there's a much simpler way?

With the sizer package, you can just write `50.w` to get 50% of the screen width. That's it. Clean, readable, and intuitive.

In this guide, I'll walk you through everything you need to know about sizer - from installation to real-world usage. Let's dive in!

---

## What is the sizer package?

[sizer](https://pub.dev/packages/sizer) is a Flutter package that makes responsive UI development a breeze. With over 160,000 weekly downloads and 1.8k likes on pub.dev, it's become a go-to choice for many Flutter developers.

### Key Features

- **Simple API**: Intuitive extensions like `.h`, `.w`, `.sp`
- **Multi-platform support**: Works on Android, iOS, Web, and Desktop
- **Device detection**: Automatic mobile/tablet/desktop and orientation detection
- **SafeArea support**: Built-in extensions for safe area calculations
- **Zero dependencies**: No external dependencies beyond Flutter

> Current version: 3.1.3 | License: MIT | Publisher: technoprashant.me (verified)

---

## Installation and Setup

### Step 1: Add the package

Add sizer to your `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  sizer: ^3.1.3
```

Then run:

```bash
flutter pub get
```

### Step 2: Wrap your app with Sizer

In your `main.dart`, wrap your `MaterialApp` with the `Sizer` widget:

```dart
import 'package:flutter/material.dart';
import 'package:sizer/sizer.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return Sizer(
      builder: (context, orientation, screenType) {
        return MaterialApp(
          title: 'Sizer Demo',
          theme: ThemeData(
            primarySwatch: Colors.blue,
          ),
          home: const HomePage(),
        );
      },
    );
  }
}
```

The `Sizer` widget's builder callback gives you three useful pieces of information:

- `context`: The BuildContext
- `orientation`: Current screen orientation (portrait/landscape)
- `screenType`: Device type (mobile/tablet/desktop)

### Step 3: Import in your files

To use sizer's extensions, add this import to each file:

```dart
import 'package:sizer/sizer.dart';
```

> **Tip**: IDE auto-import might not work for extension methods, so you'll need to add this import manually.

---

## Core Features

The heart of sizer is its **extension methods** on numeric types. These let you specify sizes as percentages of the screen dimensions.

### Screen-Based Sizing

#### `.h` - Percentage of screen height

```dart
Container(
  height: 30.h,  // 30% of screen height
)
```

#### `.w` - Percentage of screen width

```dart
Container(
  width: 50.w,   // 50% of screen width
)
```

#### Practical example

```dart
Container(
  width: 80.w,       // 80% of screen width
  height: 25.h,      // 25% of screen height
  padding: EdgeInsets.symmetric(
    horizontal: 5.w,  // 5% of screen width
    vertical: 2.h,    // 2% of screen height
  ),
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(2.w),
  ),
  child: Text('Responsive Container'),
)
```

### SafeArea-Aware Sizing

Need to account for notches, status bars, or system UI? Use `.sh` and `.sw`:

```dart
Container(
  height: 30.sh,  // 30% of height excluding SafeArea
  width: 50.sw,   // 50% of width excluding SafeArea
)
```

### Font Sizing

#### `.sp` - Screen-proportional font size

```dart
Text(
  'Hello Flutter!',
  style: TextStyle(fontSize: 16.sp),
)
```

#### `.dp` - Pixel density-based font size

```dart
Text(
  'Hello Flutter!',
  style: TextStyle(fontSize: 16.dp),
)
```

**What's the difference?**

- `.sp`: Considers both screen size and aspect ratio
- `.dp`: Only considers the device's pixel ratio

Generally, use `.sp` for body text and `.dp` for fixed-size elements like icons or labels.

### Extension Reference

| Extension | Description | Example |
|-----------|-------------|---------|
| `.h` | % of screen height | `30.h` = 30% of height |
| `.w` | % of screen width | `50.w` = 50% of width |
| `.sh` | % of SafeArea height | `30.sh` |
| `.sw` | % of SafeArea width | `50.sw` |
| `.sp` | Screen-proportional font | `16.sp` |
| `.dp` | Pixel density-based font | `16.dp` |

---

## Device Detection

Beyond sizing, sizer provides handy device detection features.

### Orientation Detection

```dart
if (Device.orientation == Orientation.portrait) {
  return PortraitLayout();
} else {
  return LandscapeLayout();
}
```

### Screen Type Detection

```dart
if (Device.screenType == ScreenType.mobile) {
  return MobileLayout();
} else if (Device.screenType == ScreenType.tablet) {
  return TabletLayout();
} else {
  return DesktopLayout();
}
```

### Additional Device Info

```dart
// Aspect ratio
double ratio = Device.aspectRatio;

// Pixel density
double pixelRatio = Device.pixelRatio;

// Box constraints
BoxConstraints constraints = Device.boxConstraints;
```

### Customizing Breakpoints

By default, sizer uses 599px as the mobile/tablet threshold. You can customize this:

```dart
Sizer(
  builder: (context, orientation, screenType) {
    return MaterialApp(
      home: HomePage(),
    );
  },
  // maxMobileWidth: 599,  // default
  // maxTabletWidth: 900,  // desktop threshold
)
```

---

## Real-World Example: Responsive Profile Card

Let me show you how sizer works in a real project scenario.

### The ProfileCard Widget

```dart
import 'package:flutter/material.dart';
import 'package:sizer/sizer.dart';

class ProfileCard extends StatelessWidget {
  final String name;
  final String role;
  final String avatarUrl;

  const ProfileCard({
    super.key,
    required this.name,
    required this.role,
    required this.avatarUrl,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      width: Device.screenType == ScreenType.mobile ? 90.w : 45.w,
      padding: EdgeInsets.all(4.w),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(3.w),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 2.w,
            offset: Offset(0, 1.h),
          ),
        ],
      ),
      child: Device.orientation == Orientation.portrait
          ? _buildVerticalLayout()
          : _buildHorizontalLayout(),
    );
  }

  Widget _buildVerticalLayout() {
    return Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        CircleAvatar(
          radius: 15.w,
          backgroundImage: NetworkImage(avatarUrl),
        ),
        SizedBox(height: 2.h),
        Text(
          name,
          style: TextStyle(
            fontSize: 18.sp,
            fontWeight: FontWeight.bold,
          ),
        ),
        SizedBox(height: 0.5.h),
        Text(
          role,
          style: TextStyle(
            fontSize: 14.sp,
            color: Colors.grey[600],
          ),
        ),
      ],
    );
  }

  Widget _buildHorizontalLayout() {
    return Row(
      children: [
        CircleAvatar(
          radius: 10.w,
          backgroundImage: NetworkImage(avatarUrl),
        ),
        SizedBox(width: 4.w),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            mainAxisSize: MainAxisSize.min,
            children: [
              Text(
                name,
                style: TextStyle(
                  fontSize: 16.sp,
                  fontWeight: FontWeight.bold,
                ),
              ),
              Text(
                role,
                style: TextStyle(
                  fontSize: 12.sp,
                  color: Colors.grey[600],
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
```

### Using the Card

```dart
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Sizer Demo',
          style: TextStyle(fontSize: 18.sp),
        ),
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: EdgeInsets.all(4.w),
          child: Column(
            children: [
              ProfileCard(
                name: 'woogi',
                role: 'Flutter Developer',
                avatarUrl: 'https://example.com/avatar.png',
              ),
              SizedBox(height: 3.h),
              Text(
                'Device: ${Device.screenType}',
                style: TextStyle(fontSize: 14.sp),
              ),
              Text(
                'Orientation: ${Device.orientation}',
                style: TextStyle(fontSize: 14.sp),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Key Takeaways from This Example

1. **Adaptive width**: 90% on mobile, 45% on tablet/desktop
2. **Layout switching**: Vertical layout in portrait, horizontal in landscape
3. **Consistent spacing**: All padding and margins are screen-proportional

---

## sizer vs flutter_screenutil

When it comes to responsive UI packages in Flutter, `sizer` and `flutter_screenutil` are the two most popular options. Here's how they compare:

### Comparison Table

| Feature | sizer | flutter_screenutil |
|---------|-------|-------------------|
| **API Complexity** | Simple | More options |
| **Learning Curve** | Low | Medium |
| **Design Size Config** | Not supported | Supported |
| **Community Size** | Medium | Large |
| **Weekly Downloads** | ~160K | ~250K |
| **Advanced Features** | Basic | Advanced scaling |

### The Key Difference: Design Size

The biggest differentiator is **design size configuration**. With flutter_screenutil, you can set a reference design size:

```dart
// flutter_screenutil setup
ScreenUtilInit(
  designSize: const Size(375, 812),  // Designer's artboard size
  builder: (context, child) {
    return MaterialApp(home: HomePage());
  },
);
```

This lets you use exact pixel values from your Figma or Sketch designs.

### Which Should You Choose?

**Choose sizer if:**
- You need quick prototyping
- Working on small or personal projects
- You prefer a simpler API
- You're new to Flutter

**Choose flutter_screenutil if:**
- Collaborating with designers
- Working with a well-defined design system
- Building large-scale team projects
- You need fine-grained customization

---

## Wrapping Up

Today we explored the sizer package - a simple yet powerful tool for building responsive Flutter UIs.

### Quick Recap

1. **Install**: Add `sizer: ^3.1.3` to pubspec.yaml
2. **Setup**: Wrap `MaterialApp` with `Sizer` widget
3. **Use**: Apply `.h`, `.w`, `.sp` extensions for responsive sizing
4. **Detect**: Use `Device.orientation` and `Device.screenType` for adaptive layouts

### Things to Keep in Mind

- IDE auto-import might not work - manually add `import 'package:sizer/sizer.dart';`
- Don't overuse percentages - sometimes fixed values make sense
- Test on extreme aspect ratios (foldables, tablets)

The sizer package is perfect when you want to "just make it responsive" without overthinking. For more complex requirements, consider flutter_screenutil or responsive_framework.

Give sizer a try in your next Flutter project - I think you'll appreciate its simplicity!

---

Hope this helps! Feel free to reach out if you have questions. -- woogi

---

**References:**
- [pub.dev - sizer](https://pub.dev/packages/sizer)
- [GitHub - TechnoPrashant/Sizer](https://github.com/TechnoPrashant/Sizer)
- [Flutter Docs - Adaptive and Responsive Design](https://docs.flutter.dev/ui/adaptive-responsive)
