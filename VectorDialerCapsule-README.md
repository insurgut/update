# VectorDialerCapsule

Experimental Vector / Xposed module for Google Phone v244.

The repository branch includes the complete Android Gradle project packed as `VectorDialerCapsule-sources.tar.gz` and an Actions workflow that extracts the sources and produces a debug APK. The original Google Phone is not repackaged.

**Limitations:** Compose accessibility lookup depends on OS restrictions; on Android 17 the grouped buttons might not appear. The APK is not device-tested. The module does not suppress call-recording notifications or warnings.

To install: download the GitHub Actions artifact, extract its `app-debug.apk`, install it, enable it for `com.google.android.dialer` in Vector, and restart the Google Phone process.
