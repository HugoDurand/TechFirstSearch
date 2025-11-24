import React, { useEffect, useState } from 'react';
import {
  View,
  ScrollView,
  Text,
  ActivityIndicator,
  StyleSheet,
  useWindowDimensions,
  Platform,
  Linking,
  TouchableOpacity,
} from 'react-native';
import { WebView } from 'react-native-webview';
import RenderHtml from 'react-native-render-html';
import { RouteProp, useRoute } from '@react-navigation/native';
import { RootStackParamList } from '../../App';
import { fetchArticle } from '../services/api';
import { ContentDetail } from '../types';
import { darkTheme } from '../theme';

type ContentViewerRouteProp = RouteProp<RootStackParamList, 'ContentViewer'>;

const ContentViewerScreen: React.FC = () => {
  const route = useRoute<ContentViewerRouteProp>();
  const { contentId, url } = route.params;
  const { width } = useWindowDimensions();
  
  const [article, setArticle] = useState<ContentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [useWebView, setUseWebView] = useState(false);

  useEffect(() => {
    loadArticle();
  }, [contentId]);

  const loadArticle = async () => {
    try {
      const data = await fetchArticle(contentId);
      setArticle(data);
      
      if (!data.full_content || data.full_content.trim().length < 200) {
        setUseWebView(true);
      }
    } catch (err) {
      console.error('Failed to load article:', err);
      setUseWebView(true);
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    });
  };

  if (loading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color={darkTheme.contentTypes.paper} />
        <Text style={styles.loadingText}>Loading article...</Text>
      </View>
    );
  }

  // Web platform doesn't support WebView
  if (useWebView || !article || !article.full_content) {
    if (Platform.OS === 'web') {
      // On web, provide a link to open in new tab
      return (
        <View style={styles.centerContainer}>
          <Text style={styles.title}>Content Not Available</Text>
          <Text style={styles.fallbackText}>
            This content couldn't be extracted for viewing in the app.
          </Text>
          <TouchableOpacity
            style={styles.linkButton}
            onPress={() => {
              if (Platform.OS === 'web') {
                window.open(url, '_blank');
              } else {
                Linking.openURL(url);
              }
            }}
          >
            <Text style={styles.linkButtonText}>Open Original Article →</Text>
          </TouchableOpacity>
        </View>
      );
    } else {
      // On mobile, use WebView
      return (
        <WebView
          source={{ uri: url }}
          style={styles.webview}
          startInLoadingState={true}
          renderLoading={() => (
            <View style={styles.centerContainer}>
              <ActivityIndicator size="large" color="#3B82F6" />
            </View>
          )}
        />
      );
    }
  }

  const htmlStyles = {
    body: {
      color: darkTheme.text.secondary,
      fontSize: 16,
      lineHeight: 28,
    },
    p: {
      marginBottom: 16,
      color: darkTheme.text.secondary,
    },
    a: {
      color: darkTheme.contentTypes.paper,
      textDecorationLine: 'none' as const,
    },
    h1: {
      color: darkTheme.text.primary,
      fontSize: 24,
      fontWeight: '700' as const,
      marginVertical: 12,
    },
    h2: {
      color: darkTheme.text.primary,
      fontSize: 20,
      fontWeight: '700' as const,
      marginVertical: 10,
    },
    h3: {
      color: darkTheme.text.primary,
      fontSize: 18,
      fontWeight: '600' as const,
      marginVertical: 8,
    },
    img: {
      marginVertical: 16,
    },
    blockquote: {
      borderLeftColor: darkTheme.border.secondary,
      borderLeftWidth: 4,
      paddingLeft: 16,
      marginVertical: 12,
      fontStyle: 'italic' as const,
    },
    code: {
      backgroundColor: darkTheme.background.tertiary,
      color: darkTheme.contentTypes.tutorial,
      padding: 4,
      borderRadius: 4,
    },
    pre: {
      backgroundColor: darkTheme.background.tertiary,
      padding: 12,
      borderRadius: 8,
      marginVertical: 12,
    },
  };

  return (
    <ScrollView style={styles.container} contentContainerStyle={styles.contentContainer}>
      <View style={styles.header}>
        <Text style={styles.title}>{article.title}</Text>
        
        <View style={styles.metadata}>
          <Text style={styles.metadataText}>{article.source_name}</Text>
          {article.author && (
            <>
              <Text style={styles.separator}>•</Text>
              <Text style={styles.metadataText}>{article.author}</Text>
            </>
          )}
          <Text style={styles.separator}>•</Text>
          <Text style={styles.metadataText}>{formatDate(article.published_date)}</Text>
        </View>
      </View>

      <View style={styles.content}>
        <RenderHtml
          contentWidth={Math.min(width, 900)}
          source={{ html: article.full_content }}
          tagsStyles={htmlStyles}
          baseStyle={{
            color: darkTheme.text.secondary,
          }}
        />
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerLabel}>Source: </Text>
        <TouchableOpacity
          onPress={() => {
            if (Platform.OS === 'web') {
              window.open(url, '_blank');
            } else {
              Linking.openURL(url);
            }
          }}
        >
          <Text style={styles.sourceLink}>{url}</Text>
        </TouchableOpacity>
        <Text style={styles.footerNote}>
          Tap to read the original article
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
  contentContainer: {
    paddingBottom: 40,
    maxWidth: 900,
    width: '100%',
    alignSelf: 'center',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: darkTheme.background.primary,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: darkTheme.text.secondary,
  },
  webview: {
    flex: 1,
    backgroundColor: darkTheme.background.primary,
  },
  header: {
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: darkTheme.border.primary,
    backgroundColor: darkTheme.card.background,
  },
  title: {
    fontSize: 24,
    fontWeight: '700',
    color: darkTheme.text.primary,
    lineHeight: 32,
    marginBottom: 12,
  },
  metadata: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    alignItems: 'center',
  },
  metadataText: {
    fontSize: 14,
    color: darkTheme.text.secondary,
  },
  separator: {
    fontSize: 14,
    color: darkTheme.text.tertiary,
    marginHorizontal: 8,
  },
  content: {
    padding: 20,
    backgroundColor: darkTheme.background.secondary,
  },
  bodyText: {
    fontSize: 16,
    lineHeight: 28,
    color: darkTheme.text.secondary,
  },
  footer: {
    padding: 20,
    borderTopWidth: 1,
    borderTopColor: darkTheme.border.primary,
    backgroundColor: darkTheme.card.background,
    alignItems: 'flex-start',
  },
  footerLabel: {
    fontSize: 12,
    color: darkTheme.text.tertiary,
    marginBottom: 4,
  },
  sourceLink: {
    fontSize: 12,
    color: darkTheme.contentTypes.paper,
    textDecorationLine: 'underline',
    marginBottom: 8,
  },
  footerNote: {
    fontSize: 11,
    color: darkTheme.text.tertiary,
    fontStyle: 'italic',
    marginTop: 4,
  },
  fallbackText: {
    fontSize: 16,
    color: darkTheme.text.secondary,
    textAlign: 'center',
    marginTop: 12,
    marginBottom: 24,
    paddingHorizontal: 20,
  },
  linkButton: {
    backgroundColor: darkTheme.contentTypes.paper,
    paddingHorizontal: 24,
    paddingVertical: 12,
    borderRadius: 8,
    marginTop: 12,
  },
  linkButtonText: {
    fontSize: 16,
    fontWeight: '600',
    color: '#FFFFFF',
  },
});

export default ContentViewerScreen;

