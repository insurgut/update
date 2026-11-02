#!/usr/bin/env python3
from pathlib import Path

root = Path("VectorDialerCapsule")
source = root / "app/src/main/java/ru/lisurgut/dialercapsule/MainHook.java"
text = source.read_text()
text = text.replace("import de.robv.android.xposed.XposedHelpers;\n", "")
for method in ("onPause", "onDestroy", "onResume"):
    old = f'XposedHelpers.findAndHookMethod(Activity.class, "{method}", new XC_MethodHook() {{'
    new = f'hookLifecycle("{method}", new XC_MethodHook() {{'
    if old not in text:
        raise RuntimeError(f"Could not find {method} hook to update")
    text = text.replace(old, new)
anchor = "    static final class Target {"
replacement = '''    private static void hookLifecycle(String name, XC_MethodHook callback) {
        try {
            Method method = Activity.class.getDeclaredMethod(name);
            XposedBridge.hookMethod(method, callback);
            XposedBridge.log("DialerCapsule: hooked Activity." + name);
        } catch (Throwable error) {
            XposedBridge.log("DialerCapsule: unable to hook Activity." + name + ": " + error);
        }
    }

    static final class Target {'''
if anchor not in text:
    raise RuntimeError("Cannot locate insertion point")
text = text.replace(anchor, replacement, 1)
source.write_text(text)
stub = root / "xposed-stubs/src/main/java/de/robv/android/xposed"
(stub / "XC_MethodHook.java").write_text(
    (stub / "XC_MethodHook.java").read_text().replace(
        "public abstract class XC_MethodHook {",
        "public abstract class XC_MethodHook {\n    public class Unhook {}"
    )
)
(stub / "XposedBridge.java").write_text("""package de.robv.android.xposed;
import java.lang.reflect.Member;
public final class XposedBridge {
    public static void log(String text) {}
    public static XC_MethodHook.Unhook hookMethod(Member method, XC_MethodHook callback) { return null; }
}
""")
(stub / "XposedHelpers.java").write_text("""package de.robv.android.xposed;
public final class XposedHelpers {
    public static XC_MethodHook.Unhook findAndHookMethod(Class<?> clazz, String name, Object... parametersAndCallback) { return null; }
}
""")
gradle = root / "app/build.gradle"
content = gradle.read_text()
if "versionCode 1; versionName '1.0'" not in content:
    raise RuntimeError("Unexpected version in Gradle config")
gradle.write_text(content.replace("versionCode 1; versionName '1.0'", "versionCode 2; versionName '1.1'"))
print("Vector compatibility patch applied: 1.1")
