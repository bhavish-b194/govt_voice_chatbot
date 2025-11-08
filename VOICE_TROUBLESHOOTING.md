# 🎤 Voice Input Troubleshooting Guide

## 🚨 **Common Issue: "No speech detected"**

If you're getting "No speech detected" errors, here's how to fix it:

### ✅ **Step 1: Check Browser Compatibility**
- **✅ Supported**: Chrome, Edge, Safari
- **❌ Not supported**: Firefox (limited support), Internet Explorer
- **💡 Recommendation**: Use Google Chrome for best results

### ✅ **Step 2: Check Microphone Permissions**
1. Look for a microphone icon in your browser's address bar
2. Click it and select "Always allow" 
3. If you don't see the icon:
   - Go to browser Settings → Privacy & Security → Site Settings → Microphone
   - Find localhost:8000 and set to "Allow"
4. Refresh the page after changing permissions

### ✅ **Step 3: Test Your Microphone**
1. Click the **"Test Microphone"** button on the page
2. Allow microphone access when prompted
3. If test fails:
   - Check if microphone is connected
   - Try a different microphone
   - Check Windows sound settings

### ✅ **Step 4: Proper Voice Input Technique**
1. Click **"CLICK & SPEAK"**
2. Wait for **"🔴 Recording started - speak now!"**
3. Speak **immediately** and **clearly**
4. Speak for **2-5 seconds** minimum
5. Don't speak too quietly or too loudly

### ✅ **Step 5: Environment Check**
- **Quiet environment**: Reduce background noise
- **Clear speech**: Speak distinctly
- **Proper distance**: 6-12 inches from microphone
- **No interruptions**: Don't speak over system sounds

## 🔧 **Advanced Troubleshooting**

### **Issue: Microphone Access Denied**
```
❌ Microphone access denied
```
**Solution:**
1. Clear browser data for localhost:8000
2. Restart browser
3. Visit http://localhost:8000 again
4. Allow microphone when prompted

### **Issue: Audio Capture Error**
```
❌ Audio capture error
```
**Solution:**
1. Close other applications using microphone (Zoom, Teams, etc.)
2. Restart browser
3. Try again

### **Issue: Network Error**
```
❌ Network error
```
**Solution:**
1. Check internet connection
2. Web Speech API requires internet
3. Try refreshing the page

## 🎯 **Best Practices for Voice Input**

### **✅ DO:**
- Speak clearly and at normal pace
- Wait for "Recording started" message
- Use simple, direct questions
- Speak in a quiet environment
- Allow microphone permissions

### **❌ DON'T:**
- Speak too fast or too slow
- Whisper or shout
- Speak in noisy environments
- Use complex, long sentences
- Interrupt the recording process

## 🔄 **Alternative: Use Text Input**

If voice input continues to have issues:

1. **Use the text input box** below the voice button
2. **Click sample question buttons** to test functionality
3. **Type your questions** like:
   - "What are agriculture schemes?"
   - "Tell me about health schemes"
   - "How to apply for education schemes?"

## 🛠️ **Technical Details**

### **How Voice Input Works:**
1. **Web Speech API** (browser-based speech recognition)
2. **Real-time processing** (no server upload needed)
3. **Multi-language support** (9 Indian languages)
4. **Instant results** (no waiting for processing)

### **System Requirements:**
- **Browser**: Chrome 25+, Edge 79+, Safari 14.1+
- **Internet**: Required for Web Speech API
- **Microphone**: Any working microphone
- **Permissions**: Microphone access allowed

## 📞 **Still Having Issues?**

If voice input still doesn't work after trying all steps:

1. **Use text input** - it has the same functionality
2. **Try a different browser** (preferably Chrome)
3. **Check Windows microphone settings**
4. **Test microphone in other applications**
5. **Restart your computer** if all else fails

## ✅ **Success Indicators**

You'll know voice input is working when you see:
- ✅ "🔴 Recording started - speak now!"
- ✅ "Hearing: [your speech in real-time]"
- ✅ "You said: [final recognized text]"
- ✅ "Confidence: [percentage]%"
- ✅ Bot response with scheme information

---

**💡 Remember**: The text input works exactly the same as voice input, so you can always use that as a reliable alternative!
