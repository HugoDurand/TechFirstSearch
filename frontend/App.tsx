import React from 'react';
import { Platform, LogBox, TouchableOpacity, Text, StyleSheet } from 'react-native';
import { NavigationContainer, LinkingOptions } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import * as Linking from 'expo-linking';
import { HelmetProvider } from 'react-helmet-async';
import FeedScreen from './src/screens/FeedScreen';
import ContentViewerScreen from './src/screens/ContentViewerScreen';
import PrivacyPolicyScreen from './src/screens/PrivacyPolicyScreen';
import { ContentProvider } from './src/context/ContentContext';
import { darkTheme } from './src/theme';

LogBox.ignoreLogs(['sending `onAnimatedValueUpdate` with no listeners registered']);

export type RootStackParamList = {
  Feed: undefined;
  ContentViewer: { contentId: number; url: string; title: string };
  PrivacyPolicy: undefined;
};

const Stack = createStackNavigator<RootStackParamList>();

const prefix = Linking.createURL('/');

const linking: LinkingOptions<RootStackParamList> = {
  prefixes: [prefix, 'https://techfirstsearch.com', 'techfirstsearch://'],
  config: {
    screens: {
      Feed: '',
      ContentViewer: {
        path: 'article/:contentId',
        parse: {
          contentId: (contentId: string) => parseInt(contentId, 10),
        },
        stringify: {
          contentId: (contentId: number) => String(contentId),
        },
      },
      PrivacyPolicy: 'privacy',
    },
  },
};

export default function App() {
  const navigationTheme = {
    dark: true,
    colors: {
      primary: darkTheme.contentTypes.paper,
      background: darkTheme.background.primary,
      card: darkTheme.card.background,
      text: darkTheme.text.primary,
      border: darkTheme.border.primary,
      notification: darkTheme.contentTypes.news,
    },
  };

  const content = (
    <ContentProvider>
      <NavigationContainer 
        theme={navigationTheme}
        linking={linking}
        documentTitle={{
          formatter: (options, route) => 
            route?.name === 'ContentViewer' 
              ? `${(route.params as { title?: string })?.title || 'Article'} | TechFirstSearch`
              : 'TechFirstSearch - Tech News & AI Research Aggregator',
        }}
      >
        <Stack.Navigator
          initialRouteName="Feed"
          screenOptions={{
            headerStyle: {
              backgroundColor: darkTheme.card.background,
              borderBottomWidth: 1,
              borderBottomColor: darkTheme.border.primary,
            },
            headerTintColor: darkTheme.text.primary,
            headerTitleStyle: {
              fontWeight: 'bold',
              color: darkTheme.text.primary,
            },
            headerShadowVisible: false,
          }}
        >
          <Stack.Screen
            name="Feed"
            component={FeedScreen}
            options={({ navigation }) => ({ 
              title: 'TechFirstSearch',
              headerRight: () => (
                <TouchableOpacity
                  onPress={() => navigation.navigate('PrivacyPolicy')}
                  style={styles.headerButton}
                >
                  <Text style={styles.headerButtonText}>ⓘ</Text>
                </TouchableOpacity>
              ),
            })}
          />
          <Stack.Screen
            name="ContentViewer"
            component={ContentViewerScreen}
            options={({ route }) => ({ title: route.params.title })}
          />
          <Stack.Screen
            name="PrivacyPolicy"
            component={PrivacyPolicyScreen}
            options={{ title: 'Privacy Policy' }}
          />
        </Stack.Navigator>
        <StatusBar style="light" />
      </NavigationContainer>
    </ContentProvider>
  );

  if (Platform.OS === 'web') {
    return <HelmetProvider>{content}</HelmetProvider>;
  }

  return content;
}

const styles = StyleSheet.create({
  headerButton: {
    marginRight: 16,
    padding: 4,
  },
  headerButtonText: {
    fontSize: 20,
    color: darkTheme.text.secondary,
  },
});
