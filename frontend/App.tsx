import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { StatusBar } from 'expo-status-bar';
import FeedScreen from './src/screens/FeedScreen';
import ContentViewerScreen from './src/screens/ContentViewerScreen';
import { ContentProvider } from './src/context/ContentContext';
import { darkTheme } from './src/theme';

export type RootStackParamList = {
  Feed: undefined;
  ContentViewer: { contentId: number; url: string; title: string };
};

const Stack = createStackNavigator<RootStackParamList>();

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

  return (
    <ContentProvider>
      <NavigationContainer theme={navigationTheme}>
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
            options={{ title: 'TechFirstSearch' }}
          />
          <Stack.Screen
            name="ContentViewer"
            component={ContentViewerScreen}
            options={({ route }) => ({ title: route.params.title })}
          />
        </Stack.Navigator>
        <StatusBar style="light" />
      </NavigationContainer>
    </ContentProvider>
  );
}

