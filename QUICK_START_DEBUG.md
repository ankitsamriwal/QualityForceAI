# Quick Start & Debugging Guide

## 🚀 Starting the Application

### Step 1: Start Backend

```bash
cd /home/user/QualityForceAI/backend

# Activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (first time only)
pip install -r ../requirements.txt

# Start the backend
python main.py
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

**Test Backend is Running:**
```bash
curl http://localhost:8000/api/health
```

Should return:
```json
{
  "status": "healthy",
  "agents_available": 7,
  "active_executions": 0
}
```

### Step 2: Start Frontend

**In a new terminal:**

```bash
cd /home/user/QualityForceAI/frontend

# Install dependencies (first time only)
npm install

# Start frontend
npm run dev
```

**Expected Output:**
```
VITE v5.0.11  ready in 234 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h to show help
```

### Step 3: Open Browser

1. Open: `http://localhost:5173`
2. Should see the Dashboard
3. Click "Marketplace" in sidebar

---

## 🐛 Debugging "Agent Not Responding"

### Check 1: Is Backend Running?

**Browser Console (F12):**

Look for this error:
```
Failed to fetch agents: AxiosError: Network Error
```

If you see this, **backend is NOT running!**

**Fix:** Start backend (see Step 1 above)

---

### Check 2: Open Browser Console

Press **F12** to open Developer Tools, go to **Console** tab.

You should see:
```
Fetching agents from API...
Agents fetched successfully: Array(7)
```

If you see errors, backend is not reachable.

---

### Check 3: Select an Agent

1. Click on any agent card (it will have blue border)
2. Click "Configure Inputs"
3. **Check Debug Panel** (black box at top) - should show:
   ```
   Selected: unit_testing
   Inputs: {}
   Pending: false
   ```

---

### Check 4: Add Some Input

For **Unit Testing Agent:**
1. Paste this code in the textarea:
```python
def add(a, b):
    return a + b
```

2. **Check Debug Panel** again - should show:
   ```
   Inputs: {"unit_testing":{"source_code":"def add..."}}
   ```

---

### Check 5: Click Execute

When you click Execute, **Console** should show:
```
Execute button clicked
Selected agents: ["unit_testing"]
Current inputs: {unit_testing: {source_code: "..."}}
Validating inputs...
Validating inputs for unit_testing: {source_code: "..."}
Starting execution...
Starting execution for agents: ["unit_testing"]
Execution requests: [{agent_type: "unit_testing", ...}]
```

If execution stops here, check:
1. Is backend still running?
2. Check backend terminal for errors
3. Try: `curl http://localhost:8000/api/agents/`

---

## ✅ Working Example

### Complete Flow Test:

1. **Select Unit Testing Agent** (blue border appears)

2. **Upload a file** or paste code:
   - Click "Upload file"
   - Choose a `.py` file
   - **You should see**: Green box with file name and size

3. **Check Console** (should show):
   ```
   Uploading file for source_code: test.py 1024
   File test.py read successfully, length: 150
   File uploaded successfully for source_code
   ```

4. **Click Execute**

5. **Console should show**:
   ```
   Execute button clicked
   Selected agents: ["unit_testing"]
   Validating inputs...
   Starting execution...
   Executing single agent
   Single execution response: {execution_id: "..."}
   Execution started successfully
   Toast: [success] Tests started successfully!
   ```

6. **You should see**:
   - Green toast notification
   - "Redirecting..." message
   - After 2 seconds, redirect to /executions page

---

## 🔴 Common Issues & Fixes

### Issue 1: "Backend Connection Error" Screen

**Problem:** Frontend can't reach backend

**Fix:**
```bash
# Check if backend is running
ps aux | grep "python main.py"

# If not running, start it
cd /home/user/QualityForceAI/backend
source venv/bin/activate
python main.py
```

---

### Issue 2: Execute Button Does Nothing

**Check Console for:**

```
Please select at least one agent
```
→ **Fix:** Click on an agent card first

```
Please fix validation errors before executing
```
→ **Fix:** Fill in required fields (marked with `*`)

```
source_code is required
```
→ **Fix:** Add code or upload file

---

### Issue 3: File Upload Not Working

**Console shows:**
```
Failed to read file
```

**Possible causes:**
- File too large (> 10MB)
- File format not supported
- Browser security blocking file read

**Fix:**
- Check file size
- Use supported formats: `.py, .js, .ts, .txt, .md`

---

### Issue 4: Validation Errors

Red error message under field:
```
source_code is required
```

**Fix:**
- Either paste code in textarea
- OR upload a file
- File must not be empty

---

### Issue 5: Backend Error in Console

```
Execution mutation error: Error: Request failed with status code 500
```

**Check backend terminal** for error details:
```
ERROR: Agent type 'unit_testing' not found
```

**Fix:** Backend might have crashed, restart it

---

## 📋 Testing Checklist

Use this to verify everything works:

- [ ] Backend starts without errors
- [ ] Can access http://localhost:8000/api/health
- [ ] Frontend starts without errors
- [ ] Can access http://localhost:5173
- [ ] Can see 7 agents in Marketplace
- [ ] Can select an agent (blue border)
- [ ] Debug panel shows selected agent
- [ ] Can paste text in textarea
- [ ] Can upload a file
- [ ] Green box shows file name after upload
- [ ] Can remove uploaded file (trash icon)
- [ ] Execute button shows validation errors if empty
- [ ] Execute button starts execution with valid input
- [ ] Console shows execution logs
- [ ] Green toast appears on success
- [ ] Redirects to /executions after 2 seconds

---

## 🆘 If Still Not Working

1. **Clear browser cache** (Ctrl+Shift+Del)
2. **Hard refresh** (Ctrl+Shift+R)
3. **Restart both backend and frontend**
4. **Check browser console for ALL errors**
5. **Check backend terminal for ALL errors**

### Get Detailed Logs:

**Backend:**
```bash
# Run with verbose logging
cd backend
python -m uvicorn main:app --reload --log-level debug
```

**Frontend:**
```bash
# Console should show debug panel
# If not, check: process.env.NODE_ENV === 'development'
```

---

## 📝 Report Issue

If still not working, provide:

1. **Backend terminal output** (full)
2. **Browser console output** (full)
3. **Screenshot of Marketplace page**
4. **Screenshot of Debug panel**
5. **Steps you followed**

---

## ✨ Success Indicators

You'll know it's working when you see:

1. ✅ **Green toast** saying "Tests started successfully!"
2. ✅ **Debug panel** shows: `Pending: true` then `false`
3. ✅ **Console logs** show execution response with `execution_id`
4. ✅ **Auto-redirect** to /executions page
5. ✅ **Execution appears** in the executions list

---

## 🎯 Quick Test Script

Run this to test the complete flow:

```bash
# Terminal 1 - Backend
cd /home/user/QualityForceAI/backend
source venv/bin/activate
python main.py &
sleep 5

# Terminal 2 - Test API
curl http://localhost:8000/api/agents/ | jq
curl http://localhost:8000/api/health | jq

# Terminal 3 - Frontend
cd /home/user/QualityForceAI/frontend
npm run dev
```

Then in browser:
1. Go to http://localhost:5173/marketplace
2. Press F12 (open console)
3. Select Unit Testing Agent
4. Paste: `def test(): pass`
5. Click Execute
6. Watch console and wait for success!
