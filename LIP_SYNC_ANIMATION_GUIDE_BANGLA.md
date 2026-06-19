# JARVIS Lip Sync Animation Guide (কথা বলার ভঙ্গি)

## 🎭 Shape Keys কী?

Shape Keys হলো Blender এর একটি feature যেটা দিয়ে mesh এর shape পরিবর্তন করা যায় animation এর জন্য। এটা দিয়ে realistic lip sync (কথা বলার ভঙ্গি) তৈরি করা যায়।

---

## 📝 আপনার JARVIS Face এ যে Shape Keys আছে:

Script automatically ৭টি shape keys তৈরি করেছে:

### 1. **A_Open** (আ)
- **ব্যবহার:** Open vowel sounds
- **উদাহরণ:** "আমি", "কথা", "বলা"
- **Effect:** Mouth opens wide, jaw drops

### 2. **E_Smile** (ই)
- **ব্যবহার:** Smile/wide sounds
- **উদাহরণ:** "ই", "কী", "দিন"
- **Effect:** Lips stretch horizontally

### 3. **O_Round** (ও)
- **ব্যবহার:** Round vowel sounds
- **উদাহরণ:** "ও", "কোথা", "বলো"
- **Effect:** Lips form circle, forward

### 4. **U_Pucker** (উ)
- **ব্যবহার:** Pucker sounds
- **উদাহরণ:** "উ", "তুমি", "সুন্দর"
- **Effect:** Lips pucker forward

### 5. **M_Closed** (ম)
- **ব্যবহার:** Closed consonants
- **উদাহরণ:** "ম", "ন", "ব"
- **Effect:** Lips closed

### 6. **F_Teeth** (ফ)
- **ব্যবহার:** Teeth on lip sounds
- **উদাহরণ:** "ফ", "ভ"
- **Effect:** Upper teeth touch lower lip

### 7. **S_Teeth** (স)
- **ব্যবহার:** Teeth showing sounds
- **উদাহরণ:** "স", "শ", "ষ"
- **Effect:** Slight smile with teeth

---

## 🎬 Shape Keys কিভাবে Use করবেন

### Method 1: Manual Control (Testing)

1. **Head object select করুন**
2. Right panel এ **Object Data Properties** (green triangle icon) click করুন
3. **Shape Keys** section দেখবেন
4. প্রতিটি shape key এর পাশে একটি **Value slider** (0.000 - 1.000) আছে
5. Slider move করে effect দেখুন:
   - **0.000** = No effect (normal face)
   - **1.000** = Full effect (maximum shape)

**Test করুন:**
```
A_Open: 0.000 → 1.000 (mouth opens)
E_Smile: 0.000 → 1.000 (smile)
O_Round: 0.000 → 1.000 (round lips)
```

### Method 2: Keyframe Animation (Actual Lip Sync)

#### Step 1: Timeline Setup

1. Bottom panel এ **Timeline** দেখবেন
2. **End frame** set করুন (উদাহরণ: 120 frames = 5 seconds at 24fps)

#### Step 2: Create Keyframes

**Example: "আমি JARVIS" বলার animation**

**Frame 1-10: "আ"**
1. Timeline এ **frame 1** এ যান
2. Head select করুন
3. Shape Keys এ **A_Open** value = **1.0** set করুন
4. **A_Open** এর উপর **right-click** → **Insert Keyframe**
5. Frame 10 এ যান
6. A_Open value = **0.0** set করুন
7. Right-click → Insert Keyframe

**Frame 10-20: "মি"**
1. Frame 10 এ **M_Closed** = **1.0** → Insert Keyframe
2. Frame 15 এ M_Closed = **0.0**, **E_Smile** = **0.8** → Insert Keyframe
3. Frame 20 এ E_Smile = **0.0** → Insert Keyframe

**Frame 30-50: "JARVIS"**
- Continue করুন প্রতিটি sound এর জন্য

#### Step 3: Play Animation

1. **Spacebar** press করুন
2. Animation play হবে
3. Adjust করুন যদি দরকার হয়

---

## 🎯 Phoneme Mapping (Bengali)

### Vowels (স্বরবর্ণ):

| Sound | Shape Key | Value | Example |
|-------|-----------|-------|---------|
| আ | A_Open | 1.0 | আমি |
| ই/ঈ | E_Smile | 0.8 | কী |
| উ/ঊ | U_Pucker | 1.0 | তুমি |
| এ | E_Smile | 0.6 | এখন |
| ও | O_Round | 1.0 | ওখানে |

### Consonants (ব্যঞ্জনবর্ণ):

| Sound | Shape Key | Value | Example |
|-------|-----------|-------|---------|
| ক/খ/গ/ঘ | A_Open | 0.5 | কথা |
| চ/ছ/জ/ঝ | E_Smile | 0.4 | জানি |
| ট/ঠ/ড/ঢ | A_Open | 0.4 | টাকা |
| ত/থ/দ/ধ | S_Teeth | 0.6 | তুমি |
| প/ফ/ব/ভ | M_Closed | 1.0 | বলা |
| ম | M_Closed | 1.0 | আমি |
| য/র/ল | A_Open | 0.3 | যাও |
| শ/ষ/স | S_Teeth | 0.8 | সুন্দর |
| হ | A_Open | 0.6 | হ্যাঁ |

---

## 🎨 Advanced: Blend Multiple Shape Keys

একসাথে multiple shape keys use করে আরও realistic effect পাবেন:

**Example: "বলো" (bolo)**

**"ব" sound:**
- M_Closed = 1.0 (lips closed)

**"ও" sound:**
- M_Closed = 0.0 (release)
- O_Round = 1.0 (round lips)
- A_Open = 0.3 (slight jaw drop)

**Transition:**
- Frame 1: M_Closed = 1.0
- Frame 5: M_Closed = 0.5, O_Round = 0.5
- Frame 10: M_Closed = 0.0, O_Round = 1.0, A_Open = 0.3

---

## 🤖 Automatic Lip Sync (Python Script)

আপনি Python script দিয়ে automatic lip sync তৈরি করতে পারেন:

```python
import bpy

def animate_phoneme(obj, shape_key_name, start_frame, end_frame, max_value=1.0):
    """Animate a single phoneme"""
    shape_key = obj.data.shape_keys.key_blocks[shape_key_name]
    
    # Start
    bpy.context.scene.frame_set(start_frame)
    shape_key.value = 0.0
    shape_key.keyframe_insert(data_path="value")
    
    # Peak
    mid_frame = (start_frame + end_frame) // 2
    bpy.context.scene.frame_set(mid_frame)
    shape_key.value = max_value
    shape_key.keyframe_insert(data_path="value")
    
    # End
    bpy.context.scene.frame_set(end_frame)
    shape_key.value = 0.0
    shape_key.keyframe_insert(data_path="value")

# Example usage
head = bpy.data.objects['JARVIS_Head']

# "আমি" animation
animate_phoneme(head, 'A_Open', 1, 10, 1.0)      # আ
animate_phoneme(head, 'M_Closed', 10, 15, 1.0)  # ম
animate_phoneme(head, 'E_Smile', 15, 25, 0.8)   # ই
```

---

## 🎬 Complete Example: "Hello JARVIS"

```python
import bpy

head = bpy.data.objects['JARVIS_Head']

# H - open
animate_phoneme(head, 'A_Open', 1, 8, 0.6)

# E - smile
animate_phoneme(head, 'E_Smile', 8, 15, 0.8)

# L - teeth
animate_phoneme(head, 'S_Teeth', 15, 22, 0.6)

# O - round
animate_phoneme(head, 'O_Round', 22, 32, 1.0)

# (pause)

# J - slight open
animate_phoneme(head, 'A_Open', 40, 47, 0.4)

# A - open
animate_phoneme(head, 'A_Open', 47, 55, 1.0)

# R - slight open
animate_phoneme(head, 'A_Open', 55, 62, 0.5)

# V - teeth on lip
animate_phoneme(head, 'F_Teeth', 62, 69, 0.8)

# I - smile
animate_phoneme(head, 'E_Smile', 69, 77, 0.8)

# S - teeth
animate_phoneme(head, 'S_Teeth', 77, 85, 0.8)
```

---

## 🎯 Tips for Realistic Lip Sync

### 1. **Timing is Key**
- প্রতিটি phoneme 5-10 frames (0.2-0.4 seconds)
- Fast speech: 5 frames
- Slow speech: 10 frames

### 2. **Overlap Shapes**
- একটি shape শেষ হওয়ার আগেই পরেরটা শুরু করুন
- Natural transition এর জন্য

### 3. **Vary Intensity**
- সব shape key 1.0 use করবেন না
- 0.3 - 1.0 range এ vary করুন

### 4. **Add Micro-movements**
- Slight jaw movement
- Head nods
- Eye blinks

### 5. **Match Audio**
- যদি audio file থাকে, তাহলে waveform দেখে sync করুন
- Blender এ: Video Sequencer → Add → Sound

---

## 🔧 Troubleshooting

### সমস্যা ১: Shape Keys দেখা যাচ্ছে না

**সমাধান:**
- নিশ্চিত করুন Head object selected আছে
- Object Data Properties (green triangle) check করুন
- যদি না থাকে, script আবার run করুন

### সমস্যা ২: Animation smooth না

**সমাধান:**
- Graph Editor open করুন (top: Animation → Graph Editor)
- Keyframes select করুন
- Press **T** → **Bezier** (smooth curves)

### সমস্যা ৩: Multiple shapes একসাথে active

**সমাধান:**
- এটা normal! Multiple shapes blend করা যায়
- শুধু নিশ্চিত করুন total value 1.0 এর বেশি না হয়

### সমস্যা ৪: Export করার পর shape keys কাজ করছে না

**সমাধান:**
- Export settings এ **Shape Keys** checked আছে কিনা check করুন
- GLB format shape keys support করে
- JARVIS panel এ shape key animation code দরকার হবে

---

## 📊 Shape Key Values Reference

### Quick Reference Table:

| Mouth Position | A_Open | E_Smile | O_Round | U_Pucker | M_Closed | F_Teeth | S_Teeth |
|----------------|--------|---------|---------|----------|----------|---------|---------|
| Neutral | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| "আ" | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| "ই" | 0.0 | 0.8 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| "ও" | 0.3 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| "উ" | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 |
| "ম" | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 |
| "ফ" | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 |
| "স" | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.8 |

---

## 🎓 Learning Resources

### Practice Sentences (Bengali):

1. **"আমি JARVIS"** - Simple, 3 phonemes
2. **"তুমি কেমন আছো"** - Medium, varied sounds
3. **"সুপ্রভাত, আজ কী করবেন"** - Complex, long sentence

### Practice Sentences (English):

1. **"Hello"** - Simple
2. **"How are you"** - Medium
3. **"Welcome to JARVIS"** - Complex

---

## ✨ Final Tips

1. **Start Simple:** একটা ছোট word দিয়ে practice করুন
2. **Watch References:** Real people এর lip movement observe করুন
3. **Iterate:** First attempt perfect হবে না, refine করতে থাকুন
4. **Use Audio:** Audio file sync করলে সবচেয়ে ভালো result
5. **Exaggerate:** Animation এ slightly exaggerate করুন, realistic দেখাবে

---

**সম্পন্ন!** এখন আপনি JARVIS কে কথা বলাতে পারবেন realistic lip sync দিয়ে! 🎉

কোনো প্রশ্ন থাকলে জানাবেন!
