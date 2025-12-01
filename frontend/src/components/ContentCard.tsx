import React from 'react';
import { View, Text, TouchableOpacity, StyleSheet, Image } from 'react-native';
import { Content } from '../types';
import { darkTheme } from '../theme';
import PlaceholderImage from './PlaceholderImage';

interface ContentCardProps {
  content: Content;
  onPress: () => void;
}

const ContentCard: React.FC<ContentCardProps> = ({ content, onPress }) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    if (diffInHours < 48) return 'Yesterday';
    if (diffInHours < 168) return `${Math.floor(diffInHours / 24)}d ago`;
    
    return date.toLocaleDateString();
  };

  const getBadgeColor = () => {
    return darkTheme.contentTypes[content.content_type as keyof typeof darkTheme.contentTypes] || darkTheme.text.muted;
  };

  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.7}>
      {content.thumbnail_url ? (
        <Image
          source={{ uri: content.thumbnail_url }}
          style={styles.thumbnail}
          resizeMode="cover"
        />
      ) : (
        <PlaceholderImage 
          contentType={content.content_type} 
          width={400} 
          height={200}
        />
      )}
      
      <View style={styles.content}>
        <View style={[styles.badge, { backgroundColor: getBadgeColor() }]}>
          <Text style={styles.badgeText}>{content.content_type.toUpperCase()}</Text>
        </View>
        
        <Text style={styles.title} numberOfLines={3}>
          {content.title}
        </Text>
        
        {content.ai_summary && (
          <View style={styles.summaryContainer}>
            <Text style={styles.summaryLabel}>TL;DR</Text>
            <Text style={styles.summaryText} numberOfLines={3}>
              {content.ai_summary}
            </Text>
          </View>
        )}
        
        <View style={styles.metadata}>
          <Text style={styles.metadataText}>{content.source_name}</Text>
          <Text style={styles.metadataSeparator}>•</Text>
          <Text style={styles.metadataText}>{formatDate(content.published_date)}</Text>
        </View>
        
        {content.author && (
          <Text style={styles.author} numberOfLines={1}>
            by {content.author}
          </Text>
        )}
      </View>
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  card: {
    backgroundColor: darkTheme.card.background,
    borderRadius: 12,
    marginHorizontal: 16,
    marginVertical: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.5,
    shadowRadius: 8,
    elevation: 4,
    overflow: 'hidden',
    borderWidth: 1,
    borderColor: darkTheme.border.primary,
  },
  thumbnail: {
    width: '100%',
    height: 200,
  },
  content: {
    padding: 16,
  },
  badge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 8,
    paddingVertical: 4,
    borderRadius: 4,
    marginBottom: 8,
  },
  badgeText: {
    color: darkTheme.background.primary,
    fontSize: 10,
    fontWeight: '700',
    letterSpacing: 0.5,
  },
  title: {
    fontSize: 18,
    fontWeight: '600',
    color: darkTheme.text.primary,
    marginBottom: 8,
    lineHeight: 24,
  },
  summaryContainer: {
    backgroundColor: darkTheme.background.secondary,
    borderRadius: 8,
    padding: 12,
    marginBottom: 12,
    borderLeftWidth: 3,
    borderLeftColor: darkTheme.contentTypes.paper,
  },
  summaryLabel: {
    fontSize: 10,
    fontWeight: '700',
    color: darkTheme.contentTypes.paper,
    letterSpacing: 1,
    marginBottom: 4,
  },
  summaryText: {
    fontSize: 14,
    color: darkTheme.text.secondary,
    lineHeight: 20,
  },
  metadata: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  metadataText: {
    fontSize: 12,
    color: darkTheme.text.secondary,
  },
  metadataSeparator: {
    fontSize: 12,
    color: darkTheme.text.tertiary,
    marginHorizontal: 6,
  },
  author: {
    fontSize: 12,
    color: darkTheme.text.tertiary,
    fontStyle: 'italic',
    marginTop: 4,
  },
});

export default ContentCard;

