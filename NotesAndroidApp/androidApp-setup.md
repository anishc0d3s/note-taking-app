# Building Android App from VS Code

## Project Structure

Create this folder structure:

```
NotesAndroidApp/
├── app/
│   ├── src/
│   │   └── main/
│   │       ├── java/
│   │       │   └── com/
│   │       │       └── notesapp/
│   │       │           └── myapp/
│   │       │               └── MainActivity.java
│   │       ├── res/
│   │       │   ├── layout/
│   │       │   │   └── activity_main.xml
│   │       │   ├── mipmap-hdpi/
│   │       │   ├── mipmap-mdpi/
│   │       │   ├── mipmap-xhdpi/
│   │       │   ├── mipmap-xxhdpi/
│   │       │   └── mipmap-xxxhdpi/
│   │       └── AndroidManifest.xml
│   └── build.gradle
├── build.gradle
├── settings.gradle
└── gradle.properties
```

## Step 1: Install Prerequisites

### 1. Install Java JDK 17
```bash
# Ubuntu/Debian
sudo apt install openjdk-17-jdk

# macOS
brew install openjdk@17

# Windows
# Download from: https://www.oracle.com/java/technologies/downloads/
```

### 2. Install Android Command Line Tools

**Download SDK Command Line Tools:**
- Visit: https://developer.android.com/studio#command-tools
- Download "Command line tools only"
- Extract to a folder (e.g., `~/Android/cmdline-tools`)

**Set up environment variables:**

```bash
# Add to ~/.bashrc or ~/.zshrc (Linux/Mac)
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/build-tools/33.0.0

# Windows (System Environment Variables)
ANDROID_HOME=C:\Users\YourName\AppData\Local\Android\Sdk
Path=%Path%;%ANDROID_HOME%\cmdline-tools\latest\bin
```

### 3. Install SDK packages

```bash
# Accept licenses
sdkmanager --licenses

# Install required packages
sdkmanager "platform-tools" "platforms;android-33" "build-tools;33.0.0"
```

## Step 2: Create Project Files

### 1. Create settings.gradle
```gradle
rootProject.name = "NotesAndroidApp"
include ':app'
```

### 2. Create gradle.properties
```properties
org.gradle.jvmargs=-Xmx2048m -Dfile.encoding=UTF-8
android.useAndroidX=true
android.enableJetifier=true
```

### 3. Copy all the artifact files to their locations:
- `AndroidManifest.xml` → `app/src/main/AndroidManifest.xml`
- `MainActivity.java` → `app/src/main/java/com/notesapp/myapp/MainActivity.java`
- `activity_main.xml` → `app/src/main/res/layout/activity_main.xml`
- `build.gradle (app)` → `app/build.gradle`
- `build.gradle (root)` → `build.gradle` (root folder)

## Step 3: Configure Server URL

**Edit MainActivity.java:**
```java
private static final String SERVER_URL = "http://YOUR_IP:5001";
```

**Find your IP address:**
```bash
# Linux/Mac
ifconfig | grep "inet "

# Windows
ipconfig

# Look for something like: 192.168.1.100
```

**Start your Flask server:**
```bash
python app.py
```

## Step 4: Build the APK

### Method 1: Using Gradle Wrapper (Recommended)

```bash
# Navigate to project folder
cd NotesAndroidApp

# Make gradlew executable (Linux/Mac)
chmod +x gradlew

# Build debug APK
./gradlew assembleDebug

# Windows
gradlew.bat assembleDebug
```

**APK location:** `app/build/outputs/apk/debug/app-debug.apk`

### Method 2: Using Gradle directly

```bash
gradle assembleDebug
```

## Step 5: Install APK on Device

### Option A: USB Connection

```bash
# Enable USB debugging on phone (Settings → Developer Options)

# Connect phone via USB

# Check device is connected
adb devices

# Install APK
adb install app/build/outputs/apk/debug/app-debug.apk
```

### Option B: Transfer APK to phone
1. Copy `app-debug.apk` to your phone
2. Open file on phone and install
3. Enable "Install from Unknown Sources" if prompted

## VS Code Extensions (Optional)

Install these for better development experience:
- **Android iOS Emulator** by DiemasMichiels
- **Gradle for Java** by Microsoft
- **Java Extension Pack** by Microsoft

## Troubleshooting

### Error: "SDK location not found"
Create `local.properties` in root:
```properties
sdk.dir=/path/to/Android/Sdk
```

### Error: "Gradle wrapper not found"
Download wrapper:
```bash
gradle wrapper
```

### Can't connect to Flask server
1. Make sure Flask is running
2. Use correct IP (not localhost/127.0.0.1)
3. Check firewall allows port 5000
4. Both devices on same WiFi network

### App crashes on open
Check logcat:
```bash
adb logcat | grep NotesApp
```

## Quick Commands Reference

```bash
# Install Java 17
brew install --cask temurin17

# Use it temporarily

# Set JAVA_HOME to your Temurin 17
export JAVA_HOME=/Library/Java/JavaVirtualMachines/temurin-17.jdk/Contents/Home
export PATH="$JAVA_HOME/bin:$PATH"

# Verify
java -version
# Should show: openjdk version "17.x.x"

### Create wrapper files
gradle wrapper --gradle-version 8.5

# Build debug APK
./gradlew assembleDebug

# Build release APK
./gradlew assembleRelease

# Clean build
./gradlew clean

# Install on connected device
./gradlew installDebug

# View all tasks
./gradlew tasks

# Check for connected devices
adb devices

# View logs
adb logcat

# Uninstall app
adb uninstall com.notesapp.myapp
```

## Testing

1. Start Flask server on your computer:
   ```bash
   python app.py
   ```

2. Note your computer's IP address

3. Update `SERVER_URL` in MainActivity.java

4. Build and install APK

5. Open app on phone (must be on same network)

## Production Deployment

For production, host your Flask backend on a cloud service:
- **Heroku**: `heroku create && git push heroku main`
- **PythonAnywhere**: Upload files via web interface
- **Render**: Connect GitHub repo
- **Railway**: `railway up`

Then update `SERVER_URL` to your hosted URL and rebuild APK.


### KNOWN Issue

- Android App Not Building
