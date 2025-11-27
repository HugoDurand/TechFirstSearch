import React, { useEffect } from 'react';
import {
  View,
  FlatList,
  RefreshControl,
  ActivityIndicator,
  Text,
  StyleSheet,
} from 'react-native';
import { useNavigation } from '@react-navigation/native';
import { StackNavigationProp } from '@react-navigation/stack';
import { RootStackParamList } from '../../App';
import { useContent } from '../context/ContentContext';
import ContentCard from '../components/ContentCard';
import SearchBar from '../components/SearchBar';
import { HomeSEO } from '../components/SEO';
import { Content } from '../types';
import { darkTheme } from '../theme';

type FeedScreenNavigationProp = StackNavigationProp<RootStackParamList, 'Feed'>;

const FeedScreen: React.FC = () => {
  const navigation = useNavigation<FeedScreenNavigationProp>();
  const { contents, loading, error, loadFeed, loadMore, search, refresh, setSearchQuery } = useContent();

  useEffect(() => {
    loadFeed();
  }, []);

  const handleSearch = (query: string) => {
    setSearchQuery(query);
    search(query);
  };

  const handleCardPress = (content: Content) => {
    navigation.navigate('ContentViewer', {
      contentId: content.id,
      url: content.url,
      title: content.title,
    });
  };

  const renderItem = ({ item }: { item: Content }) => (
    <ContentCard content={item} onPress={() => handleCardPress(item)} />
  );

  const renderEmpty = () => {
    if (loading && contents.length === 0) {
      return (
        <View style={styles.centerContainer}>
          <ActivityIndicator size="large" color={darkTheme.contentTypes.paper} />
          <Text style={styles.loadingText}>Loading content...</Text>
        </View>
      );
    }

    if (error) {
      return (
        <View style={styles.centerContainer}>
          <Text style={styles.errorText}>{error}</Text>
          <Text style={styles.errorSubtext}>Pull to refresh</Text>
        </View>
      );
    }

    return (
      <View style={styles.centerContainer}>
        <Text style={styles.emptyText}>No content found</Text>
        <Text style={styles.emptySubtext}>Try a different search</Text>
      </View>
    );
  };

  const renderFooter = () => {
    if (!loading || contents.length === 0) return null;
    return (
      <View style={styles.footerLoader}>
        <ActivityIndicator size="small" color={darkTheme.contentTypes.paper} />
      </View>
    );
  };

  return (
    <View style={styles.container}>
      <HomeSEO />
      <View style={styles.contentWrapper}>
        <SearchBar onSearch={handleSearch} placeholder="Search by title..." />
        <FlatList
          data={contents}
          renderItem={renderItem}
          keyExtractor={(item) => item.id.toString()}
          ListEmptyComponent={renderEmpty}
          ListFooterComponent={renderFooter}
          onEndReached={loadMore}
          onEndReachedThreshold={0.5}
          refreshControl={
            <RefreshControl
              refreshing={loading && contents.length > 0}
              onRefresh={refresh}
              colors={[darkTheme.contentTypes.paper]}
              tintColor={darkTheme.contentTypes.paper}
            />
          }
          contentContainerStyle={contents.length === 0 ? styles.emptyContainer : undefined}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: darkTheme.background.primary,
    alignItems: 'center',
  },
  contentWrapper: {
    flex: 1,
    width: '100%',
    maxWidth: 1200,
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingTop: 100,
  },
  emptyContainer: {
    flexGrow: 1,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 16,
    color: darkTheme.text.secondary,
  },
  errorText: {
    fontSize: 16,
    color: darkTheme.contentTypes.news,
    fontWeight: '600',
  },
  errorSubtext: {
    marginTop: 4,
    fontSize: 14,
    color: darkTheme.text.tertiary,
  },
  emptyText: {
    fontSize: 18,
    color: darkTheme.text.secondary,
    fontWeight: '600',
  },
  emptySubtext: {
    marginTop: 4,
    fontSize: 14,
    color: darkTheme.text.tertiary,
  },
  footerLoader: {
    paddingVertical: 20,
  },
});

export default FeedScreen;

