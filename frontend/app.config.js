export default {
  name: 'TechFirstSearch',
  slug: 'techfirstsearch',
  scheme: 'techfirstsearch',
  version: '1.0.0',
  orientation: 'portrait',
  icon: './assets/icon.png',
  userInterfaceStyle: 'automatic',
  splash: {
    image: './assets/splash.png',
    resizeMode: 'contain',
    backgroundColor: '#0A0A0B'
  },
  assetBundlePatterns: ['**/*'],
  ios: {
    supportsTablet: true,
    bundleIdentifier: 'com.techfirstsearch',
    infoPlist: {
      UIBackgroundModes: []
    }
  },
  web: {
    favicon: './assets/favicon.png',
    bundler: 'webpack'
  },
  plugins: []
};

