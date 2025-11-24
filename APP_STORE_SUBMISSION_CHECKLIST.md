# App Store Submission Checklist

**App**: TechFirstSearch v1.0.0  
**Date**: November 24, 2025  
**Target Platform**: iOS App Store

---

## ❌ CRITICAL - Must Complete Before Submission

These will **block your submission** if not completed:

### 1. Privacy Policy ❌ REQUIRED
- [ ] Write privacy policy document
- [ ] Host on public URL (GitHub Pages, your domain, etc.)
- [ ] Add link in app (Settings or About screen)
- [ ] Enter URL in App Store Connect "Privacy Policy URL" field
- **Why**: Apple REQUIRES this for ALL apps, even those that don't collect data
- **Time**: 1-2 hours
- **Template**: See APPLE_APP_STORE_COMPLIANCE.md section 5.1

### 2. Bundle Identifier ⚠️ RECOMMENDED
- [ ] Change `com.techfirstsearch` to `com.yourdomain.techfirstsearch`
- [ ] Update in `frontend/app.json`
- **Why**: Should use a domain you actually own
- **Time**: 5 minutes

### 3. App Icon ❌ REQUIRED
- [ ] Design 1024x1024px PNG icon
- [ ] No transparency
- [ ] No rounded corners (Apple adds them)
- [ ] Upload to App Store Connect
- **Why**: Placeholder icons are rejected
- **Time**: 2-4 hours (or hire designer)
- **Tools**: Canva, Figma, or Fiverr ($5-50)

### 4. Screenshots ❌ REQUIRED
- [ ] iPhone 6.7" (iPhone 15 Pro Max) - 3-5 screenshots
- [ ] iPhone 6.5" (iPhone 14 Plus) - 3-5 screenshots  
- [ ] iPhone 5.5" (iPhone 8 Plus) - 3-5 screenshots
- [ ] iPad 12.9" - 3-5 screenshots
- **Why**: Required for App Store listing
- **Time**: 1 hour
- **Tools**: iOS Simulator + Screenshot (⌘+S)

---

## ⚠️ IMPORTANT - Required for Submission

### 5. App Store Connect Metadata
- [ ] App Name: "TechFirstSearch"
- [ ] Subtitle (optional): "Tech News & Articles"
- [ ] Description (500-4000 chars)
- [ ] Keywords: tech, news, learning, articles, developer, programming
- [ ] Category: News or Education
- [ ] Age Rating: 12+ or 17+
- [ ] Support URL: your website or GitHub
- [ ] Marketing URL (optional)
- **Time**: 30 minutes

### 6. App Privacy Details
- [ ] Answer: "Do you collect data?" → NO
- [ ] Answer: "Third-party SDKs?" → NO
- [ ] Answer: "Data used for tracking?" → NO
- **Result**: App shows "No Data Collected" badge ✅
- **Time**: 10 minutes

### 7. Developer Account
- [ ] Apple Developer Program membership ($99/year)
- [ ] Banking information complete
- [ ] Tax information complete
- [ ] Contact information current
- **Time**: Already done or 30 minutes

---

## ✅ TESTING - Verify Before Upload

### 8. Functional Testing
- [ ] Test on physical iOS device (not just simulator)
- [ ] Test feed loading
- [ ] Test search functionality
- [ ] Test article reading (reader mode + webview)
- [ ] Test offline/no internet handling
- [ ] Check for crashes
- [ ] Verify all links work
- [ ] Test dark mode
- **Time**: 1-2 hours

### 9. Content Verification
- [ ] Verify attribution appears on all articles
- [ ] Verify clickable links to original sources
- [ ] Check that no objectionable content appears
- [ ] Test language filtering (English only)
- [ ] Verify no duplicate articles
- **Time**: 30 minutes

---

## 🚀 BUILD & UPLOAD

### 10. Production Build
- [ ] Generate iOS build in Xcode
- [ ] Archive for distribution
- [ ] Upload via Xcode or Transporter
- [ ] Wait for processing in App Store Connect
- **Time**: 1-2 hours (first time)

### 11. App Store Connect Final Steps
- [ ] Select build for release
- [ ] Set release type (Manual or Automatic)
- [ ] Answer export compliance:
  - [ ] Uses encryption? → Standard encryption (HTTPS)
  - [ ] OR No encryption (if using HTTP only)
- [ ] Add version notes (what's new)
- [ ] Click "Submit for Review"
- **Time**: 15 minutes

---

## 📋 OPTIONAL BUT RECOMMENDED

### 12. Polish & Extras
- [ ] Add Settings/About screen in app
- [ ] Add "Rate this App" prompt (using Apple API)
- [ ] Add share functionality
- [ ] Test with TestFlight beta testers
- [ ] Prepare marketing materials
- [ ] Create website/landing page
- **Time**: 2-4 hours

### 13. Launch Preparation
- [ ] Prepare launch announcement
- [ ] Ready social media posts
- [ ] Plan for user feedback handling
- [ ] Set up support email
- **Time**: 2-4 hours

---

## ⏱️ ESTIMATED TIMELINE

| Phase | Time | Status |
|-------|------|--------|
| **Critical Items** (Privacy, Icon, Screenshots) | 1-2 days | ⬜ Not Started |
| **Metadata & Account Setup** | 1 hour | ⬜ Not Started |
| **Testing & Verification** | 2-3 hours | ⬜ Not Started |
| **Build & Upload** | 2-3 hours | ⬜ Not Started |
| **Apple Review** | 1-3 days | ⬜ Not Started |
| **TOTAL TIME TO LAUNCH** | ~5-7 days | ⬜ Not Started |

---

## 🎯 TODAY'S PRIORITY

Start with these in order:

1. **Create Privacy Policy** (1-2 hours) - BLOCKER
2. **Design App Icon** (2-4 hours) - BLOCKER  
3. **Take Screenshots** (1 hour) - BLOCKER
4. **Update Bundle ID** (5 min) - Quick win
5. **Test on Device** (1 hour) - Critical

**Goal for Today**: Complete privacy policy and start icon design

**Goal for This Week**: Submit to App Store

---

## 🚨 COMMON REJECTION REASONS (Avoid These!)

- ❌ Missing privacy policy → **FIX #1**
- ❌ Placeholder app icon → **FIX #3**
- ❌ Screenshots don't match app
- ❌ App crashes during review
- ❌ Broken links or non-functional features
- ❌ Incomplete metadata

**Your App's Strengths**:
- ✅ No user data collection (easy privacy compliance)
- ✅ No monetization (no IAP complexity)
- ✅ Simple, focused functionality
- ✅ Proper content attribution
- ✅ No controversial features

---

## 📞 NEED HELP?

### Resources
- [Apple's App Store Connect Help](https://developer.apple.com/help/app-store-connect/)
- [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)

### Tools
- **Privacy Policy**: [TermsFeed Generator](https://www.termsfeed.com/privacy-policy-generator/)
- **App Icon**: Canva, Figma, Fiverr
- **Screenshots**: [AppLaunchpad](https://theapplaunchpad.com/), [Screenshot.rocks](https://screenshot.rocks/)

### If Rejected
1. Read the rejection reason carefully
2. Fix the specific issue
3. Resubmit (usually within 24 hours)
4. Use "Appeal" if you disagree

---

## ✅ COMPLETION TRACKING

**Progress**: 0 / 13 major items completed

**Last Updated**: November 24, 2025

**Next Review**: [Date after completing items]

---

## NOTES

- First-time submissions often take longer (extra scrutiny)
- Be responsive if App Review contacts you
- Have demo account ready if needed (N/A for your app)
- Monitor App Store Connect notifications

**Good luck with your submission!** 🚀

Your app is solid - just need to complete the administrative requirements and you'll be on the App Store!

