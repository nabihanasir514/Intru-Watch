
## 👤 1. Biometric Enrollment (Face Images)

The system doesn't just "upload" an image; it captures them to train the recognizer.

* **Navigate to:** `System Administration` -> `User Enrollment`.
* **Method:** Use the **Live Camera Feed** within the app.
* **Process:** 1. Enter the User's Name and ID.
2. Click **"Capture Sample"**.
3. The system requires **3 unique samples** per person.
4. Once 3 samples are saved to the `data/faces/` directory, click **"Train Recognizer"** to update the `trainer.yml` file.

---

## 📊 2. Database & Record Files

IntruWatch automatically manages its own data persistence using `.csv` and `.pkl` files. If you need to manually move or backup files, look for the following in your project directory:

* **Resident Data:** `data/checkins.csv` (Stores current campus residents).
* **Security Logs:** `data/logins.csv` (Stores operator credentials).
* **Guard Rosters:** `data/guards.pkl` (Serialized Binary Search Tree of personnel).
* **Recognition Model:** `data/trainer.yml` (The trained biometric weights).

---

## 🛠️ 3. Importing Code into GitHub

If your goal is to "upload" these files to your GitHub repository:

1. **Initialize Git:** `git init`
2. **Add Files:** `git add app.py data_structures.py utils.py`
3. **Commit:** `git commit -m "Initial Security System Deployment"`
4. **Push:** `git push origin main`

> **Security Note:** Ensure your `.gitignore` file includes `data/faces/` and `data/logins.csv` to avoid leaking sensitive biometric data or operator passwords to a public repository.

---

### Troubleshooting Upload Errors

* **Permission Denied:** Ensure the `data/` folder has write permissions so the script can save captured images.
* **Missing Directories:** If the app crashes, manually create a folder named `data` in your root directory.
* **Camera Not Found:** Ensure no other application (like Zoom or Teams) is using your webcam during the enrollment phase.

**Would you like me to generate a `.gitignore` file tailored for this project to keep your sensitive security data private?**
