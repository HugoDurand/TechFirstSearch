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

const WebIframeViewer: React.FC<{ url: string }> = ({ url }) => {
  const [iframeError, setIframeError] = useState(false);
  const [loading, setLoading] = useState(true);

  if (iframeError) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.title}>Cannot Display In-App</Text>
        <Text style={styles.fallbackText}>
          This website doesn't allow embedding. Open it in a new tab instead.
        </Text>
        <TouchableOpacity
          style={styles.linkButton}
          onPress={() => window.open(url, '_blank')}
        >
          <Text style={styles.linkButtonText}>Open in New Tab →</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <View style={styles.iframeContainer}>
      {loading && (
        <View style={styles.iframeLoading}>
          <ActivityIndicator size="large" color={darkTheme.contentTypes.paper} />
          <Text style={styles.loadingText}>Loading article...</Text>
        </View>
      )}
      <iframe
        src={url}
        style={{
          width: '100%',
          height: '100%',
          border: 'none',
          display: loading ? 'none' : 'block',
        }}
        onLoad={() => setLoading(false)}
        onError={() => setIframeError(true)}
        sandbox="allow-same-origin allow-scripts allow-popups allow-forms"
        referrerPolicy="no-referrer"
      />
      <View style={styles.iframeFooter}>
        <TouchableOpacity
          style={styles.openExternalButton}
          onPress={() => window.open(url, '_blank')}
        >
          <Text style={styles.openExternalText}>Open in New Tab ↗</Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

const ContentViewerScreen: React.FC = () => {
  const route = useRoute<ContentViewerRouteProp>();
  const { contentId, url: paramUrl, title: paramTitle } = route.params || {};
  const { width } = useWindowDimensions();
  
  const [article, setArticle] = useState<ContentDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [useWebView, setUseWebView] = useState(false);
  const [articleUrl, setArticleUrl] = useState(paramUrl || '');

  useEffect(() => {
    if (contentId) {
      loadArticle();
    }
  }, [contentId]);

  const isContentCorrupted = (content: string): boolean => {
    if (!content || content.length < 100) return true;
    const nonPrintableCount = (content.match(/[\x00-\x1F\x7F-\x9F]/g) || []).length;
    const ratio = nonPrintableCount / content.length;
    return ratio > 0.05;
  };

  const getDisplayContent = (article: ContentDetail): string | null => {
    if (article.full_content && !isContentCorrupted(article.full_content)) {
      return article.full_content;
    }
    if (article.reader_mode_content && article.reader_mode_content.trim().length > 100) {
      const paragraphs = article.reader_mode_content
        .split('\n\n')
        .filter(p => p.trim())
        .map(p => `<p>${p}</p>`)
        .join('');
      return `<div>${paragraphs}</div>`;
    }
    return null;
  };

  const loadArticle = async () => {
    try {
      const data = await fetchArticle(contentId);
      setArticle(data);
      setArticleUrl(data.url || paramUrl || '');
      
      const displayContent = getDisplayContent(data);
      if (!displayContent) {
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

  if (!contentId) {
    return (
      <View style={styles.centerContainer}>
        <Text style={styles.title}>Article Not Found</Text>
        <Text style={styles.fallbackText}>
          The article you're looking for doesn't exist or the link is invalid.
        </Text>
      </View>
    );
  }

  if (useWebView || !article || !article.full_content) {
    if (!articleUrl) {
      return (
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color={darkTheme.contentTypes.paper} />
          <Text style={styles.loadingText}>Loading...</Text>
        </View>
      );
    }
    
    if (Platform.OS === 'web') {
      return <WebIframeViewer url={articleUrl} />;
    } else {
      return (
        <WebView
          source={{ uri: articleUrl }}
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
          source={{ html: getDisplayContent(article) || '' }}
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
              window.open(articleUrl, '_blank');
            } else {
              Linking.openURL(articleUrl);
            }
          }}
        >
          <Text style={styles.sourceLink}>{articleUrl}</Text>
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
  iframeContainer: {
    flex: 1,
    backgroundColor: darkTheme.background.primary,
    // @ts-ignore - web only
    height: '100vh',
  },
  iframeLoading: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: darkTheme.background.primary,
    zIndex: 1,
  },
  iframeFooter: {
    position: 'absolute',
    bottom: 0,
    left: 0,
    right: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    padding: 12,
    alignItems: 'center',
  },
  openExternalButton: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    backgroundColor: darkTheme.contentTypes.paper,
    borderRadius: 6,
  },
  openExternalText: {
    color: '#FFFFFF',
    fontSize: 14,
    fontWeight: '600',
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
