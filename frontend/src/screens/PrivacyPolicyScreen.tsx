import React from 'react';
import { ScrollView, Text, StyleSheet, View, Platform, Linking } from 'react-native';
import { darkTheme } from '../theme';

const PrivacyPolicyScreen: React.FC = () => {
  const lastUpdated = 'November 27, 2025';

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.content}>
      <Text style={styles.title}>Privacy Policy</Text>
      <Text style={styles.lastUpdated}>Last updated: {lastUpdated}</Text>

      <View style={styles.section}>
        <Text style={styles.heading}>Introduction</Text>
        <Text style={styles.paragraph}>
          TechFirstSearch ("we," "our," or "us") is committed to protecting your privacy. 
          This Privacy Policy explains how we handle information when you use our mobile 
          application and website (collectively, the "Service").
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>Information We Collect</Text>
        <Text style={styles.paragraph}>
          TechFirstSearch is designed with privacy in mind. We do not collect, store, or 
          process any personal information from our users.
        </Text>
        <Text style={styles.subheading}>What We Don't Collect:</Text>
        <Text style={styles.listItem}>• Personal identification information (name, email, phone)</Text>
        <Text style={styles.listItem}>• Location data</Text>
        <Text style={styles.listItem}>• Device identifiers or tracking data</Text>
        <Text style={styles.listItem}>• Usage analytics or behavioral data</Text>
        <Text style={styles.listItem}>• Cookies or similar tracking technologies</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>How the App Works</Text>
        <Text style={styles.paragraph}>
          TechFirstSearch aggregates publicly available tech news, research papers, and 
          articles from various sources. The content is fetched from public RSS feeds 
          and APIs. We display this content within the app for your convenience.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>Third-Party Content</Text>
        <Text style={styles.paragraph}>
          When you click on an article to read the full content, you may be directed to 
          the original source website. These third-party websites have their own privacy 
          policies, and we encourage you to review them. We are not responsible for the 
          privacy practices of external websites.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>No User Accounts</Text>
        <Text style={styles.paragraph}>
          TechFirstSearch does not require user registration or login. There are no user 
          accounts, and therefore no personal data is stored on our servers related to 
          individual users.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>Data Storage</Text>
        <Text style={styles.paragraph}>
          We store aggregated article content (titles, summaries, and links) on our servers 
          to provide the Service. This content is publicly available information and does 
          not include any user data.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>Children's Privacy</Text>
        <Text style={styles.paragraph}>
          Our Service is not directed to children under 13. We do not knowingly collect 
          any information from children. If you believe we have inadvertently collected 
          information from a child, please contact us immediately.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>Changes to This Policy</Text>
        <Text style={styles.paragraph}>
          We may update this Privacy Policy from time to time. We will notify you of any 
          changes by posting the new Privacy Policy on this page and updating the "Last 
          updated" date.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.heading}>Contact Us</Text>
        <Text style={styles.paragraph}>
          If you have any questions about this Privacy Policy, please contact us at:
        </Text>
        <Text 
          style={styles.email}
          onPress={() => {
            if (Platform.OS === 'web') {
              window.open('mailto:privacy@techfirstsearch.com', '_blank');
            } else {
              Linking.openURL('mailto:privacy@techfirstsearch.com');
            }
          }}
        >
          privacy@techfirstsearch.com
        </Text>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>
          © 2025 TechFirstSearch. All rights reserved.
        </Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: darkTheme.background.primary,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
    maxWidth: 800,
    alignSelf: 'center',
    width: '100%',
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: darkTheme.text.primary,
    marginBottom: 8,
  },
  lastUpdated: {
    fontSize: 14,
    color: darkTheme.text.tertiary,
    marginBottom: 24,
  },
  section: {
    marginBottom: 24,
  },
  heading: {
    fontSize: 20,
    fontWeight: '600',
    color: darkTheme.text.primary,
    marginBottom: 12,
  },
  subheading: {
    fontSize: 16,
    fontWeight: '600',
    color: darkTheme.text.secondary,
    marginTop: 12,
    marginBottom: 8,
  },
  paragraph: {
    fontSize: 16,
    lineHeight: 24,
    color: darkTheme.text.secondary,
  },
  listItem: {
    fontSize: 16,
    lineHeight: 28,
    color: darkTheme.text.secondary,
    paddingLeft: 8,
  },
  email: {
    fontSize: 16,
    color: darkTheme.contentTypes.paper,
    marginTop: 8,
    textDecorationLine: 'underline',
  },
  footer: {
    marginTop: 40,
    paddingTop: 20,
    borderTopWidth: 1,
    borderTopColor: darkTheme.border.primary,
  },
  footerText: {
    fontSize: 14,
    color: darkTheme.text.tertiary,
    textAlign: 'center',
  },
});

export default PrivacyPolicyScreen;

